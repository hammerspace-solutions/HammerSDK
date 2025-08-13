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

import urllib.parse as urllib

from typing import List, Optional


class UriBuilder:
    """
    Builds a URI, taking care of URI escaping and ensuring a well-formatted URI.
    """

    def __init__(
        self,
        scheme: Optional[str] = None,
        hostname: Optional[str] = None,
        port: Optional[int] = None,
        path: Optional[str] = None,
        rstrip_slash: bool = True,
    ):
        # Port is not allowed without a hostname
        assert (port and hostname) or (not hostname)

        self._scheme = scheme
        self._hostname = hostname
        self._port = port
        self._path = path or ''
        if rstrip_slash:
            self._path = self._path.rstrip('/')
            if not self._path.startswith('/'):
                self._path = '/' + self._path
        self._query_params: List[str] = []
        self._fragment = ''

    def add_path_component(self, component: str, append_slash: bool = False) -> 'UriBuilder':
        """
        Adds a single path component to the URI. Any characters not in the
        unreserved set, including '/', will be escaped.
        """
        # Completely URI encode the component, even the '/' characters
        self._path = '{}/{}'.format(self._path, urllib.quote(component, ''))
        if append_slash:
            self.append_slash()
        return self

    def append_slash(self) -> 'UriBuilder':
        self._path += '/'
        return self

    def add_query_param(self, name: str, value: Optional[object] = None) -> 'UriBuilder':
        """
        Adds a query parameter with an optional value to the query string. Any
        characters not in the reserved set will be escaped. Spaces will be
        escaped with '+' characters
        """

        # We need to make sure that the words True and False are in lowercase

        new_value = str(value)
        if new_value == "True" or new_value == "False":
            new_value = new_value.lower()

        if new_value is not None:
            self._query_params.append(
                '{}={}'.format(urllib.quote(name, ''), urllib.quote(str(new_value), '')))

        return self

    def __str__(self) -> str:
        # Consider an empty path to be the root for string-printing purposes
        path = '/' if not self._path else str(self._path)
        scheme = '' if not self._scheme else self._scheme
        netloc = '' if not self._netloc() else self._netloc()
        params = '&'.join(self._query_params)
        return urllib.urlunsplit((scheme, netloc, path, params, None))

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def _netloc(self) -> str:
        netloc = ''
        if self._hostname:
            if self._port:
                port_part = ':%s' % str(self._port)
            else:
                port_part = ''
            netloc += f'{self._hostname}{port_part}'

        return netloc
