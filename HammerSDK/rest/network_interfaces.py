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
def list_network_interfaces(conninfo: request.Connection) -> Any:
    """
    Get all network interfaces.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: A list of all network interfaces in json format
    """
    method = 'GET'
    uri = '/mgmt/v1.2/rest/network-interfaces'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def resolve_network_interface(conninfo: request.Connection, node: str, if_name: str) -> Any:
    """
    Get a network interface by node and interface name.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        node (str): The name of the node
        if_name (str): The name of the interface

    Returns:
        json object: The specified network interface
    """
    method = 'GET'
    uri = UriBuilder(path='/mgmt/v1.2/rest/network-interfaces/resolve')
    uri.add_query_param('node', node)
    uri.add_query_param('ifName', if_name)
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_network_interface(conninfo: request.Connection, identifier: str) -> Any:
    """
    Get a network interface by its ID.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier (UUID) of the network interface

    Returns:
        json object: The specified network interface
    """
    method = 'GET'
    uri = f'/mgmt/v1.2/rest/network-interfaces/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def create_virtual_network_interface(conninfo: request.Connection, identifier: str, interface_view: Dict[str, Any]) -> Any:
    """
    Create a virtual network interface.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier for the operation
        interface_view (Dict[str, Any]): A dictionary representing the virtual interface to create

    Returns:
        json object: The created virtual network interface
    """
    method = 'POST'
    uri = f'/mgmt/v1.2/rest/network-interfaces/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               uri,
                               body=interface_view,
                               request_content_type='application/json',
                               headers=header)


@request.request
def update_network_interface(conninfo: request.Connection, identifier: str, interface_view: Dict[str, Any]) -> Any:
    """
    Update a network interface by its ID.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the network interface to update
        interface_view (Dict[str, Any]): A dictionary representing the properties to update

    Returns:
        json object: The updated network interface
    """
    method = 'PUT'
    uri = f'/mgmt/v1.2/rest/network-interfaces/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               uri,
                               body=interface_view,
                               request_content_type='application/json',
                               headers=header)


@request.request
def delete_network_interface(conninfo: request.Connection, identifier: str) -> Any:
    """
    Delete a network interface by its ID.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the network interface to delete

    Returns:
        json object: The deleted network interface
    """
    method = 'DELETE'
    uri = f'/mgmt/v1.2/rest/network-interfaces/{identifier}'
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
