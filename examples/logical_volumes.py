#!/usr/bin/env python

# Copyright (c) 2023 Hammerspace
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
# -----------------------------------------------------------------------------
# logical_volumes.py
#
# Example to demonstrate how to deal with logical_volume data from a Hammerspace environment

"""
== Example Usage:

logical_volumes.py --host ip_address|hostname --user NAME --passwd PASSWORD

=== Required:

[-i | --ip | --host] ip|hostname    An ip address or hostname of the Anvil

=== Options:

[--user] username                   Use 'username' for authentication
                                        (defaults to 'admin')
[--passwd] password                 Use 'password' for authentication
                                        (defaults to 'admin')
[-P | --port] number                Use 'number' for the API server port
                                        (defaults to 8443)

-h | --help                         Print out the script usage/help

=== Examples:

- Test logical_volumes in the Hammerspace environment

./logical_volumes.py --host dev --port 8443 --user admin -passwd admin


"""

# Import python libraries

import sys
import argparse
import json

from HammerSDK.hammer_client import HammerClient
from HammerSDK.lib import log

from typing import Dict

progName = "hammerspace.hammerclient"
progDesc = "Hammerspace Example Program"
progVers = "5.1.18"


# Hammerspace - class to deal with calls to the Hammerspace environment

class Hammerspace:

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, *exc_s):
        self.teardown()

    def __init__(self):

        # Version info

        self.progName = progName
        self.progDesc = progDesc
        self.progVers = progVers

        # Others

        self.args = None
        self.logger = None

        # Anvil variables

        self.hammer_connection = None
        self.hammer_login = None
        self.logical_volume_info = None

    # Login to the API

    def login(self, user, passwd):

        try:
            self.hammer_login = self.hammer_connection.login(user, passwd, verify_version=False)
        except (Exception,) as excpt:
            log.error(f'Hammerspace login error: {excpt}')
            sys.exit(1)

    # List all the logical_volumes

    def list_logical_volumes(self):

        try:
            return self.hammer_connection.logical_volumes.list_logical_volumes()
        except (Exception,) as excpt:
            log.error(f'Cannot list logical volumes: {excpt}')
            sys.exit(1)

    # Get one logical volume

    def get_logical_volume(self, logical_volume_id):

        try:
            return self.hammer_connection.logical_volumes.get_logical_volume(logical_volume_id)
        except (Exception,) as excpt:
            log.error(f'Cannot get logical volume: {excpt}')
            sys.exit(1)

    # Setup the benchmark

    def setup(self):

        # Get script arguments

        self.args = self.commandargs(self.progDesc)

        # Open a connection to the Hammerspace API

        log.debug("Setup the HammerClient Connection")

        self.hammer_connection = HammerClient(self.args.host, self.args.port)

    # Normally, any code (other than setup) goes here

    def run(self):

        # Login to Hammerspace environment

        self.login(self.args.user, self.args.passwd)

        # List all the logical_volumes

        self.logical_volume_info = self.list_logical_volumes()

        # Tell us how many logical volumes there are...

        leng = len(self.logical_volume_info)
        print(f"There are {leng} logical volumes returned")

        # Get one of the logical volume uuid fields so that we can do the next call

        logical_volume_id = 0

        for logical_volume in self.logical_volume_info:
            logical_volume_id = logical_volume['uoid']['uuid']
            break

        # Get one logical volume

        self.logical_volume_info = self.get_logical_volume(logical_volume_id)

        # There better be only one logical volume

        assert isinstance(self.logical_volume_info, Dict)

        # Print out the logical volume structure

        print(json.dumps(self.logical_volume_info, indent=4))

        return

    # The program is done... Start the tear down (if needed)

    def teardown(self):

        return

    # Build and get the command line

    def commandargs(self, desc):

        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument('--version', action='version',
                            version='{name} - Version {version}'.format(name=self.progName,
                                                                        version=self.progVers))
        parser.add_argument('-i', '--ip', '--host', dest='host',
                            required=True,
                            help='Specify Hammerspace host for API')
        parser.add_argument('-P', '--port', type=int, dest='port',
                            default=8443, required=False,
                            help='Specify port on Hammerspace; default to 8443')
        parser.add_argument('-u', '--user', default='admin', dest='user',
                            required=False,
                            help='Specify user credentials for login')
        parser.add_argument('--pass',
                            default='admin', dest='passwd',
                            help='Specify password for login')
        parser.add_argument('--log',
                            help='Set the logging level',
                            dest='loglevel',
                            default='INFO',
                            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'DEBUG'])
        try:
            return parser.parse_args()
        except argparse.ArgumentTypeError as e:
            self.logger.error("Argument Parsing Error: %s", e)
            sys.exit(1)


# Main routine

def main():

    # Run the program

    with Hammerspace() as hammer:
        hammer.run()

    sys.exit()


#
# Main routine

if __name__ == '__main__':
    main()
