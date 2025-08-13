# Copyright (c) 2024-2025 Hammerspace, Inc
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


# Create a site in the Hammerspace environment

@request.request
def create_site(conninfo: request.Connection,
                address: str,
                trustclientcert: Optional[bool] = True) -> Any:
    """
    Create a site within a Hammerspace environment. Note that this routine does not
    return until the site has been completely created. This operation occurs in the
    background and can take some time (multiple seconds).

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        address (str): UNC of the site
        trustclientcert (bool): Trust the cert passed by the site

    Returns:
        json: site information

    Examples:

        | Simple example on how to create a site

        | from HammerSDK.hammer_client import HammerClient
        | self.hammer_connection = HammerClient(self.host, self.port)
        | site_info = self.hammer_connection.sites.create_site(
        |      address="192.168.1.1")

    """

    method = 'POST'
    header = {'accept': 'application/json'}

    uri = UriBuilder(path='/mgmt/v1.2/rest/sites')

    # Create the body

    create_sites_request = {
        "address": addressp,
        "trustClientCert": trustclientcert
    }

    # Send the request to the API

    response = conninfo.request(method, str(uri),
                                body=create_sites_request,
                                headers=header,
                                request_content_type='application/json')

    # Only return the json structure if there is one to return.

    return response

# Send a request and process the response. We have this routine because about 90%
# of the functions for sites processing have the same code

def _request_processing(conninfo: request.Connection, *args, **kwargs):

    response = conninfo.request(*args, **kwargs)

    # Only return json structure if there is really data to return. Otherwise, return
    # the entire response structure

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response


# Return all the sites in the Hammerspace environment

@request.request
def list_sites(conninfo: request.Connection) -> Any:
    """
    List all the sites within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: sites in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/sites'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get one particular site from the Hammerspace environment

@request.request
def get_site(conninfo: request.Connection, site_id: str) -> Any:
    """
    Get a specific site within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        site_id (str): The uuid of the site

    Returns:
        json object: single site
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/sites/{site_id}'
    header = {'Accept': 'application/json'}

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get the local site from the Hammerspace environment

@request.request
def get_local_site(conninfo: request.Connection,
                   verify_version: Optional[bool] = True,
                   version: Optional[str] = SDK_Version) -> Any:
    """
    Get the local site from a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        json object: local site
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/sites/local'
    header = {'Accept': 'application/json'}

    # If we are not verifying the version of software running on the Anvil, then
    # just get what they want and leave
    
    if not verify_version:
        return
    else:
        site_info = _request_processing(conninfo, method, str(uri), headers=header)
        cur_version = site_info["swVersion"]["version"]

        # Is the SDK version less than what we expect? Then throw an exception...

        if cur_version < version:
            raise InvalidSDKVersion(version, cur_version)

        return site_info

    
# Delete one particular site from the Hammerspace environment

@request.request
def delete_site(conninfo: request.Connection, site_id: str) -> Any:
    """
    Delete a specific site from a Hammerspace environment. Note that this routine will
    not return until the site is deleted.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        site_id (str): The uuid of the site

    Returns:
        None

    Examples:

        | Simple example on how to delete a site
        |
        | from HammerSDK.hammer_client import HammerClient
        |
        | self.hammer_connection = HammerClient(self.host, self.hport)
        | self.hammer_connection.shares.delete_site(site_id="abcdefghijklmnopqrst")
    """

    method = 'DELETE'
    header = {'Accept': 'application/json'}

    uri = UriBuilder(path=f'/mgmt/v1.2/rest/sites/{site_id}')

    # Send request to API

    return _request_processing(conninfo, method, str(uri), headers=header)

