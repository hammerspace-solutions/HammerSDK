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

# Return all the share snapshots in the Hammerspace environment


@request.request
def list_snapshot_schedules(conninfo: request.Connection) -> Any:
    """
    List all the share snapshot schedules within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: share snapshot schedules in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/share-snapshots'
    header = {'Accept': 'application/json'}

    # Send request to API

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def create_snapshot_schedule(conninfo: request.Connection, schedule_view: Dict[str, Any]) -> Any:
    """
    Create a new share snapshot schedule.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        schedule_view (Dict[str, Any]): A dictionary representing the snapshot schedule to create.

    Returns:
        json object: The created share snapshot schedule.
    """
    method = 'POST'
    uri = '/mgmt/v1.2/rest/share-snapshots'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               uri,
                               body=schedule_view,
                               request_content_type='application/json',
                               headers=header)


@request.request
def update_snapshot_schedule(conninfo: request.Connection, identifier: str, schedule_view: Dict[str, Any]) -> Any:
    """
    Update an existing share snapshot schedule.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The UUID of the snapshot schedule to update.
        schedule_view (Dict[str, Any]): A dictionary with the updated properties for the schedule.

    Returns:
        json object: The updated share snapshot schedule.
    """
    method = 'PUT'
    uri = f'/mgmt/v1.2/rest/share-snapshots/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               uri,
                               body=schedule_view,
                               request_content_type='application/json',
                               headers=header)


# Delete one particular share snapshot from the Hammerspace environment

@request.request
def delete_snapshot_schedule(conninfo: request.Connection, snapshot_id: str,
                             clear_snapshots: Optional[bool] = False):
    """
    Delete a specific share snapshot schedule from a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        snapshot_id (str): The uuid of the share snapshot schedule
        clear_snapshots (bool, optional): If True, delete all the snapshots for this share schedule

    Returns:
        None

    Examples:
        from HammerSDK.hammer_client import HammerClient

        # Without deleting all the snapshots

        self.hammer_connection = HammerClient(self.host, self.port)
        self.hammer_connection.rest.delete_share_snapshot(snapshot_id="abcdefghijklmnopqrst")

        # Deleting all the share snapshots

        self.hammer_connection.rest.delete_share_snapshot(snapshot_id="abcdefghijklmnopqrst", clear_snapshots=True)
    """

    method = 'DELETE'
    header = {'Accept': 'application/json'}

    uri = UriBuilder(path=f'/mgmt/v1.2/rest/share-snapshots/{snapshot_id}')

    # Add clear_snapshot

    clear_snaps = True if clear_snapshots else False

    uri.add_query_param('clear-snapshots', clear_snaps)

    # Send request to API

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get list of snapshots for a particular share in the Hammerspace environment

@request.request
def get_snapshot_list(conninfo: request.Connection, share_id: str) -> Any:
    """
    Get all the snapshots for a specific share within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_id (str): The uuid of the share

    Returns:
        List: Iterable list of snapshots taken for a particular share
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/share-snapshots/snapshot-list/{share_id}'
    header = {'Accept': 'application/json'}

    # Send request to API

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def create_immediate_snapshot(conninfo: request.Connection, share_identifier: str, snapshot_name: Optional[str] = None) -> Any:
    """
    Create an immediate share snapshot.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_identifier (str): The identifier (UUID) of the share.
        snapshot_name (str, optional): The name for the snapshot.

    Returns:
        json object: Response containing the snapshot name.
    """
    method = 'POST'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/share-snapshots/snapshot-create/{share_identifier}')
    header = {'Accept': 'application/json'}

    if snapshot_name:
        uri.add_query_param('snapshot-name', snapshot_name)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def delete_snapshot(conninfo: request.Connection, share_identifier: str, snapshot_name: str) -> Any:
    """
    Delete a specific share snapshot.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_identifier (str): The identifier (UUID) of the share.
        snapshot_name (str): The name of the snapshot to delete.

    Returns:
        json object: Command result view.
    """
    method = 'POST'
    uri = f'/mgmt/v1.2/rest/share-snapshots/snapshot-delete/{share_identifier}/{snapshot_name}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def clone_snapshot(conninfo: request.Connection,
                     share_identifier: str,
                     snapshot_name: str,
                     destination_path: str,
                     overwrite_destination: Optional[bool] = False) -> Any:
    """
    Clone a share snapshot to a new destination.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_identifier (str): The identifier (UUID) of the share.
        snapshot_name (str): The name of the snapshot to clone.
        destination_path (str): The destination path for the clone.
        overwrite_destination (bool, optional): Overwrite if the destination path exists. Defaults to False.

    Returns:
        Response object from the server, typically a 202 Accepted response.
    """
    method = 'POST'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/share-snapshots/clone-create/{share_identifier}')
    header = {'Accept': 'application/json'}

    uri.add_query_param('snapshot-name', snapshot_name)
    uri.add_query_param('destination-path', destination_path)
    if overwrite_destination:
        uri.add_query_param('overwrite-destination', 'true')

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def restore_share_from_snapshot(conninfo: request.Connection, share_identifier: str, snapshot_name: str) -> Any:
    """
    Restore an entire share from a snapshot.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_identifier (str): The identifier (UUID) of the share to restore.
        snapshot_name (str): The name of the snapshot to restore from.

    Returns:
        Response object from the server, typically a 202 Accepted response.
    """
    method = 'POST'
    uri = f'/mgmt/v1.2/rest/share-snapshots/snapshot-restore/{share_identifier}/{snapshot_name}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def restore_files_from_snapshot(conninfo: request.Connection,
                                share_identifier: str,
                                snapshot_name: str,
                                filename: str) -> Any:
    """
    Restore specific files from a share snapshot.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share_identifier (str): The identifier (UUID) of the share.
        snapshot_name (str): The name of the snapshot to restore from.
        filename (str): The path to the file or directory to restore within the snapshot.

    Returns:
        json object: Command result view.
    """
    method = 'POST'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/share-snapshots/snapshot-restore-files/{share_identifier}/{snapshot_name}')
    header = {'Accept': 'application/json'}

    uri.add_query_param('filename', filename)

    return _request_processing(conninfo, method, str(uri), headers=header)


# Send a request and process the response. We have this routine because about 90%
# of the functions for share snapshot processing have the same code

def _request_processing(conninfo: request.Connection, *args, **kwargs):

    response = conninfo.request(*args, **kwargs)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response
