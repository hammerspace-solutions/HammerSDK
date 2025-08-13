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
def list_backups(conninfo: request.Connection) -> Any:
    """
    Get Backup configuration.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: Backup configurations in json format
    """
    method = 'GET'
    uri = '/mgmt/v1.2/rest/backup'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def create_backup_schedule(conninfo: request.Connection, backup_view: Dict[str, Any]) -> Any:
    """
    Create a backup schedule.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        backup_view (Dict[str, Any]): A dictionary representing the backup schedule to create

    Returns:
        json object: The created backup schedule
    """
    method = 'POST'
    uri = '/mgmt/v1.2/rest/backup'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               str(uri),
                               body=backup_view,
                               request_content_type='application/json',
                               headers=header)


@request.request
def create_immediate_backup(conninfo: request.Connection, volume_ip: str, export_path: str) -> Any:
    """
    Create an immediate backup.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_ip (str): The IP address of the volume
        export_path (str): The export path for the backup

    Returns:
        json object: Response from the server
    """
    method = 'POST'
    uri = f'/mgmt/v1.2/rest/backup/backup-create/{volume_ip}/{export_path}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def list_all_backups(conninfo: request.Connection, volume_ip: str, export_path: str) -> Any:
    """
    List all backups for a given volume.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_ip (str): The IP address of the volume
        export_path (str): The export path of the volume

    Returns:
        List: A list of backup names
    """
    method = 'GET'
    uri = f'/mgmt/v1.2/rest/backup/backup-list/{volume_ip}/{export_path}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def restore_latest_backup(conninfo: request.Connection,
                          volume_ip: str,
                          export_path: str,
                          cluster_uuid: Optional[str] = None) -> Any:
    """
    Restore the latest backup from a storage volume.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_ip (str): The IP address of the volume
        export_path (str): The export path of the volume
        cluster_uuid (str, optional): The cluster UUID to restore to

    Returns:
        json object: Response from the server
    """
    method = 'POST'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/backup/backup-restore/{volume_ip}/{export_path}')
    header = {'Accept': 'application/json'}

    if cluster_uuid:
        uri.add_query_param('cluster-uuid', cluster_uuid)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def restore_named_backup(conninfo: request.Connection,
                         volume_ip: str,
                         export_path: str,
                         backup_name: str,
                         cluster_uuid: Optional[str] = None) -> Any:
    """
    Restore a specific backup from a storage volume.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        volume_ip (str): The IP address of the volume
        export_path (str): The export path of the volume
        backup_name (str): The name of the backup to restore
        cluster_uuid (str, optional): The cluster UUID to restore to

    Returns:
        json object: Response from the server
    """
    method = 'POST'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/backup/backup-restore/{volume_ip}/{export_path}/{backup_name}')
    header = {'Accept': 'application/json'}

    if cluster_uuid:
        uri.add_query_param('cluster-uuid', cluster_uuid)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def update_backup_schedule(conninfo: request.Connection, identifier: str, backup_view: Dict[str, Any]) -> Any:
    """
    Update a backup schedule.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the backup schedule to update
        backup_view (Dict[str, Any]): A dictionary representing the backup schedule properties to update

    Returns:
        json object: The updated backup schedule
    """
    method = 'PUT'
    uri = f'/mgmt/v1.2/rest/backup/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               uri,
                               body=backup_view,
                               request_content_type='application/json',
                               headers=header)


@request.request
def delete_backup_schedule(conninfo: request.Connection, identifier: str) -> Any:
    """
    Delete a backup schedule.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the backup schedule to delete

    Returns:
        json object: The deleted backup schedule
    """
    method = 'DELETE'
    uri = f'/mgmt/v1.2/rest/backup/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Send a request and process the response
def _request_processing(conninfo: request.Connection, *args, **kwargs):
    response = conninfo.request(*args, **kwargs)

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response
