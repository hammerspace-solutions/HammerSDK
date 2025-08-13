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


import HammerSDK.lib.request as request
import json

from HammerSDK.lib.uri import UriBuilder
from HammerSDK.lib.HammerExceptions import (ObjectiveInvalidPriority,
                                            ObjectiveInvalidCost,
                                            ObjectiveInvalidStorageSize,
                                            ObjectiveInvalidPlaceon,
                                            ObjectiveInvalidConfineExclude,
                                            ObjectiveInvalidAppliedObjective)
from typing import Any, Optional, List, Dict, Iterable
from enum import Enum
from copy import deepcopy

# SDK Version

SDK_Version = "5.1.18"


# Build the priority enum list

class PriorityList(Enum):
    """
    List of valid priorities for objectives
    :meta private:
    """
    LOW = "LOW"
    MEDIUM_LOW = "MEDIUM LOW"
    MEDIUM = "MEDIUM"
    MEDIUM_HIGH = "MEDIUM HIGH"
    HIGH = "HIGH"


# Build the Storage size list

class StorageSizeList(Enum):
    """
    List of valid storage size types for objectives
    """
    MB = "MB"
    GB = "GB"
    TB = "TB"
    PB = "PB"


# Class to handle all the verifying and parsing for the place-on, confine-to,
# and exclude-from structures

