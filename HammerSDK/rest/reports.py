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
from typing import Any, Optional, List

# SDK Version
SDK_Version = "5.1.18"


@request.request
def get_active_files(conninfo: request.Connection,
                       start_millis: Optional[int] = None,
                       end_millis: Optional[int] = None,
                       share: Optional[str] = None,
                       sv: Optional[str] = None,
                       limit: Optional[int] = None) -> Any:
    """
    Query influxDB for active files reports.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        start_millis (int, optional): Start of the interval in ms from epoch.
        end_millis (int, optional): End of the interval in ms from epoch.
        share (str, optional): Share to filter by.
        sv (str, optional): Storage volume to filter by.
        limit (int, optional): Limit the number of results.

    Returns:
        json object: Active files report
    """
    method = 'GET'
    uri = UriBuilder(path='/mgmt/v1.2/rest/reports/active-files')
    header = {'Accept': 'application/json'}

    if start_millis is not None:
        uri.add_query_param('startMillis', start_millis)
    if end_millis is not None:
        uri.add_query_param('endMillis', end_millis)
    if share:
        uri.add_query_param('share', share)
    if sv:
        uri.add_query_param('sv', sv)
    if limit is not None:
        uri.add_query_param('limit', limit)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_activity_analytics(conninfo: request.Connection,
                             share: Optional[str] = None,
                             sv: Optional[str] = None) -> Any:
    """
    Query influxDB for active clients reports.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        share (str, optional): Share to filter by.
        sv (str, optional): Storage volume to filter by.

    Returns:
        json object: Activity analytics report
    """
    method = 'GET'
    uri = UriBuilder(path='/mgmt/v1.2/rest/reports/activity-analytics')
    header = {'Accept': 'application/json'}

    if share:
        uri.add_query_param('share', share)
    if sv:
        uri.add_query_param('sv', sv)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_cloud_activity(conninfo: request.Connection,
                         osv: str,
                         start_millis: Optional[int] = None,
                         end_millis: Optional[int] = None,
                         cdm_breakdown: Optional[bool] = False) -> Any:
    """
    Query influxDB for activity on cloud.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        osv (str): Object Storage Volume.
        start_millis (int, optional): Start of the interval in ms from epoch.
        end_millis (int, optional): End of the interval in ms from epoch.
        cdm_breakdown (bool, optional): Breakdown by CDM. Defaults to False.

    Returns:
        json object: Cloud activity report
    """
    method = 'GET'
    uri = UriBuilder(path='/mgmt/v1.2/rest/reports/cloud-activity')
    header = {'Accept': 'application/json'}

    uri.add_query_param('osv', osv)
    if start_millis is not None:
        uri.add_query_param('startMillis', start_millis)
    if end_millis is not None:
        uri.add_query_param('endMillis', end_millis)
    if cdm_breakdown:
        uri.add_query_param('cdm_breakdown', 'true')

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_licensed_usage(conninfo: request.Connection,
                         activation_id: str,
                         preceding_duration_millis: Optional[int] = None) -> Any:
    """
    Get the usage associated with a metered client license.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        activation_id (str): Activation ID of the metered usage license.
        preceding_duration_millis (int, optional): Reporting range in ms before current time.

    Returns:
        json object: Licensed usage report
    """
    method = 'GET'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/reports/licensed-usage/{activation_id}')
    header = {'Accept': 'application/json'}

    if preceding_duration_millis is not None:
        uri.add_query_param('precedingDurationMillis', preceding_duration_millis)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_mobility_report(conninfo: request.Connection,
                          start_millis: Optional[int] = None,
                          end_millis: Optional[int] = None,
                          share: Optional[str] = None,
                          from_sv: Optional[str] = None,
                          to_sv: Optional[str] = None,
                          reasons: Optional[List[str]] = None,
                          statuses: Optional[List[str]] = None) -> Any:
    """
    Query influxDB for mobility reports.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        start_millis (int, optional): Start of the interval in ms from epoch.
        end_millis (int, optional): End of the interval in ms from epoch.
        share (str, optional): Share to filter by.
        from_sv (str, optional): Source storage volume.
        to_sv (str, optional): Destination storage volume.
        reasons (List[str], optional): List of mobility reasons to filter by.
        statuses (List[str], optional): List of mobility statuses to filter by.

    Returns:
        json object: Mobility report
    """
    method = 'GET'
    uri = UriBuilder(path='/mgmt/v1.2/rest/reports/mobility')
    header = {'Accept': 'application/json'}

    if start_millis is not None:
        uri.add_query_param('startMillis', start_millis)
    if end_millis is not None:
        uri.add_query_param('endMillis', end_millis)
    if share:
        uri.add_query_param('share', share)
    if from_sv:
        uri.add_query_param('from', from_sv)
    if to_sv:
        uri.add_query_param('to', to_sv)
    if reasons:
        for reason in reasons:
            uri.add_query_param('reasons', reason)
    if statuses:
        for status in statuses:
            uri.add_query_param('statuses', status)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_proxy_usage(conninfo: request.Connection, preceding_duration_millis: Optional[int] = None) -> Any:
    """
    Get the usage for all clusters known to be subject to metered usage.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        preceding_duration_millis (int, optional): Reporting range in ms before current time.

    Returns:
        json object: Proxy usage report
    """
    method = 'GET'
    uri = UriBuilder(path='/mgmt/v1.2/rest/reports/proxy-usage')
    header = {'Accept': 'application/json'}

    if preceding_duration_millis is not None:
        uri.add_query_param('precedingDurationMillis', preceding_duration_millis)

    return _request_processing(conninfo, method, str(uri), headers=header)


@request.request
def get_replication_latencies(conninfo: request.Connection,
                                uuid: str,
                                participant_id: Optional[str] = None,
                                start_millis: Optional[int] = None,
                                end_millis: Optional[int] = None) -> Any:
    """
    Query influxDB for replication latencies.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        uuid (str): Share UUID.
        participant_id (str, optional): Participant ID to filter by.
        start_millis (int, optional): Start of the interval in ms from epoch.
        end_millis (int, optional): End of the interval in ms from epoch.

    Returns:
        json object: Replication latencies report
    """
    method = 'GET'
    uri = UriBuilder(path=f'/mgmt/v1.2/rest/reports/replication/share-latencies/{uuid}')
    header = {'Accept': 'application/json'}

    if participant_id:
        uri.add_query_param('participantId', participant_id)
    if start_millis is not None:
        uri.add_query_param('startMillis', start_millis)
    if end_millis is not None:
        uri.add_query_param('endMillis', end_millis)

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
