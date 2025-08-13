# Copyright (c) 2023-2025 Hammerspace, Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests as requests

from typing import (
    Callable,
    Mapping,
    Optional,
    Sequence,
    TypeVar,
    Union,
    Any,
)

from HammerSDK.lib import log
from HammerSDK.lib.uri import UriBuilder

Body = Union[Sequence[object], Mapping[str, object]]

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_FORM = 'application/x-www-form-urlencoded'

LOGIN_ERROR = "You need to login to establish credentials"

# Decorator for different methods

RequestFunction = TypeVar('RequestFunction', bound=Callable[..., 'Any'])


# Decorator for request methods

def request(fn: RequestFunction) -> RequestFunction:
    setattr(fn, 'request', True)
    return fn


# We are trying to create a connection class more for the future than anything else.
# Right now, the Hammerspace API uses a cookie versus an OAuth authentication model.
# In the OAuth model, we would have a connection and credentials.

# In this class, we will hold the host, port, and build a URL. Rather than use the
# requests library "as-is", we will instead go a little lower level and build a
# request based upon the method (GET, POST, etc).

class Connection:
    def __init__(
        self,
        host: str,
        port: int,
        timeout: Optional[int] = None,
    ):
        self.session = None
        self.host = host
        self.port = port
        self.scheme = 'https'
        self.timeout = timeout

    def is_connected(self) -> bool:
        return self.session is not None

    def open(self) -> requests.Session:
        if not self.is_connected():
            self.session = requests.Session()

        return self.session

    def close(self) -> None:
        """
        Close the underlying network connection.

        An explicit close() should not strictly be necessary, as refcount GC
        will also ensure the connection gets closed. This provides a stronger
        guarantee or tighter control if desired (e.g. it might be useful when a
        long lived instance has long idle periods).
        """
        if self.session:
            self.session = None

    # Format the prepped request so that we can look at it (if debugging is enabled)

    def format_prepped_request(self, prepped, encoding=None):
        # prepped has .method, .path_url, .headers and .body attribute to view the request
        encoding = encoding or requests.utils.get_encoding_from_headers(prepped.headers)

        if isinstance(prepped.body, str):
            body = prepped.body
        elif prepped.body is None:
            body = ""
        else:
            body = prepped.body.decode(encoding) if encoding else '<binary data>'

        headers = '\n'.join(['{}: {}'.format(*hv) for hv in prepped.headers.items()])
        return f"""\
    {prepped.method} {prepped.path_url} HTTP/1.1
    {headers}

    {body}"""

    # This is the main workhorse... We will build a url and utilize the requests
    # python library to handle the operation. In the future, we will throw off the
    # yoke of this library as it primarily deals with cookie based authentication.

    def request(
        self,
        method: str,
        uri: str,
        body: Optional[Body] = None,
        request_content_type: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
        no_delay: Optional[bool] = False,
    ) -> requests.Response:

        # Start out by building the URL.

        self.api_url = UriBuilder(self.scheme, self.host, self.port, uri)

        # Build the uri and headers for this request

        self.build_headers(request_content_type, headers)

        # Prepare the request and send it to the recipient

        self.prepare_and_send(method, body)

        # The API might have passed back that a task was created. If so, then query the task until
        # we get a response... Otherwise, move on...

        if not no_delay:
            self.query_task(self.response, request_content_type)

        # Determine if there is a problem with the message returned and raise an error
        # if there is... The requests library will not raise an error as long as the
        # communication is open and working. It is up to the application library (this
        # module) to look at the reply and figure out if something didn't work.

        return self.parse_response()

    # In some cases, we might have to make another HTTP call because we got a task ID as a return to a previous call
    # This means that the previous function in the API created a task and didn't return anything meaningful
    # Now, we have to query the task and grab the end result once it completes

    def query_task(self,
                   prev_response: requests.Response,
                   request_content_type: Optional[str] = None):

        if prev_response.status_code == 202:

            # If the headers from the previous response have a Location tag, that indicates that a task is running
            # We will need to loop until the task is completed

            # Get the Task URI if it exists

            if not prev_response.headers.get('Location'):
                return

            self.api_url = prev_response.headers['Location']

            # Delete the task id in the headers so that we can copy them over for re-use

            del prev_response.headers['Location']

            # Build the headers

            self.build_headers(request_content_type, prev_response.headers)

            # Now, loop until we get a completed status

            while (True):

                # Finally, send the request to query the task

                self.prepare_and_send('GET')

                # Check the response and raise an exception if there is an error

                self.parse_response()

                # Has the job completed? If not, then loop and do it again

                task_response = self.response.json()
                if task_response["status"] == "COMPLETED":
                    return

    # Prepare the request and send it to the recipient

    def prepare_and_send(self,
                         method: str,
                         body: Optional[Body] = None):

        # Prepare the request and send it to the recipient

        try:
            if 'Content-Type' in self.new_headers and self.new_headers['Content-Type'] == "application/json":
                req = requests.Request(method, self.api_url, json=body, headers=self.new_headers)
            else:
                req = requests.Request(method, self.api_url, data=body, headers=self.new_headers)

            # prepped.body = data

            prepped = self.session.prepare_request(req)

            # Log the prepped request for debugging purposes

            log.debug(self.format_prepped_request(prepped, 'utf8'))

            # Send the request

            self.response = self.session.send(prepped,
                                              stream=False,
                                              timeout=self.timeout,
                                              verify=False,
                                              cert=None,
                                              proxies=None)
        except (ConnectionError,):

            # If the connection has received an error, it can no longer be reused.
            # Close it so that the next request will open a new connection.

            self.close()
            raise

    # Build the URI and the headers

    def build_headers(self,
                  request_content_type: Optional[str] = None,
                  headers: Optional[Mapping[str, str]] = None):

        # Before we do anything, make sure that we have a valid session

        if not self.is_connected():
            raise requests.ConnectionError(LOGIN_ERROR)

        # Build the headers

        self.new_headers = {}

        # Copy any headers passed from the caller

        if headers:
            for key, value in headers.items():
                self.new_headers[key] = value

        # Copy the request content type if it exists

        if request_content_type:
            self.new_headers['Content-Type'] = request_content_type

    # Determine if we have an valid or invalid response.

    def parse_response(self) -> requests.Response:

        log.debug('RESPONSE STATUS: %d' % self._status())

        # What is the status of the response

        if not self._success():
            log.debug('Server replied: %d %s' % (self._status(), self._reason()))

            # Raise an error and let the caller take care of it

            self.response.raise_for_status()

        else:
            return self.response

    def _status(self) -> int:
        assert hasattr(self, "response")
        return self.response.status_code

    def _success(self) -> bool:
        return self._status() >= 200 and self._status() < 300

    def _reason(self) -> str:
        assert hasattr(self, "response")
        return self.response.reason
