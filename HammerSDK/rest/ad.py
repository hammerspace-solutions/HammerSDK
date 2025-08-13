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


# Get AD configuration

@request.request
def get_ad_configuration(conninfo: request.Connection,
                         include_discovery_info: Optional[bool] = False) -> Any:
    """
    Get AD configuration.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        include_discovery_info (bool, optional): When true, populates the discoveryInfo field with information about the realm

    Returns:
        json object: AD configuration
    """

    method = 'GET'
    uri = UriBuilder(path='/mgmt/v1.2/rest/ad')
    header = {'Accept': 'application/json'}

    if include_discovery_info:
        uri.add_query_param('includeDiscoveryInfo', 'true')

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get discovered realm information

@request.request
def discover_realm(conninfo: request.Connection,
                   domain: str,
                   include_server_time: Optional[bool] = False) -> Any:
    """
    Get discovered realm information.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        domain (str): The domain to discover
        include_server_time (bool, optional): When true, populates the serverTime field for each domain controller

    Returns:
        json object: Discovered realm information
    """

    method = 'GET'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/ad/discover/{domain}')
    header = {'Accept': 'application/json'}

    if include_server_time:
        uri.add_query_param('includeServerTime', 'true')

    return _request_processing(conninfo, method, str(uri), headers=header)


# Flush AD cache

@request.request
def flush_ad_cache(conninfo: request.Connection) -> Any:
    """
    Flush AD cache.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        json object: Response from the server
    """

    method = 'POST'
    uri = '/mgmt/v1.2/rest/ad/flush_cache'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, uri, headers=header)


# Get a specific AD configuration by ID

@request.request
def get_ad_by_id(conninfo: request.Connection,
                 identifier: str,
                 include_discovery_info: Optional[bool] = False) -> Any:
    """
    Get an AD by ID.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the AD configuration
        include_discovery_info (bool, optional): When true, populates the discoveryInfo field with information about the realm

    Returns:
        json object: AD configuration
    """

    method = 'GET'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/ad/{identifier}')
    header = {'Accept': 'application/json'}

    if include_discovery_info:
        uri.add_query_param('includeDiscoveryInfo', 'true')

    return _request_processing(conninfo, method, str(uri), headers=header)


# Update AD configuration

@request.request
def update_ad(conninfo: request.Connection,
            identifier: str,
            ad_view: Dict[str, Any]) -> Any:
    """
    Configure AD.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the AD configuration
        ad_view (Dict[str, Any]): A dictionary representing the AD properties to update

    Returns:
        json object: Updated AD configuration
    """

    method = 'PUT'
    uri = f'/mgmt/v1.2/rest/ad/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo,
                               method,
                               uri,
                               body=ad_view,
                               request_content_type='application/json',
                               headers=header)


# Send a request and process the response

def _request_processing(conninfo: request.Connection, *args, **kwargs):

    response = conninfo.request(*args, **kwargs)

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response
