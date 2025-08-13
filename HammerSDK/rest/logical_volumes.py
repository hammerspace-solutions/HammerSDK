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

from typing import Any

# SDK Version                                                                                  
SDK_Version = "5.1.18"


# Return all the logical volumes in the Hammerspace environment

@request.request
def list_logical_volumes(conninfo: request.Connection) -> Any:
    """
    List all the logical volumes within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: logical volumes in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/logical-volumes'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get one particular logical volume from the Hammerspace environment

@request.request
def get_logical_volume(conninfo: request.Connection, volume_id: str) -> Any:
    """
    Get a specific logical volume from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_id (str): The uuid of the logical volume

    Returns:
        json object: single logical volume
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/logical-volumes/{volume_id}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Delete one particular logical volume from the Hammerspace environment

@request.request
def delete_logical_volume(conninfo: request.Connection, volume_id: str) -> Any:
    """
    Delete a specific logical volume from within a Hammerspace environment.


    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_id (str): The uuid of the logical volume

    Returns:
        json object: single logical volume
    """

    method = 'DELETE'
    uri = f'/mgmt/v1.2/rest/logical-volumes/{volume_id}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Send a request and process the response. We have this routine because about 90% of
# the functions for logical volume processing have the same code

def _request_processing(conninfo: request.Connection, *args, **kwargs):

    response = conninfo.request(*args, **kwargs)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response
