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
# login.py
#
# Example to demonstrate how to login to a Hammerspace environment

'''
== Example Usage:

login.py --host ip_address|hostname --user NAME --passwd PASSWORD

=== Required:

[-i | --ip | --host] ip|hostname    An ip address or hostname of the Anvil

=== Options:

[--user] username                   Use 'username' for authentication
                                        (defaults to 'admin')
[-p] [--passwd] password            Use 'password' for authentication
                                        (defaults to 'admin')
[-P | --port] number                Use 'number' for the API server port
                                        (defaults to 8443)

-h | --help                         Print out the script usage/help

=== Examples:

- Login to the Hammerspace environment

./login.py --host dev --port 8443 --user admin -passwd admin


'''

# Import python libraries

import sys
import argparse

from HammerSDK.hammer_client import HammerClient
from HammerSDK.lib import log

progName = "hammerspace.hammerclient"
progDesc = "Hammerspace Example Program"
progVers = "5.1.18"


# Hammerspace - class to deal with calls to the Hammerspace environment

class Hammerspace():

    def __init__(self):

        # Version info

        self.progName = progName
        self.progDesc = progDesc
        self.progVers = progVers

        # Others

        self.args = None
        self.logger = None

    # Setup the benchmark

    def SetUp(self):

        # Get script arguments

        self.args = self.CommandArgs(self.progDesc)

        # Set some of the cluster info from the arguments

        self.hport = self.args.port
        self.hhost = self.args.host
        self.hlogin = self.args.user
        self.hpasswd = self.args.passwd

        # Open a connection to the Hammerspace API

        log.info("This is a test")

        self.hammer_connection = HammerClient(self.hhost, self.hport)
        return

    # Normally, any code (other than setup) goes here

    def Run(self):

        # Login to Hammerspace environment

        try:
            self.hammer_login = self.hammer_connection.login(self.hlogin, self.hpasswd)
        except (Exception,) as excpt:
            log.error('Hammerspace login error = %s', excpt)
            sys.exit(1)

        return

    # The program is done... Start the tear down (if needed)

    def TearDown(self):

        return

    # Build and get the command line

    def CommandArgs(self, desc):

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
        parser.add_argument('-p', '--pass',
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

    hammer = Hammerspace()
    hammer.SetUp()

    # Run the program

    hammer.Run()

    # Once the program is done, tear everything down.

    hammer.TearDown()
    sys.exit()


#
# Main routine

if __name__ == '__main__':
    main()
