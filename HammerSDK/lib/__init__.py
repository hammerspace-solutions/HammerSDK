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

import logging


# Create a class to handle formatting messages for logging

class VarFormatter(logging.Formatter):
    default_formatter = logging.Formatter("%(levelname)s: %(message)s")

    def __init__(self, formats):
        """ formats is a dict { loglevel : logformat } """
        self.formatters = {}
        for loglevel in formats:
            self.formatters[loglevel] = logging.Formatter(formats[loglevel])

    def format(self, record):
        formatter = self.formatters.get(record.levelno, self.default_formatter)
        return formatter.format(record)


#
# How we should print messages based upon the level

formatter = VarFormatter({logging.INFO: "%(message)s",
                          logging.WARNING: "WARNING: %(message)s",
                          logging.ERROR: "ERROR: %(asctime)s %(message)s",
                          logging.DEBUG: "DEBUG: %(asctime)s [%(filename)s:%(l\
ineno)s - %(funcName)20s() ] %(message)s"})

# Get the logging handler

log = logging.getLogger('hammerspace.hammerclient')
level = logging.DEBUG

# If we don't have a handler set up, then we will create a streaming handler
# to the console

if not log.hasHandlers():

    # Set the level

    log.setLevel(level=level)

    # Configure a console handler

    console = logging.StreamHandler()
    console.setLevel(level=level)
    console.setFormatter(formatter)
    log.addHandler(console)
    new_level = logging.getLevelName(level).upper()

    # Put out a simple 'Hello' message

    log.debug("Logger Initialized")
    log.debug(f"Level - '{new_level}'")
