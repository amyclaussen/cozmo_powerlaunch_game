"""
POWERLAUNCH

With this minigame, power up Cozmo and launch your little buddy towards a target! Don't worry, you can't hurt him - powerboosing is one of Cozmo's favorites.

This is a variation on an archery or golf minigame.
"""

import cozmo
from cozmo.util import distance_mm, speed_mmps


def make_block_cycle_through_colors():
	pass

def stop_on_color_when_tap_cube():

def launch_cozmo_forward(robot: cozmo.robot.Robot, distance, speed):

	robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()


def cozmo_program(robot: cozmo.robot.Robot):

	launch_cozmo_forward(robot, 150, 50)


cozmo.run_program(cozmo_program)