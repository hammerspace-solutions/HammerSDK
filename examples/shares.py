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
# shares.py
#
# Example to demonstrate how to deal with shares from a Hammerspace environment

'''
== Example Usage:

shares.py --host ip_address|hostname --user NAME --passwd PASSWORD

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

- Test shares in the Hammerspace environment

./shares.py --host dev --port 8443 --user admin -passwd admin


'''

# Import python libraries

import sys
import argparse

from HammerSDK.hammer_client import HammerClient
from HammerSDK.lib import log

from typing import Dict

progName = "hammerspace.hammerclient"
progDesc = "Hammerspace Example Program"
progVers = "5.1.18"


# Hammerspace - class to deal with calls to the Hammerspace environment

class Hammerspace():

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
        self.shares_info = None
        self.shares_uuid = None
        self.mounts_info = None
        self.objectives_info = None
        self.share_info = None

    # Setup the benchmark

    def setup(self):

        # Get script arguments

        self.args = self.commandargs(self.progDesc)

        # Open a connection to the Hammerspace API

        log.debug("Setup the HammerClient Connection")

        self.hammer_connection = HammerClient(self.args.host, self.args.port)

    # Login to the API

    def login(self, user, passwd):

        try:
            self.hammer_login = self.hammer_connection.login(user, passwd, verify_version=False)
        except (Exception,) as excpt:
            log.error(f'Hammerspace login error: {excpt}')
            sys.exit(1)

    # Create a share

    def create_share(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.create_share(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot create share for Hammerspace: {excpt}')
            sys.exit(1)

    # List all the share

    def list_shares(self):

        try:
           return self.hammer_connection.shares.list_shares()
        except (Exception,) as excpt:
            log.error(f'Cannot list shares: {excpt}')
            sys.exit(1)

    # List all the uuids for share

    def list_uuids_for_shares(self):

        try:
            return self.hammer_connection.shares.list_uuids_for_shares()
        except (Exception,) as excpt:
            log.error(f'Cannot list uuids for shares: {excpt}')
            sys.exit(1)

    # Get the mounts for the shares

    def get_mounts_for_share(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.get_mounts_for_share(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot get mounts_for_share: {excpt}')
            sys.exit(1)

    # Get the objectives for the shares

    def get_objectives_for_share(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.get_objectives_for_share(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot get objectives for share: {excpt}')
            sys.exit(1)

    # Set an objective for the shares

    def set_objective(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.set_objective(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot set objective for share: {excpt}')
            sys.exit(1)

    # Update an objective for the shares

    def update_objective(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.update_objective(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot update objective for share: {excpt}')
            sys.exit(1)

    # Unset an objective for the shares

    def unset_objective(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.unset_objective(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot unset objective for share: {excpt}')
            sys.exit(1)

    # Get one particular share

    def get_share(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.get_share(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot get share: {excpt}')
            sys.exit(1)

    # Delete one particular share

    def delete_share(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.delete_share(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot delete share: {excpt}')
            sys.exit(1)

    # Undelete one particular share

    def undelete_share(self, *args, **kwargs):

        try:
            return self.hammer_connection.shares.undelete_share(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot undelete share: {excpt}')
            sys.exit(1)

    # Normally, any code (other than setup) goes here

    def run(self):

        # Login to Hammerspace environment

        self.login(self.args.user, self.args.passwd)

        # Create a share

        share_id = self.create_share(name="Graphics",
                                     path="/Graphics",
                                     comment="Kade Graphics",
                                     size_limit=200000000,
                                     warning_threshold=80,
                                     create_path=True)
        #                             volume_id=["29e4edc2-93e5-44c8-8cfa-719d7dc5eb76"],
        #                             volume_type=["STORAGE_VOLUME"])

        # List all the shares

        self.shares_info = self.list_shares()

        # Tell us how many shares there are...

        leng = len(self.shares_info)
        print(f"There are {leng} shares returned")

        # List all of the UUID's for all the share

        self.shares_uuid = self.list_uuids_for_shares()

        # Tell us how many uuids for shares there are...

        leng = len(self.shares_uuid)
        print(f"There are {leng} uuids for shares returned")

        # Don't continue if we could not find a uuid for the above named share

        if share_id != 0:

            # Get the mounts for a particular share

            self.mounts_info = self.get_mounts_for_share(share_id)

            # Get the objectives for a particular share

            self.objectives_info = self.get_objectives_for_share(share_id)

            # Get one share

            self.share_info = self.get_share(share_id)

            # There better be only one share

            assert isinstance(self.share_info, Dict)

            # Set an objective on the share

            self.objectives_info = self.set_objective(share_id,
                                                      "keep-online",
                                                      applicability="True")

            # Update an objective on the share

            self.objectives_info = self.update_objective(share_id,
                                                         "keep-online",
                                                         applicability="True",
                                                         new_applicability="Always")

            # "Unset"" an objective on the share

            self.objectives_info = self.unset_objective(share_id,
                                                        "keep-online",
                                                         applicability="Always")

            # Delete the share

            self.share_info = self.delete_share(share_id,
                                                delete_path=False,
                                                delete_delay=60)

            # Undelete the same share

            self.share_info = self.undelete_share(share_id)

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

    # Setup the program

    with Hammerspace() as hammer:
        hammer.run()

    sys.exit()


#
# Main routine

if __name__ == '__main__':
    main()
