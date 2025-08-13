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

from HammerSDK.lib.HammerExceptions import InvalidSDKArgumentsGiven
from HammerSDK.lib.uri import UriBuilder
from typing import Any, Optional, Iterable, Dict, List
from copy import deepcopy

# SDK Version                                                                                  
SDK_Version = "5.1.18"


# Create a volume group in the Hammerspace environment

@request.request
def create_group(conninfo: request.Connection,
                 name: str,
                 comment: Optional[str] = None,
                 node_names: Optional[Iterable[str]] = None,
                 volume_names: Optional[Iterable[str]] = None,
                 volume_group_names: Optional[Iterable[str]] = None) -> Any:
    """
    Create a volume group within the Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        name (str): Name of the volume group
        comment (str, optional): Optional comment on the new volume group
        node_names (Iterable[str], optional): An array of node names
        volume_names (Iterable[str], optional): An array of volume names
        volume_group_names (Iterable[str], optional): An array of volume group names

    Returns:node_id
        json object: volume group

    Examples:

        | Simple example on how to create a volume group

        | from HammerSDK.hammer_client import HammerClient
        | self.hammer_connection = HammerClient(self.host, self.port)
        | volume_info = self.hammer_connection.volume_groups.create_group(
        |      name="kade-group",
        |      comment="Test volume group"
        |      volume_names=["dsx-node-1::/hsvol0", "dsx-node-1::/hsvol1",
        |      node_names=["dsx-node-2", "dsx-node-3")
    """

    method = 'POST'
    header = {'Accept': 'application/json'}

    uri = UriBuilder(path='/mgmt/v1.2/rest/volume-groups')

    # Create the body

    group_body = {
        "name": name,
        "_type": "VOLUME_GROUP",
        "expressions": []
    }

    expressions_body = {
        "operator": "IN",
        "locations": []
    }

    node_body = {
        "_type": "NODE_LOCATION",
        "node": {
            "_type": "NODE",
            "name": ""
        }
    }

    volume_body = {
        "_type": "VOLUME_LOCATION",
        "storageVolume": {
            "_type": "STORAGE_VOLUME",
            "name": ""
        }
    }

    volume_group_body = {
        "_type": "VOLUME_GROUP",
        "name": ""
    }

    # Add the comment if it exists

    if comment is not None:
        group_body["comment"] = comment

    # If there are no arguments, then raise an error

    if not volume_names and not node_names and not volume_group_names:
        raise InvalidSDKArgumentsGiven("No arguments given to volume group create")

    # If there are volumes named, then build the structure

    if volume_names is not None:
        expressions_body["locations"].extend(_build_locations(volume_body, volume_body["storageVolume"], volume_names))

    # If there are nodes name, then build the structure

    if node_names is not None:
        expressions_body["locations"].extend(_build_locations(node_body, node_body["node"], node_names))

    # If there are volume_groups, then build the structure

    if volume_group_names is not None:
        expressions_body["locations"].extend(_build_locations(volume_group_body, volume_group_body, volume_group_names))

    # Now that we have built the expressions, add them to the body of the message

    group_body["expressions"].append(expressions_body)
    group_info = json.dumps(group_body, sort_keys=True, indent=4)

    # Send the request to the API

    return _request_processing(conninfo, method, str(uri), headers=header,
                               body=group_body, request_content_type='application/json')


# Return all the volume groups in the Hammerspace environment

@request.request
def list_groups(conninfo: request.Connection) -> Any:
    """
    List all the volume groups within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: volume groups in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/volume-groups'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get one particular storage volume from the Hammerspace environment

@request.request
def get_group(conninfo: request.Connection, volume_group_id: str) -> Any:
    """
    Get a specific volume group from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_group_id (str): The uuid of the volume group
    Returns:
        json object: volume group
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/volume-groups/{volume_group_id}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Delete one particular storage volume from the Hammerspace environment

@request.request
def delete_group(conninfo: request.Connection, volume_group_id: str) -> Any:
    """
    Delete a specific volume group from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_group_id (str): The uuid of the volume group

    Returns:
        json object: storage volume
    """

    method = 'DELETE'
    uri = f'/mgmt/v1.2/rest/volume-groups/{volume_group_id}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Send a request and process the response. We have this routine because about
# 90% of the functions for volume group processing have the same code

def _request_processing(conninfo: request.Connection, *args, **kwargs):

    response = conninfo.request(*args, **kwargs)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response


# Build locations dictionary

def _build_locations(template_form: Dict[str, Any],
                     template: Dict[str, Any],
                     names: Iterable[str]) -> List[Dict[str, Any]]:

    locations = []

    for name in names:
        template["name"] = name
        locations.append(deepcopy(template_form))

    return locations
