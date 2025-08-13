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

from typing import Any, Optional, Iterable, List

# SDK Version                                                                                  
SDK_Version = "5.1.18"


# Create a share in the Hammerspace environment

@request.request
def create_share(conninfo: request.Connection,
                 name: str,
                 path: str,
                 comment: Optional[str] = None,
                 size_limit: Optional[int] = None,
                 warning_threshold: Optional[int] = None,
                 create_path: Optional[bool] = True,
                 volume_id: Optional[List[str]] = None,
                 volume_type: Optional[List[str]] = None) -> str:
    """
    Create a share within a Hammerspace environment. Note that this routine does not
    return until the share has been completely created. This operation occurs in the
    background and can take some time (multiple seconds).

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        name (str): Name of the share
        path (str): Path of the share within the environment
        comment (str, optional): Optional comment on the new share
        size_limit (int, optional): Optional size limit for share (in bytes)
        warning_threshold (int, optional): Optional percentage for a warning (from 0 to 100)
        create_path (bool, optional): If False, do not create the path in the infrastructure
        volume_id (Iterable[str], optional): An array of volume UUID's
        volume_type (Iterable[str], optional): An array of volume type's

    Returns:
        str: share id

    Examples:

        | Simple example on how to create a share

        | from HammerSDK.hammer_client import HammerClient
        | self.hammer_connection = HammerClient(self.host, self.port)
        | share_id = self.hammer_connection.shares.create_share(
        |      name="Graphics",
        |      path="/xyz/Graphics",
        |      comment="XYZ Graphics",
        |      size_limit=1000000,
        |      warning_threshold=70,
        |      create_path=False,
        |      volume_id=["f7840083-3e1a-44f4-b067-db07c9e8241a"],
        |      volume_type=["STORAGE_VOLUME"])

    """

    method = 'POST'
    header = {'accept': 'application/json'}

    uri = UriBuilder(path='/mgmt/v1.2/rest/shares')

    # Add create_path

    uri.add_query_param('create-path', create_path)

    # Create the body

    create_share_request = {
        "name": name,
        "path": path,
        "comment": comment if comment is not None else "",
        "shareSizeLimit": size_limit if size_limit is not None else "",
        "warnUtilizationPercentThreshold": warning_threshold if warning_threshold is not None else "",
    }

    # Validate volume_id and volume_type

    if volume_id is not None:
        _check_list_type(volume_id, "volume_id")
        _check_list_type(volume_type, "volume_type")
        _check_same_len(volume_id, volume_type)
        create_share_request['volumes'] = [{"uoid": {"uuid": volume_id[volid], "objectType": volume_type[volid]}} for
                                           volid in range(len(volume_id))]

    # Send the request to the API

    response = conninfo.request(method, str(uri),
                                body=create_share_request,
                                headers=header,
                                request_content_type='application/json')

    # Only return the json structure if there is one to return.

    return _parse_response(response)


# Verify that they passed in a List

def _check_list_type(v: Iterable[str], name: str):
    if not isinstance(v, List):
        raise ValueError(f"{name} is not of a List type")


# Verify that we have a volume_id for every volume_type

def _check_same_len(volume_id: List[str], volume_type: List[str]):
    if len(volume_id) != len(volume_type):
        raise ValueError("There must be a volume_type for each volume_id")


# Parse the response from the API

def _parse_response(response):
    if response.text:
        shares_info = response.json()
        ctxmap = shares_info["ctxMap"]["entity-uoid"]
        id_start = ctxmap.index("=") + 1
        id_end = ctxmap.index(",")
        share_id = ctxmap[id_start:id_end]
        return share_id
    else:
        return response


# Send a request and process the response. We have this routine because about 90%
# of the functions for share processing have the same code

def _request_processing(conninfo: request.Connection, *args, **kwargs):

    response = conninfo.request(*args, **kwargs)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response


# Return all the shares in the Hammerspace environment

@request.request
def list_shares(conninfo: request.Connection) -> Any:
    """
    List all the shares within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: shares in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/shares'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Return all the UUIDs related to shares in the Hammerspace environment

@request.request
def list_uuids_for_shares(conninfo: request.Connection) -> Any:
    """
    List all the uuids for the shares within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: uuids in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/shares/uuid-list'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get all the mounts for one particular share from the Hammerspace environment

@request.request
def get_mounts_for_share(conninfo: request.Connection, share_id: str) -> Any:
    """
    List all the mounts for a given share within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): Share UUID

    Returns:
        json object: Mount info for a particular share
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/shares/{share_id}/mount-details'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get all the objectives for one particular share from the Hammerspace environment

@request.request
def get_objectives_for_share(conninfo: request.Connection, share_id: str) -> Any:
    """
    List all the objectives for a given share within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): The uuid of the share

    Returns:
        json object: Objectives info for a particular share
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/shares/{share_id}/objective-list'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get one particular share from the Hammerspace environment

