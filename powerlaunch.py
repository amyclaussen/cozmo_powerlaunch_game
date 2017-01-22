"""
POWERLAUNCH

With this minigame, power up Cozmo and launch your little buddy towards a target! Don't worry, you can't hurt him - powerboosing is one of Cozmo's favorites.

This is a variation on an archery or golf minigame.
"""

import cozmo
from cozmo.util import distance_mm, speed_mmps

import color_cycle

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

	make_cube_cycle_through_colors(robot)


cozmo.run_program(cozmo_program)