class Placement:

    def __init__(self, name: str):

        # Name of objective... Used here for raising exceptions

        self.name = name

        # Store the place-on while we work on it

        self.place_on = {}

        # Store the confine-to or exclude-from while we work on it

        self.confine_exclude = {}

        # place-on keys

        self.placeon_keys = ["first", "second", "third"]

        # directive types (used for verifying the directives passed in as an aggument)

        self.builder_types = ["volumes", "volume-groups", "nodes"]

        # placeOn body

        self.place_on_body = {
            "placeOn": []
        }

        # volume group structure

        self.volume_group_body = {
            "_type": "VOLUME_GROUP",
            "name": None
        }

        # volume structure

        self.volume_body = {
            "_type": "VOLUME_LOCATION",
            "storageVolume": {
                "_type": "STORAGE_VOLUME",
                "name": None
            }
        }

        # node structure

        self.node_body = {
            "_type": "NODE_LOCATION",
            "node": {
                "_type": "NODE",
                "name": None
            }
        }

        # volume builder structure for place-on, confine-to, and exclude-from

        self.volume_builder = {
            "type": self.builder_types[0],
            "template_body": self.volume_body,
            "template_subbody": self.volume_body["storageVolume"]
        }

        # volume group builder structure for place-on, confine-to, and exclude-from

        self.volumegroup_builder = {
            "type": self.builder_types[1],
            "template_body": self.volume_group_body,
            "template_subbody": self.volume_group_body
        }

        # node builder structure for place-on, confine-to, and exclude-from

        self.node_builder = {
            "type": self.builder_types[2],
            "template_body": self.node_body,
            "template_subbody": self.node_body["node"]
        }

        # place-on builder structure

        self.placeon_builder = [
            {"first": [self.volume_builder, self.volumegroup_builder, self.node_builder]},
            {"second": [self.volume_builder, self.volumegroup_builder, self.node_builder]},
            {"third": [self.volume_builder, self.volumegroup_builder, self.node_builder]}
        ]

        # confine-to or exclude-from builder structure

        self.confine_exclude_builder = [self.volume_builder,
                                        self.volumegroup_builder,
                                        self.node_builder]

    # Validate the place-on json structure. We have to make sure that what a user
    # passes us will work

    def validate_place_on(self, json_data):

        self.place_on = json_data

        # Get all the keys in the place_on structure from json_data

        placeon_keys = list(self.place_on.keys())

        # There should be at least one key

        if len(placeon_keys) == 0:
            raise ObjectiveInvalidPlaceon(self.name, "No 'first', 'second' or 'third' in place_on keys")

        # Get all the placeon_keys passed in and make sure that each is formed correctly

        for field in placeon_keys:
            if field not in self.placeon_keys:
                raise ObjectiveInvalidPlaceon(self.name, f"'{field}' not a valid place-on key")

            # The items within either "first", "second" or "third" must be a list

            if not isinstance(self.place_on[field], list):
                raise ObjectiveInvalidPlaceon(self.name, f"Items in the '{field}' place-on group must be a list")

            # THe items referenced by "first", "second", or "third" are lists of dictionaries

            for item in self.place_on[field]:
                if not isinstance(item, dict):
                    raise ObjectiveInvalidPlaceon(self.name,
                                                  f"This item in the '{field}' place-on group must be a" +
                                                  f" dictionary: {item}.")

                # Each item within the list of dictionaries must contain "volumes", "volume-groups", or "nodes"

                if not any(key in item for key in self.builder_types):
                    raise ObjectiveInvalidPlaceon(self.name,
                                                  f"The item in the '{field}' place-on group " +
                                                  f"must begin with either 'volumes', 'volume-groups', " +
                                                  f"or 'nodes'. The item is: {item}.")

                for key in self.builder_types:
                    directive_item = item.get(key, None)
                    if directive_item and not isinstance(directive_item, list):
                        raise ObjectiveInvalidPlaceon(self.name,
                                                      f"The items within '{key}' of the '{field}' place-on group" +
                                                      f" must be a list")

    # Validate the confine_to json structure. We have to make sure that what a user
    # passes us will work

    def validate_confine_exclude(self, json_data):

        self.confine_exclude = json_data

        # Validate that the keys are one of "volumes", "volume-groups", or "nodes"

        confine_exclude_keys = list(self.confine_exclude.keys())

        # There should be at least one key

        if len(confine_exclude_keys) == 0:
            raise ObjectiveInvalidConfineExclude(self.name,
                                                 "Confine-to or Exclude-from is invalid without any directives")

        for field in confine_exclude_keys:
            if field not in self.builder_types:
                item = self.confine_exclude[field]
                raise ObjectiveInvalidConfineExclude(self.name,
                                                     f"The item in the '{field}' confine-to or exclude-from group " +
                                                     f"must begin with either 'volumes', 'volume-groups', " +
                                                     f"or 'nodes'. The item is: {item}.")

            if not isinstance(self.confine_exclude[field], list):
                raise ObjectiveInvalidConfineExclude(self.name,
                                                     f"Items in the '{field}' confine-to or exclude-from group " +
                                                     "must be a list")

    # Process place-on arguments (validate and build structure)

    def process_placeon(self, placement_body: list):

        # Go through each item of the placeon_builder array and handle parsing
        # the placeon directive passed in... This can get a little complicated
        # and hence why we have this structure.
        #
        # We have to not only handle first, second, and third placeon directives, but also
        # volumes, volume groups, and/or nodes within each directive.

        all_keys = self._get_all_keys_in_order(self.placeon_builder)

        for key_item in all_keys:

            # Get a particular directive from a list of directives using a dictionary keys

            directives_list = self._get_directives(key_item, self.placeon_builder)
            placeon_directive = self.place_on.get(key_item, None)

            if placeon_directive:

                # Now, cycle through all the items in the items array. This contains
                # a list of structure to use to direct how to build for volumes,
                # volume groups, and nodes

                handle_directive = False
                location = []

                for item in directives_list:
                    entity_names = self._get_entity_names(item, "type", placeon_directive)
                    if entity_names:
                        location.extend(self._build_locations(item["template_body"],
                                                              item["template_subbody"],
                                                              entity_names))
                        handle_directive = True

                if handle_directive:
                    self.place_on_body["placeOn"] = location
                    placement_body.append(deepcopy(self.place_on_body))

    # Process confine-to and exclude-from arguments (validate and build structure)

    def process_confine_exclude(self) -> list:

        # Go through each item of builder array and handle parsing the confine-to
        # or exclude-from directive passed in... This can get a little complicated
        # and hence why we have this structure.
        #
        # We have to handle volumes, volume groups, and/or nodes within each directive.

        location = []

        for item in self.confine_exclude_builder:

            # Now, cycle through all the items in the items array. This contains
            # a list of structure to use to direct how to build for volumes,
            # volume groups, and nodes

            entity_names = self._get_entity_items(item, "type", self.confine_exclude)
            if entity_names:
                location.extend(self._build_locations(item["template_body"],
                                                      item["template_subbody"],
                                                      entity_names))

        return location

    # Build keys from a list of dictionarys

    def _get_all_keys_in_order(self, list_of_dicts):

        ordered_keys = []
        for dict_ in list_of_dicts:
            for key in dict_:
                if key not in ordered_keys:
                    ordered_keys.append(key)

        return ordered_keys

    # Get all the directives based upon the key in the list of dictionaries

    def _get_directives(self, key: str, list_of_dicts: list):

        directive_list = [d.get(key, None) for d in list_of_dicts]
        for directive in directive_list:
            if directive is not None:
                return directive

    # Build locations dictionary

    def _build_locations(self,
                         template_body: Dict[str, Any],
                         template_subbody: Dict[str, Any],
                         names: Iterable[str]) -> List[Dict[str, Any]]:

        locations = []

        for name in names:
            template_subbody["name"] = name
            locations.append(deepcopy(template_body))

        return locations

    # Get entity names in the placeon_directive

    def _get_entity_names(self,
                          directive_item: dict,
                          key: str,
                          placeon_directive: list) -> List[str]:

        entity_list = [entity.get(directive_item.get(key)) for entity in placeon_directive]

        # Now that we have the entity_names, get rid of any that might be None

        if entity_list:
            entities = [entity for entity in entity_list if entity is not None]
            if entities:
                return entities[0]

    # Get entity names in the confineto directive

    def _get_entity_items(self, directive_item: dict, key: str, confineto_directive: dict) -> List[str]:

        entities = []
        entity_names = []

        entity_names.extend(confineto_directive.get(directive_item.get(key)))

        # Now that we have the entity_names, get rid of any that might be None

        for entity in entity_names:
            if entity is not None:
                entities.append(entity)

        return entities


