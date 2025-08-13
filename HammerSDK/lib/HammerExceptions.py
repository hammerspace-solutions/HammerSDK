#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2024 Hammerspace, Inc
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
# HammerExceptions.py
#
# Generally, the API generates its own exceptions. However, there are times in which
# the API will always return a 200 code (all is good), but the data returned contains
# an error. For those cases, the SDK will generate an exception.

# Expression Validation Error

class ExpressionValidationFailure(Exception):

    def __init__(self, line=None, column=None, message=""):
        self.line = line
        self.column = column
        self.message = message

    def __str__(self):
        return f"Invalid Expression @ Line {self.line}, Column {self.column}, Message: {self.message}"


# Get local site doesn't exist - This is a new call in Thor2. It can be executed without
# first logging in to the API. This was required so that we could get the site uuid
# and software version in order to check them.

class LocalSiteEndpointDoesNotExist(Exception):

    def __str__(self):
        return f"(GET) Local Site API call does not exist in this version"


# Invalid SDK Version

class InvalidSDKVersion(Exception):

    def __init__(self, sdk_version, anvil_version):
        self.sdk_version = sdk_version
        self.anvil_version = anvil_version

    def __str__(self):
        return f"Invalid SDK Version. Anvil={self.anvil_version}, SDK={self.sdk_version}"


# Invalid SDK Arguments Given

class InvalidSDKArgumentsGiven(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Invalid arguments to SDK: {self.msg}"


# Volume Base Exception

class VolumeException(Exception):

    def __init__(self, volume_name: str, resp: str = None):
        self.volume_name = volume_name
        self.response = resp

    def __str__(self):
        return f"Volume {self.volume_name}"


# Volume was in use

class VolumeWasUsed(VolumeException):

    def __str__(self):
        return f"Volume {self.volume_name} was previously in use. Use 'force' to override"


# Volume not decommissioned

class VolumeNotDecommissioned(VolumeException):

    def __str__(self):
        return f"Volume {self.volume_name} must be decommissioned first"


# Volume is being decommissioned

class VolumeDecommissioning(VolumeException):

    def __str__(self):
        return f"Volume {self.volume_name} is being decommissioned"


# Objective Base Exception

class ObjectiveException(Exception):

    def __init__(self, objective_name: str):
        self.objective_name = objective_name

    def __str__(self):
        return f"Objective {self.objective_name}"


# Objective has an invalid priority

class ObjectiveInvalidPriority(ObjectiveException):

    def __init__(self, objective_name: str, priority: str):
        super().__init__(objective_name)
        self.priority = priority

    def __str__(self):
        return f"Objective {self.objective_name} has invalid priority: {self.priority}"


# Objective has a cost dictionary

class ObjectiveInvalidCost(ObjectiveException):

    def __str__(self):
        return f"Objective {self.objective_name} has invalid cost dictionary"


# Objective has an invalid storage size

class ObjectiveInvalidStorageSize(ObjectiveException):

    def __init__(self, objective_name: str, size: str):
        super().__init__(objective_name)
        self.size = size

    def __str__(self):
        return f"Objective {self.objective_name} has invalid storage size of {self.size}"


# Objective has invalid place-on structure

class ObjectiveInvalidPlaceon(ObjectiveException):

    def __init__(self, objective_name: str, item: str):
        super().__init__(objective_name)
        self.item = item

    def __str__(self):
        return f"Place-on for Objective {self.objective_name} is malformed.  {self.item}"


# Objective has invalid confine-to or exclude-from structure

class ObjectiveInvalidConfineExclude(ObjectiveException):

    def __init__(self, objective_name: str, item: str):
        super().__init__(objective_name)
        self.item = item

    def __str__(self):
        return f"Confine-to or Exclude-from for Objective {self.objective_name} is malformed.  {self.item}"


# Objective - cannot add applied objective and place-on, confine-to, or exclude-from
# at the same time

class ObjectiveInvalidAppliedObjective(ObjectiveException):

    def __init__(self, objective_name: str, item: str):
        super().__init__(objective_name)
        self.item = item

    def __str__(self):
        return f"Objective {self.objective_name}: {self.item}"
