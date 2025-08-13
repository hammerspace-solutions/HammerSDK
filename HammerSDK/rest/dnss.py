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
def list_dns_configs(conninfo: request.Connection) -> Any:
    """
    Get DNS configuration.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: A list of DNS configurations in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/dnss'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_dns_config(conninfo: request.Connection, identifier: str) -> Any:
    """
    Get a specific DNS configuration by its ID.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier (UUID) of the DNS configuration

    Returns:
        json object: The specified DNS configuration
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/dnss/{identifier}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def update_dns_config(conninfo: request.Connection,
                        identifier: str,
                        dns_view: Dict[str, Any],
                        force: Optional[bool] = False) -> Any:
    """
    Update a DNS configuration.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        identifier (str): The identifier of the DNS configuration to update
        dns_view (Dict[str, Any]): A dictionary representing the DNS properties to update
        force (bool, optional): Force the update operation. Defaults to False.

    Returns:
        json object: The updated DNS configuration
    """

    method = 'PUT'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/dnss/{identifier}')
    header = {'Accept': 'application/json'}

    if force:
        uri.add_query_param('force', 'true')

    return _request_processing(conninfo,
                               method,
                               str(uri),
                               body=dns_view,
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