# Send a request and process the response. We have this routine because about 90%
# of the functions for objective processing have the same code

def _request_processing(conninfo: request.Connection, *args, **kwargs):

    response = conninfo.request(*args, **kwargs)

    # Only return json structure if there is really data to return. Otherwise,
    # return the entire response structure

    if response.text:
        return json.loads(json.dumps(response.json(), sort_keys=True))
    else:
        return response


# Validate the priority

def _objective_priority_check(priority, name):
    """
    Check the requested priority
    """

    if not priority:
        return "MEDIUM"
    else:
        priority_upper = priority.upper()

    for pri in PriorityList:
        if priority_upper == pri.value:
            return priority_upper
    else:
        raise ObjectiveInvalidPriority(name, priority_upper)


# Validate the cost structure

def _validate_cost(cost: dict, name: str):
    """
    validate cost dictionary
    """

    if not isinstance(cost, dict) or not cost.get("value") or not cost.get("size"):
        raise ObjectiveInvalidCost(name)

    for sz in StorageSizeList:
        if cost.get("size") == sz.value:
            return

    raise ObjectiveInvalidStorageSize(name, cost.get("size"))


# Validate the Applied Objective

def _validate_applied_objective(name: str, objectives: list):
    """
    validate applied objective list of dictionaries
    """

    # applied objective keys

    applied_objective_keys = ["applied", "type", "objective-name"]

    # applied objective types

    applied_objective_types = ["true", "always", "never"]

    for obj in objectives:

        # Validate each dictionary and make sure it is valid

        if not isinstance(obj, dict):
            raise ObjectiveInvalidAppliedObjective(name, f"Item for Applied Objective is not a dictionary." +
                                                   f"Item = {obj}")

        # Make sure that all the keys exist in every dictionary

        for key in applied_objective_keys:
            if key not in obj:
                raise ObjectiveInvalidAppliedObjective(name, f"The key '{key}' does not exist in 'Applied Objective" +
                                                       "dictionary")

        # Verify that the "type" is one of "true, "always", or "never"

        applied_type = obj["type"]
        if not isinstance(applied_type, str):
            raise ObjectiveInvalidAppliedObjective(name, f"The type must be a str type." +
                                                   f" Type discovered is '{type(applied_type)}'")

        applied_type = applied_type.lower()
        if applied_type not in applied_objective_types:
            raise ObjectiveInvalidAppliedObjective(name, f"The type must be one of 'always', 'true', " +
                                                   f"or 'never'. Type discovered is '{applied_type}'")


# Build the Applied Objective

def _build_applied_objective(name: str, objectives: list, applied_objective_body: dict):
    """
    Build applied objective from list of dictionaries previously verified
    """

    applied_objectives = []

    # applied objective keys

    applied_objective_keys = ["applied", "type", "objective-name"]

    # Cycle through all the applied objectives passed in

    for obj in objectives:

        # Start with the objective itself

        app_objective = obj[applied_objective_keys[0]]

        # We need to add the type to the applied objective

        app_type = obj[applied_objective_keys[1]].upper()
        app_objective = f"{app_objective}?{app_type}"

        # Build the applied objective structure from our pieces

        applied_objective_body["objective"]["name"] = obj[applied_objective_keys[2]]
        applied_objective_body["applicability"] = app_objective

        # Add the new applied objective to ouor list

        applied_objectives.append(deepcopy(applied_objective_body))

    return applied_objectives


# Create a share in the Hammerspace environment

