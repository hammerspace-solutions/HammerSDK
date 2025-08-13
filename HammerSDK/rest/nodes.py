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

from typing import Any, List

# SDK Version                                                                                  
SDK_Version = "5.1.18"


# Return all the nodes in the Hammerspace environment

@request.request
def list_nodes(conninfo: request.Connection) -> Any:
    """
    List all the nodes within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: nodes in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/nodes'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get one particular node from the Hammerspace environment

@request.request
def get_node(conninfo: request.Connection, node_id: str) -> Any:
    """
    Get a specific node from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        node_id (str): The uuid of the node

    Returns:
        json object: single node
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/nodes/{node_id}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Delete one particular node from the Hammerspace environment

@request.request
def delete_node(conninfo: request.Connection, node_id: str) -> Any:
    """
    Delete a specific node from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        node_id (str): The uuid of the node

    Returns:
        json object: single node
    """

    method = 'DELETE'
    uri = f'/mgmt/v1.2/rest/nodes/{node_id}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Send a request and process the response. We have this routine because about 90%
# of the functions for node processing have the same code

def _request_processing(conninfo: request.Connection, *args, **kwargs):

    response = conninfo.request(*args, **kwargs)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if response.text:
        return _sanitize_json(response.json())
    else:
        return response


# Sanitize the json returned so that it doesn't contain LOTS and LOTS of duplicates

def _sanitize_json(json_info):

    nodes_info = []

    if not isinstance(json_info, List):
        return json.loads(json.dumps(_sanitize_json_item(json_info), sort_keys=True))

    for json_item in range(len(json_info)):
        nodes_info.append(_sanitize_json_item(json_info[json_item]))

    return json.loads(json.dumps(nodes_info, sort_keys=True))


# Sanitize a single json item to remove all the duplicates

def _sanitize_json_item(json_info):

    gateway_info = json_info.get("gateway")
    if gateway_info and gateway_info.get("node"):
        del json_info["gateway"]["node"]

    location_info = json_info.get("location")
    if location_info and location_info.get("node"):
        del json_info["location"]["node"]

    if json_info.get("platformServices"):
        for service in range(len(json_info["platformServices"])):
            if json_info["platformServices"][service].get("node"):
                del json_info["platformServices"][service]["node"]

    if json_info.get("systemServices"):
        for service in range(len(json_info["systemServices"])):
            if json_info["systemServices"][service].get("node"):
                del json_info["systemServices"][service]["node"]

    return json_info
