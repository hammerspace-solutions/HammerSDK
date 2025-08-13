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


import HammerSDK.lib.request as request
import json

from HammerSDK.lib.uri import UriBuilder
from typing import Any, Optional

# SDK Version
SDK_Version = "5.1.18"


@request.request
def list_volumes(conninfo: request.Connection) -> Any:
    """
    Get all volumes (File and Object).

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: A list of all storage volumes in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/base-storage-volumes'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_volume(conninfo: request.Connection, identifier: str) -> Any:
    """
    Get a specific volume by its ID.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier (UUID) of the volume

    Returns:
        json object: The specified volume
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/base-storage-volumes/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Send a request and process the response
def _request_processing(conninfo: request.Connection, *args, **kwargs):
    """
    Internal function to handle API requests and process responses.
    """
    response = conninfo.request(*args, **kwargs)

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response