@request.request
def get_share(conninfo: request.Connection, share_id: str) -> Any:
    """
    Get a specific share within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): The uuid of the share

    Returns:
        json object: single share
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/shares/{share_id}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Delete one particular share from the Hammerspace environment

@request.request
def delete_share(conninfo: request.Connection, share_id: str,
                 delete_delay: Optional[int] = 0,
                 delete_path: Optional[bool] = True) -> Any:
    """
    Delete a specific share from a Hammerspace environment. Note that this routine will not return until the share
    is deleted. If, however, the delete_delay is greater than 0, then this routine will return even though the
    share has probably not been deleted yet as the operation occurs in the background and can take some time.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): The uuid of the share
        delete_delay (int, optional): Delay in seconds before deleting the share. 0 is immediate.
        delete_path (bool, optional): If True, delete the contents of the share

    Returns:
        None

    Examples:

        | Simple example on how to delete a share
        |
        | from HammerSDK.hammer_client import HammerClient
        |
        | # With default 'delete_delay' and 'delete_path'
        |
        | self.hammer_connection = HammerClient(self.host, self.hport)
        | self.hammer_connection.shares.delete_share(share_id="abcdefghijklmnopqrst")
        |
        | # With specific 'delete_delay' and 'delete_path'
        |
        | self.hammer_connection.shares.delete_share(
        |    share_id="abcdefghijklmnopqrst",
        |    delete_delay=0,
        |    delete_path=False)
    """

    method = 'DELETE'
    header = {'Accept': 'application/json'}

    uri = UriBuilder(path=f'/mgmt/v1.2/rest/shares/{share_id}')

    # Add delete delay and delete_path

    uri.add_query_param('delete_delay', delete_delay)
    uri.add_query_param('delete_path', delete_path)

    # If they don't want to delete the share for a while, then we won't wait

    delay = True if delete_delay > 0 else False

    # Send request to API

    return _request_processing(conninfo, method, str(uri), headers=header, no_delay=delay)


# Un-delete one particular share from the Hammerspace environment

@request.request
def undelete_share(conninfo: request.Connection, share_id: str) -> Any:
    """
    Undelete a specific share from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): The uuid of the share

    Returns:
        None
    """

    method = 'POST'
    uri = f'/mgmt/v1.2/rest/shares/{share_id}/undelete'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Set an Objective on one particular share from the Hammerspace environment

@request.request
def set_objective(conninfo: request.Connection,
                  share_id: str,
                  objective: str,
                  path: Optional[str] = None,
                  applicability: Optional[str] = None) -> Any:

    """
    Set an Objective on a specific share from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): The uuid of the share
        objective (str): The name of the objective
        path (str, optional): Optional path offset within the share
        applicability (str, optional): Optional string specifying applicability

    Returns:
        json object: Objectives info for share

    Examples:

        | Simple example on how to set an objective on a share
        |
        | from HammerSDK.hammer_client import HammerClient
        |
        | # With no applicability set
        |
        | self.hammer_connection = HammerClient(self.host, self.hport)
        | self.hammer_connection.shares.set_objective(
        |     share_id="abcdefghijklmnopqrst", objective="keep-online")
        |
        | # Set a valid applicability
        |
        | self.hammer_connection.shares.set_objective(
        |    share_id="abcdefghijklmnopqrst", objective'keep-online", applicability="True")
    """

    method = 'POST'
    header = {'Accept': 'application/json'}

    uri = UriBuilder(path=f'/mgmt/v1.2/rest/shares/{share_id}/objective-set')

    # Add the objective

    uri.add_query_param('objective-identifier', objective)

    # If the path is set, then add it too

    if path is not None:
        uri.add_query_param('path', path)

    # If the applicability is set, then add it to the URI

    if applicability is not None:
        uri.add_query_param('applicability', applicability)

    # Send the request to the API

    return _request_processing(conninfo, method, str(uri), headers=header)


# Set an Objective on one particular share from the Hammerspace environment

@request.request
def update_objective(conninfo: request.Connection,
                     share_id: str,
                     objective: str,
                     applicability: str,
                     new_applicability: str,
                     path: Optional[str] = None):

    """
    Set an Objective on a specific share from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): The uuid of the share
        objective (str): The name of the objective
        applicability (str): The old applicability string for this objective
        new_applicability (str): The new applicability string for this objective
        path (str, optional): Optional path offset within the share

    Returns:
        json object: Objectives info for share

    Examples:

        | Simple example on how to update an objective on a share
        |
        | from HammerSDK.hammer_client import HammerClient
        |
        | self.hammer_connection = HammerClient(self.host, self.hport)
        | self.hammer_connection.shares.update_objective(
        |     share_id="abcdefghijklmnopqrst", objective="keep-online",
        |     applicability="True", new_applicability="Always)

    """

    method = 'POST'
    header = {'Accept': 'application/json'}

    uri = UriBuilder(path=f'/mgmt/v1.2/rest/shares/{share_id}/objective-update')

    # Add the objective

    uri.add_query_param('objective-identifier', objective)

    # If the path is set, then add it too

    if path is not None:
        uri.add_query_param('path', path)

    # Set the applicability and new_applicability

    uri.add_query_param('applicability', applicability)
    uri.add_query_param('new-applicability', new_applicability)

    # Send the request to the API

    return _request_processing(conninfo, method, str(uri), headers=header)


# "Unset"" an Objective on one particular share from the Hammerspace environment

@request.request
def unset_objective(conninfo: request.Connection,
                    share_id: str,
                    objective: str,
                    path: Optional[str] = None,
                    applicability: Optional[str] = None) -> Any:

    """
    Unset an Objective on a specific share from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): The uuid of the share
        objective (str): The name of the objective
        path (str, optional): Optional path offset within the share
        applicability (str, optional): Optional string specifying applicability

    Returns:
        json object: Objectives info for share
    """

    method = 'POST'
    header = {'Accept': 'application/json'}

    uri = UriBuilder(path=f'/mgmt/v1.2/rest/shares/{share_id}/objective-unset')

    # Add the objective

    uri.add_query_param('objective-identifier', objective)

    # If the path is set, then add it too

    if path is not None:
        uri.add_query_param('path', path)

    # If the applicability is set, then add it to the URI

    if applicability is not None:
        uri.add_query_param('applicability', applicability)

    # Send the request to the API

    return _request_processing(conninfo, method, str(uri), headers=header)