@request.request
def create_objective(conninfo: request.Connection,
                     name: str,
                     priority: Optional[str] = None,
                     comment: Optional[str] = None,
                     durability: Optional[int] = None,
                     availability: Optional[int] = None,
                     cost: Optional[dict] = None,
                     place_on: Optional[dict] = None,
                     confine_to: Optional[dict] = None,
                     exclude_from: Optional[dict] = None,
                     applied_objectives: Optional[list] = None,
                     read_iops: Optional[int] = None,
                     read_thruput: Optional[int] = None,
                     read_resptime: Optional[int] = None,
                     write_iops: Optional[int] = None,
                     write_thruput: Optional[int] = None,
                     write_resptime: Optional[int] = None) -> Any:
    """
    Create an objective within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        name (str): Name of the objective
        priority (str, optional): Optional priority of the objective. Defaults to "Medium"
        comment (str, optional): Optional comment on the new share
        durability (int, optional): Optional durability of the data associated with the objective
        availability (int, optional): Optional availability of the data associated with the objective
        cost (dict, optional): Optional cost values for the objective
        place_on (dict, optional): Optional place-on directives for the objective
        confine_to (dict, optional): Optional confine-to directives for the objective
        exclude_from (dict, optional): Optional exclude-from directives for the objective
        applied_objectives (list, optional): Optional applied objectives for the objective
        read_iops (int, optional): Optional read iops for the objective
        read_thruput (int, optional): Optional read thruput for the objective
        read_resptime (int, optional): Optional read response time for the objective
        write_iops (int, optional): Optional write iops for the objective
        write_thruput (int, optional): Optional write thruput for the objective
        write_resptime (int, optional): Optional write response time for the objective

    Returns:
        json object: single objective

    Examples:

        | Simple example on how to create an objective

        | from HammerSDK.hammer_client import HammerClient
        | self.hammer_connection = HammerClient(self.host, self.port)
        | share_id = self.hammer_connection.objectives.create_objective(
        |      name="v-objective",
        |      comment="Keep most recently used files with a local copy",
        |      priority="High",
        |      durability=2,
        |      availability=3,
        |      cost={"value": "1.20", "size": "GB"},
        |      place_on={"first": [{"volume": "dsx-volume-1"}, {"volume": "dsx-volume-2"}],
        |                "second": [{"volume-group": "dsx-group"}]},
        |      confine_to={"volumes": ["dsx-volume-1", "dsx-volume-2"]},
        |      exclude_from={"nodes": ["dsx-3"]},
        |      write_thruput=274000000,
        |      read_thrupput=750000000)

        | Simple example on how to create an applied objective

        | from HammerSDK.hammer_client import HammerClient
        | self.hammer_connection = HammerClient(self.host, self.port)
        | share_id = self.hammer_connection.objectives.create_objective(
        |      name="v-applied-objective",
        |      comment="Create applied objective",
        |      applied_objectives=[{"applied": "LAST_USE_AGE<3*HOURS",
        |                           "type": "true",
        |                           "objective-name": "v-objective"}])

    """

    # Create the body

    objective_body = {
        "name": name,
        "basic": "true",
        "priority": _objective_priority_check(priority, name),
        "comment": comment
    }

    # protection

    protection_body = {
        "durability": durability,
        "availability": availability
    }

    # Performance

    read_performance_body = {
        "minThroughput": None,
        "minIops": None,
        "maxResponseTime": None
    }

    write_performance_body = {
        "minThroughput": None,
        "minIops": None,
        "maxResponseTime": None
    }

    # placementObjective

    placement_body = {
        "placeOnLocations": [],
        "excludeFrom": [],
        "confineTo": [],
        "allowedOnlineDelay": None,
        "doNotMove": None,
        "capacityOptimize": None
    }

    # applied objective structure

    applied_objective_body = {
      "objective": {
        "name": None
      },
      "applicability": None
    }

    method = 'POST'
    header = {'Accept': 'application/json'}
    uri = UriBuilder(path='/mgmt/v1.2/rest/objectives')

    # Start building the placement structure by creating a class to verify and parse various options like
    # place_on, confine_to, and exlcude_from

    placement = Placement(name)

    # Do we have a cost dictionary?

    if cost is not None:

        # Validate that the cost structure is good. Throw an exception if bad...

        _validate_cost(cost, name)

        # The cost structure is good... Fill in the values for the API

        objective_body["extendedInfo"] = {
            "unit": cost.get("size"),
            "unitCost": cost.get("value")
        }

    # Do we have a durability or availability argument?

    if availability is not None or durability is not None:
        objective_body["protection"] = protection_body

    # If there are place_on arguments, process them

    if place_on is not None:

        # Verify that the place_on structure is valid

        placement.validate_place_on(place_on)

        # Build structure for place-on. This will process the first, second, and third place-on
        # directives plus the volumes, volume groups, and nodes within each directive

        placement.process_placeon(placement_body["placeOnLocations"])

    # If there are confine_to arguments, process them

    if confine_to is not None:

        # Validate that the confine_to structure is valid

        placement.validate_confine_exclude(confine_to)

        # Build structure for confine-to. This will process volumes, volume groups, and nodes within each directive

        placement_body["confineTo"] = placement.process_confine_exclude()

    # If there are exclude_from arguments, process them

    if exclude_from is not None:

        # Validate the exclude_from structure is valid

        placement.validate_confine_exclude(exclude_from)

        # Build structure for exclude-from. This will process volumes, volume groups, and nodes within each directive

        placement_body["excludeFrom"] = placement.process_confine_exclude()

    # Do we have write performance metrics to add

    if write_iops is not None or write_thruput is not None or write_resptime is not None:
        write_performance_body["minIops"] = write_iops
        write_performance_body["minThroughput"] = write_thruput
        write_performance_body["maxResponseTime"] = write_resptime
        objective_body["writePerformance"] = write_performance_body

        # make sure to set the online delay to "online"... The default is forever and that doesn't work for
        # write or read performance metrics

        placement_body["allowedOnlineDelay"] = 0

    # Do we have read performance metrics to add

    if read_iops is not None or read_thruput is not None or read_resptime is not None:
        read_performance_body["minIops"] = read_iops
        read_performance_body["minThroughput"] = read_thruput
        read_performance_body["maxResponseTime"] = read_resptime
        objective_body["readPerformance"] = read_performance_body

        # make sure to set the online delay to "online"... The default is forever and that doesn't work for
        # write or read performance metrics

        placement_body["allowedOnlineDelay"] = 0

    # Add the placement_body into the objective

    objective_body["placementObjective"] = placement_body

    # Does the Applied Objective exist?

    if applied_objectives:

        # We cannot do anytging with an applied objective when either a place-on, confine-to, or exclude-from is set

        if place_on or confine_to or exclude_from:
            raise ObjectiveInvalidAppliedObjective(name, "An applied objective cannot be set when" +
                                                   "a place-on, confine-to, or exclude-from is defined")
        else:
            objective_body["basic"] = "false"
            _validate_applied_objective(name, applied_objectives)
            objective_body["appliedObjectives"] = _build_applied_objective(name,
                                                                           applied_objectives,
                                                                           applied_objective_body)

    # Used ONLY for debugging

    objective_info = json.dumps(objective_body, sort_keys=True, indent=4)

    # Send the request to the API

    return _request_processing(conninfo,
                               method,
                               str(uri),
                               headers=header,
                               body=objective_body,
                               request_content_type='application/json')


