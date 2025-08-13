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


"""
hammer_client is a wrapper for the modules in the rest directory. It is composed
of a single public function called HammerClient that wraps all of the functions.
"""

import functools
import types
import requests
import HammerSDK.lib.request as request
import HammerSDK.rest  # Pull in all the REST client modules and methods

from HammerSDK.lib.HammerExceptions import InvalidSDKVersion

from typing import Any, Callable, Mapping, Optional, Sequence, Type, Union

# SDK Version

SDK_Version = "5.1.18"


def _wrap_rest_request(request_method: Callable[..., requests.Response]) -> Callable[..., Any]:
    """
    Wrap a function that begins with the parameters conninfo
    returning a function suitable for use as a method on a rest module class.
    """

    @functools.wraps(request_method)
    def wrapper(self: Any, *args: object, **kwargs: object) -> Any:
        response = request_method(self.client.conninfo, *args, **kwargs)
        return response

    return wrapper


DEFAULT_REST_PORT: int = 8443


class HammerClient:
    """
    Provide access to the all the HammerSDK API wrappers.

    Args:
        address (str): Hostname or IP address to Hammerspace Anvil
        port (int): Port on which the Hammerspace API listens
        timeout (int, optional): Number of seconds before giving up

    Returns:
        HammerClient (class): The HammerClient class

    Examples:
        from HammerSDK.hammer_client import HammerClient

        self.hammer_connection = HammerClient(self.host, self.hport)
    """

    # rest module attributes

    auth: Any
    nodes: Any
    logical_volumes: Any
    objectives: Any
    shares: Any
    share_snapshots: Any
    sites: Any
    storage_volumes: Any
    volume_groups: Any
    
    def __init__(
        self,
        address: str,
        port: int = DEFAULT_REST_PORT,
        timeout: Optional[int] = None,
    ) -> None:

        self.conninfo = request.Connection(address, port, timeout=timeout)

        # Opening the connection will create a session to Hammerspace

        self.conninfo.open()

    @property
    def port(self) -> int:
        return self.conninfo.port

    def login(self,
              username: str,
              password: str,
              verify_version: Optional[bool] = True) -> requests.Response:
        """
        Login to a Hammerspace Anvil

        Args:
             username (str): Username needed to login to the Hammerspace Anvil
             password (str): Password needed to login to the Hammerspace Anvil
             verify_version (bool): False if the SDK version should not be verified against the Anvil

        Returns:
             response (requests.Response): The json response structure

        Examples:
             from HammerSDK.hammer_client import HammerClient

             self.hammer_connection = HammerClient(self.host, self.hport)
             self.hammer_connection.login(self.username, self.password)
        """

        # Login through the Anvil

        response_data = self.auth.login(username, password)

        # If the Anvil version doesn't match the SDK version, then throw an exception

        if not verify_version:
            return response_data

        nodes_info = self.nodes.list_nodes()
        for nodes in nodes_info:
            if nodes.get("swVersion"):
                cur_version = nodes["swVersion"]["version"]

                # Is the SDK version less than what we expect? Then throw an exception...

                if cur_version < self.SDK_version:
                    raise InvalidSDKVersion(self.SDK_version, cur_version)
                else:
                    break

        return response_data


    def close(self) -> None:
        """
        Close the underlying network connection.

        An explicit close() should not strictly be necessary, as refcount GC will also
        ensure the connection gets closed.  This provides a stronger guarantee or
        tighter control if desired (e.g. it might be useful when a long lived instance
        has long idle periods).

        This client may be re-used after being closed (with the effect of implicitly
        re-opening the connection).

        Examples:
             from HammerSDK.hammer_client import HammerClient

             self.hammer_connection = HammerClient(self.host, self.hport)
             self.hammer_connection.login(self.username, self.password)
        """

        self.conninfo.close()

    def request(
        self,
        method: str,
        uri: str,
        body: Optional[Union[Sequence[object], Mapping[str, object]]] = None,
        request_content_type: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Any:
        """
        Make a raw request against the Hammerspace REST API, returning a Response with
        JSON-decoded data payload and an optional etag.
        """

        response = self.conninfo.request(
            method=method,
            uri=uri,
            body=body,
            request_content_type=request_content_type,
            headers=headers)

        return response.text


# Wraps the new style of modules with requests

def _wrap_strongly_typed_module(self: HammerClient, module: Any) -> Any:
    def wrap_request(request_method: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(request_method)
        def wrapper(*args: object, **kwargs: object) -> Any:
            return request_method(*args, **kwargs)

        return wrapper

    for member_name in dir(module):
        if callable(getattr(module, member_name)):
            func = getattr(module, member_name)
        else:
            continue

        if getattr(func, 'request', False) is True:
            setattr(module, member_name, wrap_request(func))

    return module


def _wrap_rest_module(module: types.ModuleType,
                      existing_property: Optional[property]) -> property:
    """
    Given a module, return a property that mimics it.

    This is tricky because we want to wrap each function in the module, and bind
    its first two arguments with fields in the HammerClient object. However, we
    don't have the HammerClient object instantiated at this point. So, what we
    return is the ability to create the mimicking class, instead of the class
    itself.
    """

    class RestModule:
        __doc__ = module.__doc__

        def __init__(self, client: HammerClient):
            self.client = client

    if existing_property is None:
        wrapped_class: Callable[..., Any] = RestModule
    else:
        assert existing_property.fget is not None
        wrapped_class = existing_property.fget  # get the existing class

    for name, method in vars(module).items():
        if callable(method) and getattr(method, 'request', False) is True:
            setattr(wrapped_class, name, _wrap_rest_request(method))

    return property(wrapped_class)


def _wrap_all_rest_modules(root: types.ModuleType, cls: Type[HammerClient]) -> None:
    """
    Wrap all rest modules loaded in the provided root module, adding a property
    to the HammerClient type for each. If a property already exists, it will not
    be overwritten.

    This allows the private modules to dominate the public ones.
    """

    for name, module in vars(root).items():

        if isinstance(module, types.ModuleType):
            existing_property = getattr(cls, name, None)
            setattr(cls, name, _wrap_rest_module(module, existing_property))


_wrap_all_rest_modules(HammerSDK.rest, HammerClient)
