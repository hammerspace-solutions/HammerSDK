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
import requests

from HammerSDK.lib.HammerExceptions import (VolumeNotDecommissioned,
                                            VolumeDecommissioning,
                                            VolumeWasUsed)
from HammerSDK.lib.uri import UriBuilder
from typing import Any, Optional

VOLUME_IN_USE_ERROR = 4052

# SDK Version                                                                                  
SDK_Version = "5.1.18"


# Create a storage volume in the Hammerspace environment

@request.request
def create_volume(conninfo: request.Connection,
                  name: str,
                  logical_volume_name: str,
                  node_name: str,
                  comment: Optional[str] = None,
                  read_write: Optional[bool] = True,
                  force: Optional[bool] = True) -> Any:
    """
    Create a volume within the Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        name (str): Name of the volume
        logical_volume_name (str): Name of the logical volume that you want to add
        node_name (str): Name of the node to add the logical volume to (thus creating the storage volume)
        comment (str, optional): Optional comment on the new volume
        read_write (bool, optional): Should the volume be added as read/write (default: True)
        force (bool, optional): If the volume was previously used, should it be forced added (default: True)

    Returns:
        json object: storage volume

    Examples:

        | Simple example on how to create a volume

        | from HammerSDK.hammer_client import HammerClient
        | self.hammer_connection = HammerClient(self.host, self.port)
        | volume_info = self.hammer_connection.storage_volume.create_volume(
        |      name="kade-dsx-1.selab.hammer.space::/hsvol0",
        |      logical_volume_name="/hsvol0",
        |      node_name="kade-dsx-1.selab.hammer.space",
        |      comment="HSVOL0 volume on dsx-1")
    """

    method = 'POST'
    header = {'accept': 'application/json'}

    uri = UriBuilder(path='/mgmt/v1.2/rest/storage-volumes')
    uri.add_query_param('force', bool(force))

    # Create the body

    create_volume_body = {
        "name": name,
        "logicalVolume": {"name": logical_volume_name, "_type": "LOGICAL_VOLUME"},
        "node": {"name": node_name, "_type": "NODE"},
        "_type": "STORAGE_VOLUME",
        "accessType": "READ_WRITE" if read_write else "READ_ONLY"
    }

    # Add the comment if it exists

    if comment is not None:
        create_volume_body["comment"] = comment

    # Send the request to the API

    try:
        response = conninfo.request(method,
                                    str(uri),
                                    body=create_volume_body,
                                    headers=header,
                                    request_content_type='application/json')
    except requests.exceptions.RequestException as req_exc:
        error_message = bytes(req_exc.response.content)
        error_code = json.loads(error_message)[0].get('errorCode', None)
        if error_code == VOLUME_IN_USE_ERROR:
            raise VolumeWasUsed(logical_volume_name, str(error_message))
        else:
            raise

    # Only return the json structure if there is one to return.

    if len(response.text) > 0:
        return json.loads(json.dumps(response.json(), sort_keys=True, indent=4))

    return response


# Return all the storage volumes in the Hammerspace environment

@request.request
def list_storage_volumes(conninfo: request.Connection) -> Any:
    """
    List all the storage volumes within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: storage volumes in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/storage-volumes'
    header = {'accept': 'application/json'}

    response = conninfo.request(method, uri, headers=header)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if len(response.text) > 0:
        return json.loads(json.dumps(response.json(), sort_keys=True, indent=4))

    return response


# Get one particular storage volume from the Hammerspace environment

@request.request
def get_storage_volume(conninfo: request.Connection, volume_id: str) -> Any:
    """
    Get a specific storage volume from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_id (str): The uuid of the storage volume
    Returns:
        json object: storage volume
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/storage-volumes/{volume_id}'
    header = {'accept': 'application/json'}

    response = conninfo.request(method, uri, headers=header)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if len(response.text) > 0:
        return json.loads(json.dumps(response.json(), sort_keys=True, indent=4))

    return response


# Delete one particular storage volume from the Hammerspace environment

@request.request
def delete_storage_volume(conninfo: request.Connection, volume_id: str) -> Any:
    """
    Delete a specific storage volume from within a Hammerspace environment. Delete must be preceded
    by a called to decommission the volume. If this step is omitted, then an exception will be raised
    until the decommissioning has completed.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_id (str): The uuid of the storage volume

    Returns:
        json object: storage volume

    Raises:
        VolumeNotDecommissioned: Thrown if volume has not been decommissioned before deletion attempt
        VolumeDecommissioning: Thrown if volume is currently being decommissioned
    """

    # The volume must be decommissioned before we can delete.

    get_volume = get_storage_volume(conninfo, volume_id)

    # If the volume is being decommissioned, then raise an exception

    if get_volume["storageVolumeState"] == "DECOMMISSIONING" or \
            get_volume["storageVolumeState"] == "DECOMMISSIONING_QUIESCED":
        raise VolumeDecommissioning(get_volume["name"])

    # Make sure that we set the state to signify that we are decommissioning this volume

    if get_volume["storageVolumeState"] != "DECOMMISSIONED":
        raise VolumeNotDecommissioned(get_volume["name"])

    method = 'DELETE'
    uri = f'/mgmt/v1.2/rest/storage-volumes/{volume_id}'
    header = {'accept': 'application/json'}

    response = conninfo.request(method, uri, headers=header)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if len(response.text) > 0:
        return json.loads(json.dumps(response.json(), sort_keys=True, indent=4))

    return response


# Decommission one particular storage volume from the Hammerspace environment

@request.request
def decommission_storage_volume(conninfo: request.Connection, volume_id: str) -> Any:
    """
    Decommission a specific storage volume from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_id (str): The uuid of the storage volume

    Returns:
        json object: storage volume

    Raises:
        VolumeDecommissioning: Thrown if volume is currently being decommissioned
    """

    # Before we can start, verify that the volume exists. Additionally, we need the returned structure
    # as we need to return almost all of its components to the request

    get_volume = get_storage_volume(conninfo, volume_id)

    # If the volume is being decommissioned, then raise an exception

    if get_volume["storageVolumeState"] == "DECOMMISSIONING" or \
            get_volume["storageVolumeState"] == "DECOMMISSIONING_QUIESCED":
        raise VolumeDecommissioning(get_volume["name"])

    # Make sure that we set the state to signify that we are decommissioning this volume

    get_volume["storageVolumeState"] = "DECOMMISSIONING"

    method = 'PUT'
    uri = f'/mgmt/v1.2/rest/storage-volumes/{volume_id}'
    header = {'accept': 'application/json'}

    response = conninfo.request(method,
                                uri,
                                body=get_volume,
                                headers=header,
                                request_content_type="application/json")

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if len(response.text) > 0:
        return json.loads(json.dumps(response.json(), sort_keys=True, indent=4))

    return response
