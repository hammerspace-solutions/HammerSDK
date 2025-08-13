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
from typing import Any, Optional, Dict

# SDK Version
SDK_Version = "5.1.18"


@request.request
def list_file_snapshots(conninfo: request.Connection) -> Any:
    """
    List all file snapshots.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: A list of all file snapshots in json format
    """
    method = 'GET'
    uri = '/mgmt/v1.2/rest/file-snapshots'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def create_file_snapshot_schedule(conninfo: request.Connection, file_snapshot_view: Dict[str, Any]) -> Any:
    """
    Create a file snapshot schedule.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        file_snapshot_view (Dict[str, Any]): A dictionary representing the file snapshot schedule to create

    Returns:
        json object: The created file snapshot schedule
    """
    method = 'POST'
    uri = '/mgmt/v1.2/rest/file-snapshots'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               str(uri),
                               body=file_snapshot_view,
                               request_content_type='application/json',
                               headers=header)


@request.request
def create_file_snapshot(conninfo: request.Connection, filename_expression: str) -> Any:
    """
    Create an immediate file snapshot.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        filename_expression (str): The file expression to snapshot

    Returns:
        Response object from the server
    """
    method = 'POST'
    uri = UriBuilder(path='/mgmt/v1.2/rest/file-snapshots/create')
    uri.add_query_param('filename-expression', filename_expression)
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def delete_file_snapshot(conninfo: request.Connection, filename_expression: str, date_time_expression: str) -> Any:
    """
    Delete a file snapshot.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        filename_expression (str): The file expression of the snapshot to delete
        date_time_expression (str): The date-time expression of the snapshot to delete

    Returns:
        json object: Command result view
    """
    method = 'POST'
    uri = UriBuilder(path='/mgmt/v1.2/rest/file-snapshots/delete')
    uri.add_query_param('filename-expression', filename_expression)
    uri.add_query_param('date-time-expression', date_time_expression)
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def list_snapshots_for_file(conninfo: request.Connection, filename_expression: str) -> Any:
    """
    Get all file snapshots for a specific file expression.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        filename_expression (str): The file expression to list snapshots for

    Returns:
        List: A list of file stat views for the snapshots
    """
    method = 'GET'
    uri = UriBuilder(path='/mgmt/v1.2/rest/file-snapshots/list')
    uri.add_query_param('filename-expression', filename_expression)
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def restore_file_from_snapshot(conninfo: request.Connection, filename_expression: str, date_time_expression: str) -> Any:
    """
    Restore a file from a snapshot.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        filename_expression (str): The file expression to restore
        date_time_expression (str): The date-time expression of the snapshot to restore from

    Returns:
        json object: Command result view
    """
    method = 'POST'
    uri = UriBuilder(path='/mgmt/v1.2/rest/file-snapshots/restore')
    uri.add_query_param('filename-expression', filename_expression)
    uri.add_query_param('date-time-expression', date_time_expression)
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def clone_file_snapshot(conninfo: request.Connection, file_source: str, file_destination: str) -> Any:
    """
    Clone a file from a snapshot.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        file_source (str): The source file path in the snapshot
        file_destination (str): The destination path for the cloned file

    Returns:
        Response object from the server
    """
    method = 'POST'
    uri = f'/mgmt/v1.2/rest/file-snapshots/{file_source}/{file_destination}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_file_snapshot(conninfo: request.Connection, identifier: str) -> Any:
    """
    Get a file snapshot schedule by its ID.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier (UUID) of the file snapshot schedule

    Returns:
        json object: The specified file snapshot schedule
    """
    method = 'GET'
    uri = f'/mgmt/v1.2/rest/file-snapshots/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def update_file_snapshot(conninfo: request.Connection, identifier: str, file_snapshot_view: Dict[str, Any]) -> Any:
    """
    Update a file snapshot schedule.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the file snapshot schedule to update
        file_snapshot_view (Dict[str, Any]): A dictionary representing the properties to update

    Returns:
        json object: The updated file snapshot schedule
    """
    method = 'PUT'
    uri = f'/mgmt/v1.2/rest/file-snapshots/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               uri,
                               body=file_snapshot_view,
                               request_content_type='application/json',
                               headers=header)


@request.request
def delete_file_snapshot_schedule(conninfo: request.Connection, identifier: str) -> Any:
    """
    Delete a file snapshot schedule.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the file snapshot schedule to delete

    Returns:
        json object: The deleted file snapshot schedule
    """
    method = 'DELETE'
    uri = f'/mgmt/v1.2/rest/file-snapshots/{identifier}'
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
