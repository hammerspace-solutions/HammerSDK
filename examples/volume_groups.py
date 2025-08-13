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
# volume_groups.py
#
# Example to demonstrate how to deal with volume_groups data from a Hammerspace environment

"""
== Example Usage:

volume_groups.py --host ip_address|hostname --user NAME --passwd PASSWORD

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

- Test storage_volumes in the Hammerspace environment

./storage_volumes.py --host dev --port 8443 --user admin -passwd admin


"""

# Import python libraries

import sys
import argparse
import json

from HammerSDK.hammer_client import HammerClient
from HammerSDK.lib import log
from HammerSDK.lib.HammerExceptions import InvalidSDKArgumentsGiven

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
        self.groups_info = None
        self.group_info = None

    # Login to the API

    def login(self, user, passwd):

        try:
            self.hammer_login = self.hammer_connection.login(user, passwd, verify_version=False)
        except (Exception,) as excpt:
            log.error(f'Hammerspace login error: {excpt}')
            sys.exit(1)

    # Create a volume group

    def create_group(self, *args, **kwargs):

        try:
            return self.hammer_connection.volume_groups.create_group(*args, **kwargs)
        except (InvalidSDKArgumentsGiven,) as excpt:
            log.error(f"Valid error: {excpt}")
        except (Exception,) as excpt:
            log.error(f'Cannot create volume group: {excpt}')
            sys.exit(1)

    # List all the volume groups

    def list_groups(self):

        try:
            return self.hammer_connection.volume_groups.list_groups()
        except (Exception,) as excpt:
            log.error(f'Cannot list volume groups: {excpt}')
            sys.exit(1)

    # Get one volume group

    def get_group(self, *args, **kwargs):

        try:
            return self.hammer_connection.volume_groups.get_group(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot get volume group: {excpt}')
            sys.exit(1)

    # Delete volume group.

    def delete_group(self, *args, **kwargs):

        try:
            return self.hammer_connection.volume_groups.delete_group(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot delete volume group: {excpt}')
            sys.exit(1)

    # Setup the benchmark

    def setup(self):

        # Get script arguments

        self.args = self.commandargs(self.progDesc)

        # Set some of the cluster info from the arguments

        self.hammer_connection = None

        # Open a connection to the Hammerspace API

        log.debug("Setup the HammerClient Connection")

        self.hammer_connection = HammerClient(self.args.host, self.args.port)

    # Normally, any code (other than setup) goes here

    def run(self):

        # Login to Hammerspace environment

        self.login(self.args.user, self.args.passwd)

        # Create an invalid volume group. Testing errors

        self.group_info = self.create_group(name=self.args.groupname,
                                            comment="Test Storage Volume")

        # Create a volume group

        self.group_info = self.create_group(name=self.args.groupname,
                                            volume_names=self.args.volnames,
                                            node_names=self.args.nodenames,
                                            volume_group_names=self.args.groupnames,
                                            comment="Test Storage Group")

        # List all the volume groups

        self.groups_info = self.list_groups()

        # Tell us how many volume groups there are...

        leng = len(self.groups_info)
        print(f"There are {leng} volume groups returned")

        # Get one of the volume group uuid fields so that we can do the next call

        group_id = 0

        for volume_group in self.groups_info:
            if volume_group["name"] == self.args.groupname:
                group_id = volume_group['uoid']['uuid']
                break

        # Get one volume group

        self.group_info = self.get_group(group_id)

        # There better be only one volume group

        assert isinstance(self.group_info, Dict)

        # Print out the volume group structure

        print(json.dumps(self.group_info, indent=4))

        # Try to delete volume group.

        self.group_info = self.delete_group(group_id)
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
        parser.add_argument('-port', type=int, dest='port',
                            default=8443, required=False,
                            help='Specify port on Hammerspace; default to 8443')
        parser.add_argument('-u', '--user', default='admin', dest='user',
                            required=False,
                            help='Specify user credentials for login')
        parser.add_argument('--pass',
                            default='admin', dest='passwd',
                            help='Specify password for login')
        parser.add_argument('--group_name',
                            dest='groupname',
                            required=True,
                            help='Specify volume group to add')
        parser.add_argument('--vol_name',
                            dest='volnames',
                            action="append",
                            required=False,
                            help='Specify volume name to use')
        parser.add_argument('--node_name',
                            dest='nodenames',
                            action="append",
                            required=False,
                            help='Specify node name to use')
        parser.add_argument('--vol_group_name',
                            dest='groupnames',
                            action="append",
                            required=False,
                            help='Specify volume group names to use')
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
