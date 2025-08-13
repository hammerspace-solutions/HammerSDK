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
def list_cluster_info(conninfo: request.Connection) -> Any:
    """
    Get cluster info.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: A list of cluster information objects
    """
    method = 'GET'
    uri = '/mgmt/v1.2/rest/cntl'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def accept_eula(conninfo: request.Connection) -> Any:
    """
    Accept the End User License Agreement (EULA).

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        Response object from the server
    """
    method = 'POST'
    uri = '/mgmt/v1.2/rest/cntl/accept-eula'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def shutdown_cluster(conninfo: request.Connection,
                     poweroff: Optional[bool] = False,
                     reboot: Optional[bool] = False,
                     reason: Optional[str] = None) -> Any:
    """
    Shutdown or reboot the cluster.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        poweroff (bool, optional): Power off the system. Defaults to False.
        reboot (bool, optional): Reboot the system. Defaults to False.
        reason (str, optional): A reason for the shutdown or reboot.

    Returns:
        Response object from the server, typically a 202 Accepted response.
    """
    method = 'POST'
    uri = UriBuilder(path='/mgmt/v1.2/rest/cntl/shutdown')
    header = {'Accept': 'application/json'}

    if poweroff:
        uri.add_query_param('poweroff', 'true')
    if reboot:
        uri.add_query_param('reboot', 'true')
    if reason:
        uri.add_query_param('reason', reason)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_cluster_state(conninfo: request.Connection) -> Any:
    """
    Get the current state of the cluster.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        json object: The cluster state information
    """
    method = 'GET'
    uri = '/mgmt/v1.2/rest/cntl/state'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_cluster_info(conninfo: request.Connection, identifier: str) -> Any:
    """
    Get cluster info for a specific cluster.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the cluster

    Returns:
        json object: The cluster information
    """
    method = 'GET'
    uri = f'/mgmt/v1.2/rest/cntl/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def update_cluster(conninfo: request.Connection, identifier: str, cluster_view: Dict[str, Any]) -> Any:
    """
    Update cluster configuration.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the cluster to update
        cluster_view (Dict[str, Any]): A dictionary representing the cluster properties to update

    Returns:
        json object: The updated cluster information
    """
    method = 'PUT'
    uri = f'/mgmt/v1.2/rest/cntl/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               uri,
                               body=cluster_view,
                               request_content_type='application/json',
                               headers=header)


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
