#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Make Cozmo stack Cubes.

This script is meant to show off how easy it is to do high level robot actions.
Cozmo will wait until he sees two Cubes, and then will pick up one and place it on the other.
He will pick up the first one he sees, and place it on the second one.
'''

import cozmo

def identify_cubes_and_return_list(robot: cozmo.robot.Robot):
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    print("looking around")

    list_of_identified_cubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=60)
    print("cubes identified", list_of_identified_cubes)

    lookaround.stop()

    if len(list_of_identified_cubes) < 2:
        print("Error: need 2 Cubes but only found", len(cubes), "Cube(s)")
    else:
        print("returning list of", len(list_of_identified_cubes), "cubes:", list_of_identified_cubes)
        return list_of_identified_cubes

        # current_action = robot.pickup_object(list_of_identified_cubes[0])
        # current_action.wait_for_completed()
        # if current_action.has_failed:
        #     code, reason = current_action.failure_reason
        #     print("Pickup Cube failed: code=%s reason=%s" % (code, reason))

        # current_action = robot.place_on_object(list_of_identified_cubes[1])
        # current_action.wait_for_completed()
        # if current_action.has_failed:
        #     code, reason = current_action.failure_reason
        #     print("Place On Cube failed: code=%s reason=%s" % (code, reason))

def stack_cubes(robot: cozmo.robot.Robot, list_of_identified_cubes):

    current_action = robot.pickup_object(list_of_identified_cubes[0])
    current_action.wait_for_completed()
    if current_action.has_failed:
        code, reason = current_action.failure_reason
        print("Pickup Cube failed: code=%s reason=%s" % (code, reason))

    current_action = robot.place_on_object(list_of_identified_cubes[1])
    current_action.wait_for_completed()
    if current_action.has_failed:
        code, reason = current_action.failure_reason
        print("Place On Cube failed: code=%s reason=%s" % (code, reason))


if __name__ == '__main__':
    list_of_identified_cubes = cozmo.run_program(identify_cubes_and_return_list)
    print(list_of_identified_cubes)
    # stack_cubes(robot, list_of_identified_cubes)
