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

import requests
import HammerSDK.lib.request as request

NOT_CONNECTED = "Not logged in or connected to Hammerspace environment"

# SDK Version                                                                                  
SDK_Version = "5.1.18"


# Login to the Hammerspace environment

@request.request
def login(
        conninfo: request.Connection,
        username: str,
        password: str):
    """
    Login to the  Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        username (str): The username used to login to the Hammerspace Anvil
        password (str): The password used to login to the Hammerspace Anvil
    Returns:
        None
    """

    header = {}
    header['Accept'] = 'application/json'

    # Setup the method, uri, and login info (body)

    method = 'POST'
    uri = '/mgmt/v1.2/rest/login'
    login_info = {'username': str(username), 'password': str(password)}

    # Make the call...

    resp = conninfo.request(method,
                            uri,
                            request_content_type="application/x-www-form-urlencoded",
                            body=login_info,
                            headers=header)
    return resp


# Logout from the Hammerspace environment
#
# Because we are using cookies instead of OAuth, we have to just close the connection and be
# done with it

@request.request
def logout(conninfo: request.Connection):
    """
    Logout from the  Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
    Returns:
        None
    """

    if not conninfo.is_connected():
        raise requests.ConnectionError(NOT_CONNECTED)

    conninfo.close()
