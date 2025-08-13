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
# objectives.py
#
# Example to demonstrate how to deal with objectives from a Hammerspace environment

"""
== Example Usage:

objectives.py --host ip_address|hostname --user NAME --passwd PASSWORD

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

- Test objectives in the Hammerspace environment

./objectives.py --host dev --port 8443 --user admin -passwd admin


"""

# Import python libraries

import sys
import argparse
import json

from HammerSDK.hammer_client import HammerClient
from HammerSDK.lib import log
from HammerSDK.lib.HammerExceptions import (ObjectiveInvalidPriority,
                                            ObjectiveInvalidCost,
                                            ObjectiveInvalidStorageSize,
                                            ObjectiveInvalidPlaceon,
                                            ObjectiveInvalidConfineExclude,
                                            ObjectiveInvalidAppliedObjective)
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

        self.progName = progName
        self.progDesc = progDesc
        self.progVers = progVers
        
        # Others

        self.args = None
        self.logger = None

        # Anvil variables

        self.hammer_connection = None
        self.hammer_login = None
        self.objectives_info = None
        self.objective_info = None

    # Login to the API

    def login(self, user, passwd):

        try:
            self.hammer_login = self.hammer_connection.login(user, passwd, verify_version=False)
        except (Exception,) as excpt:
            log.error(f'Hammerspace login error: {excpt}')
            sys.exit(1)

    # Create an objective with known errors

    def create_objective_error(self, *args, **kwargs):

        try:
            return self.hammer_connection.objectives.create_objective(*args, **kwargs)
        except (Exception,
                ObjectiveInvalidPriority,
                ObjectiveInvalidCost,
                ObjectiveInvalidStorageSize,
                ObjectiveInvalidPlaceon,
                ObjectiveInvalidConfineExclude,
                ObjectiveInvalidAppliedObjective) as excpt:
            log.error(f'Known objective error: {excpt}')

    # Create a valid objective

    def create_objective(self, *args, **kwargs):

        try:
            return self.hammer_connection.objectives.create_objective(*args, **kwargs)
        except (Exception,
                ObjectiveInvalidPriority,
                ObjectiveInvalidCost,
                ObjectiveInvalidStorageSize,
                ObjectiveInvalidPlaceon,
                ObjectiveInvalidConfineExclude,
                ObjectiveInvalidAppliedObjective) as excpt:
            log.error(f'Known objective error: {excpt}')
            sys.exit(1)

    # Delete one objective

    def delete_objective(self, *args, **kwargs):

        try:
            return self.hammer_connection.objectives.delete_objective(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot delete objective: {excpt}')
            sys.exit(1)

    # Get one objective

    def get_objective(self, *args, **kwargs):

        try:
            return self.hammer_connection.objectives.get_objective(*args, **kwargs)
        except (Exception,) as excpt:
            log.error(f'Cannot get objective: {excpt}')
            sys.exit(1)

    # List all the objectives

    def list_objectives(self, *args, **kwargs):

        try:
            return self.hammer_connection.objectives.list_objectives()
        except (Exception,) as excpt:
            log.error(f'Cannot list objectives: {excpt}')
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

        # Trying to create objectives with errors. These should all raise Exceptions

        # Invalid place-on driective with name of "fubar" versus "first"

        self.objectives_info = self.create_objective_error(name="v-objective-error",
                                                           place_on={
                                                               "fubar": [
                                                                   {
                                                                       "volumes":
                                                                           [
                                                                               "kade-dsx-1.selab.hammer.space::/hsvol0",
                                                                               "kade-dsx-2.selab.hammer.space::/hsvol0"
                                                                           ]
                                                                   }
                                                               ]
                                                           }
                                                           )

        # Invalid place-on objective with malformed "volumes"

        self.objectives_info = self.create_objective_error(name="v-objective-error",
                                                           place_on={
                                                               "first": [
                                                                   {
                                                                       "volumes":
                                                                       {
                                                                               "kade-dsx-1.selab.hammer.space::/hsvol0",
                                                                               "kade-dsx-2.selab.hammer.space::/hsvol0"
                                                                       }
                                                                   }
                                                               ]
                                                           }
                                                           )

        # Invalid place-on directive with malformed "first"

        self.objectives_info = self.create_objective_error(name="v-objective-error",
                                                           place_on={
                                                               "first":
                                                                   {
                                                                       "volumes":
                                                                           [
                                                                               "kade-dsx-1.selab.hammer.space::/hsvol0",
                                                                               "kade-dsx-2.selab.hammer.space::/hsvol0"
                                                                           ]
                                                                   }
                                                           }
                                                           )

        # Invalid place-on directive with something called "volume" instead of "volumes"

        self.objectives_info = self.create_objective_error(name="v-objective-error",
                                                           place_on={
                                                               "first": [
                                                                   {
                                                                       "volume":
                                                                           [
                                                                               "kade-dsx-1.selab.hammer.space::/hsvol0",
                                                                               "kade-dsx-2.selab.hammer.space::/hsvol0"
                                                                           ]
                                                                   }
                                                               ]
                                                           }
                                                           )

        # Invalid confine-to directive with something called "volume" instead of "volumes"

        self.objectives_info = self.create_objective_error(name="v-objective-error",
                                                           confine_to={
                                                                       "volume":
                                                                           [
                                                                               "kade-dsx-1.selab.hammer.space::/hsvol0",
                                                                               "kade-dsx-2.selab.hammer.space::/hsvol0"
                                                                           ]
                                                                   }
                                                           )

        # Create an objective

        self.objective_info = self.create_objective(name="v-objective-test",
                                                    place_on={
  "first": [
    {
      "volumes":
      [
        "kade-dsx-1.selab.hammer.space::/hsvol0",
        "kade-dsx-2.selab.hammer.space::/hsvol0"
      ]
    }
  ],
  "second": [
    {
      "volume-groups":
      [
        "TestGroup"
      ]
    },
    {
      "volumes":
      [
        "kade-dsx-1.selab.hammer.space::/hsvol0",
        "kade-dsx-2.selab.hammer.space::/hsvol0"
      ]
    }
  ]
},
                                                    confine_to={
    "volumes":
    [
        "kade-dsx-1.selab.hammer.space::/hsvol1",
        "kade-dsx-2.selab.hammer.space::/hsvol1"
    ],
    "volume-groups":
    [
        "TestGroup"
    ],
    "nodes":
    [
        "kade-dsx-1.selab.hammer.space",
        "kade-dsx-2.selab.hammer.space"
    ]
},
                                                    exclude_from={
    "volumes":
    [
        "kade-dsx-1.selab.hammer.space::/hsvol1",
        "kade-dsx-2.selab.hammer.space::/hsvol1"
    ],
    "volume-groups":
    [
        "TestGroup"
    ],
    "nodes":
    [
        "kade-dsx-1.selab.hammer.space",
        "kade-dsx-2.selab.hammer.space"
    ]
},
                                                    read_thruput=750000000,
                                                    write_thruput=250000000
                                                    )

        # Create an invalid applied objective with an incorrect type

        self.applied_info = self.create_objective_error(name="v-applied-objective",
                                                    applied_objectives=[
                                                        {
                                                            "applied": "LAST_USE_AGE<1*HOURS",
                                                            "type": "fubar",
                                                            "objective-name": "v-objective-test"
                                                        }
                                                    ]
                                                    )

        # Create an invalid applied objective with a type that is not a str

        self.applied_info = self.create_objective_error(name="v-applied-objective",
                                                    applied_objectives=[
                                                        {
                                                            "applied": "LAST_USE_AGE<1*HOURS",
                                                            "type": {"type:", "true"},
                                                            "objective-name": "v-objective-test"
                                                        }
                                                    ]
                                                    )

        # Create an applied objective

        self.applied_info = self.create_objective(name="v-applied-objective",
                                                    applied_objectives=[
                                                        {
                                                            "applied": "LAST_USE_AGE<1*HOURS",
                                                            "type": "true",
                                                            "objective-name": "v-objective-test"
                                                        }
                                                    ]
                                                    )

        # Get the uuid for the newly created objective

        objective_id = self.objective_info["uoid"]["uuid"]
        applied_id = self.applied_info["uoid"]["uuid"]

        # List all the objectives

        self.objectives_info = self.list_objectives()

        # Tell us how many objectives there are...

        leng = len(self.objectives_info)
        print(f"There are {leng} objectives returned")

        # Get one objective

        self.objective_info = self.get_objective(objective_id)

        # There better be only one objective

        assert isinstance(self.objective_info, Dict)

        # Print out the objective structure

        print(json.dumps(self.objective_info, indent=4))

        # Delete the objective and the applied objective

        self.delete_objective(objective_id)
        self.delete_objective(applied_id)
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

    # Run the program

    with Hammerspace() as hammer:
        hammer.run()

    sys.exit()


#
# Main routine

if __name__ == '__main__':
    main()