# Return all the objectives in the Hammerspace environment

@request.request
def list_objectives(conninfo: request.Connection) -> Any:
    """
    List all the objectives within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil

    Returns:
        List: objectives in json format
    """

    method = 'GET'
    uri = '/mgmt/v1.2/rest/objectives'
    header = {'Accept': 'application/json'}

    # Send the request to the API

    return _request_processing(conninfo, method, str(uri), headers=header)


# Get one particular objective from the Hammerspace environment

@request.request
def get_objective(conninfo: request.Connection, objective_id: str) -> Any:
    """
    Get a specific objective from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        objective_id (str): The uuid of the objective

    Returns:
        json object: single objective
    """

    method = 'GET'
    uri = f'/mgmt/v1.2/rest/objectives/{objective_id}'
    header = {'Accept': 'application/json'}

    # Send the request

    return _request_processing(conninfo, method, str(uri), headers=header)


# Delete one particular objective from the Hammerspace environment

@request.request
def delete_objective(conninfo: request.Connection, objective_id: str) -> Any:
    """
    Delete a specific objective from within a Hammerspace environment.

    Args:
        conninfo (request.Connection): Connection to the Hammerspace Anvil
        objective_id (str): The uuid of the objective

    Returns:
        json object: API REST response
    """

    method = 'DELETE'
    uri = f'/mgmt/v1.2/rest/objectives/{objective_id}'
    header = {'Accept': 'application/json'}

    # Send the request

    return _request_processing(conninfo, method, str(uri), headers=header)
