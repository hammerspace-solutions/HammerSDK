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
