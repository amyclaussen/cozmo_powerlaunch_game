"""
POWERLAUNCH

With this minigame, power up Cozmo and launch your little buddy towards a target! Don't worry, you can't hurt him - powerboosing is one of Cozmo's favorites.

This is a variation on an archery or golf minigame.
"""

import cozmo
from cozmo.util import distance_mm, speed_mmps

import color_cycle

class PowerlaunchGame:

    def __init__(self):
        self.list_of_identified_cubes = []

    def identify_cubes_and_create_list(robot: cozmo.robot.Robot):
        lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        print("looking around")

        PowerlaunchGame.list_of_identified_cubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=60)
        print("cubes identified", PowerlaunchGame.list_of_identified_cubes)

        lookaround.stop()

        if len(PowerlaunchGame.list_of_identified_cubes) < 2:
            print("Error: need 2 Cubes but only found", len(PowerlaunchGame.list_of_identified_cubes), "Cube(s)")
        else:
            print("returning list of", len(PowerlaunchGame.list_of_identified_cubes), "cubes:", PowerlaunchGame.list_of_identified_cubes)


def make_cube_cycle_through_colors(robot: cozmo.robot.Robot):

    color_cycle.run_color_cycle(robot, 10)

def stop_on_color_when_tap_cube(robot: cozmo.robot.Robot):
	pass

def determine_launch_force_based_on_cube_color(robot: cozmo.robot.Robot):
	pass

def launch_cozmo_forward(robot: cozmo.robot.Robot, distance, speed):

	robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()


def cozmo_program(robot: cozmo.robot.Robot):

	# launch_cozmo_forward(robot, 150, 50)

	# make_cube_cycle_through_colors(robot)

    # cozmo.behavior.BehaviorTypes

    PowerlaunchGame.identify_cubes_and_create_list(robot)


cozmo.run_program(cozmo_program)

