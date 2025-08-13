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
# storage_volumes.py
#
# Example to demonstrate how to deal with storage_volumes data from a Hammerspace environment

"""
== Example Usage:

storage_volumes.py --host ip_address|hostname --user NAME --passwd PASSWORD

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

from time import sleep

from HammerSDK.hammer_client import HammerClient
from HammerSDK.lib import log
from HammerSDK.lib.HammerExceptions import VolumeNotDecommissioned, VolumeDecommissioning, VolumeWasUsed

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

        # Anvil connection

        self.hammer_connection = None
        self.hammer_login = None
        self.storage_volume_info = None
        self.decommissioning_volume_info = None
        self.decommissioned_volume_info = None
        self.delete_volume_info = None

    # Setup the benchmark

    def setup(self):

        # Get script arguments

        self.args = self.commandargs(self.progDesc)
        self.hammer_connection = None

        # Open a connection to the Hammerspace API

        log.debug("Setup the HammerClient Connection")

        self.hammer_connection = HammerClient(self.args.host, self.args.port)

    # Execute any volume operation safely... This eliminates code duplication

    @staticmethod
    def safe_storage_volume_operation(operation, *args, **kwargs):
        """
            This method wraps the operations on the storage volumes, providing a unified place for error handling.
            :param operation: A function representing the storage volumes operation to be performed.
            :param args: Positional arguments to pass to the operation function.
            :param kwargs: Keyword arguments to pass to the operation function.
            :return: The result of the storage volume operation.
            """

        while True:
            try:
                result = operation(*args, **kwargs)
            except (VolumeDecommissioning,) as excpt:
                log.info(f"{excpt}")
                sleep(10)
                continue
            except (VolumeNotDecommissioned,):
                raise
            except (VolumeWasUsed,):
                raise
            except (Exception,) as excpt:
                log.error('Cannot execute operation on storage volume from Hammerspace = %s', excpt)
                sys.exit(1)
            else:
                return result

    def run(self):

        # Login to Hammerspace environment

        try:
            self.hammer_login = self.hammer_connection.login(self.args.user, self.args.passwd)
        except (Exception,) as excpt:
            log.error('Hammerspace login error = %s', excpt)
            sys.exit(1)

        # Create a storage volume

        created = False
        force_flag = False

        # This call is going to occur twice. Once with an exception because the volume was previously in use

        while not created:
            try:
                Hammerspace.safe_storage_volume_operation(
                    self.hammer_connection.storage_volumes.create_volume,
                    name=self.args.volname,
                    logical_volume_name=self.args.log_volname,
                    node_name=self.args.nodename,
                    comment="Test Storage Volume",
                    force=force_flag)
            except (VolumeWasUsed, ) as excpt:
                log.error(excpt)
                force_flag = True
            else:
                created = True

        # List all the storage_volumes

        self.storage_volume_info = Hammerspace.safe_storage_volume_operation(
                 self.hammer_connection.storage_volumes.list_storage_volumes)

        # Tell us how many storage volumes there are...

        leng = len(self.storage_volume_info)
        print(f"There are {leng} storage volumes returned")

        # Get one of the storage volume uuid fields so that we can do the next call

        storage_volume_id = 0

        for storage_volume in self.storage_volume_info:
            storage_volume_id = storage_volume['uoid']['uuid']
            break

        # Get one storage volume

        self.storage_volume_info = Hammerspace.safe_storage_volume_operation(
            self.hammer_connection.storage_volumes.get_storage_volume,
            volume_id=storage_volume_id)

        # There better be only one storage volume

        assert isinstance(self.storage_volume_info, Dict)

        # Print out the storage volume structure

        print(json.dumps(self.storage_volume_info, indent=4))

        # Try to delete a non-decommissioned storage volume. We should get an exception

        try:
            self.delete_volume_info = Hammerspace.safe_storage_volume_operation(
                self.hammer_connection.storage_volumes.delete_storage_volume,
                volume_id=storage_volume_id)
        except (VolumeNotDecommissioned,) as excpt:
            log.error(f'Expected exception: {excpt}')

        # Now, test the decommissioning of the volume

        self.decommissioned_volume_info = Hammerspace.safe_storage_volume_operation(
            self.hammer_connection.storage_volumes.decommission_storage_volume,
            volume_id=storage_volume_id)

        # Finally, delete the volume

        decommissioned = False

        while not decommissioned:
            try:
                self.delete_volume_info = Hammerspace.safe_storage_volume_operation(
                    self.hammer_connection.storage_volumes.delete_storage_volume,
                    volume_id=storage_volume_id)
            except (VolumeNotDecommissioned,) as excpt:
                continue
            else:
                decommissioned = True

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
        parser.add_argument('--vol_name',
                            dest='volname',
                            required=True,
                            help='Specify storage volume name to add')
        parser.add_argument('--logical_vol_name',
                            dest='log_volname',
                            required=True,
                            help='Specify logical volume name to use')
        parser.add_argument('--node_name',
                            dest='nodename',
                            required=True,
                            help='Specify node name to use')
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
