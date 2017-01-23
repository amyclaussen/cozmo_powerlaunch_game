"""
POWERLAUNCH

Ready...Aim...POWER!

With this minigame, power up Cozmo and launch your little buddy towards a cube tower target! Don't worry, you can't hurt him - powerlaunching is one of Cozmo's favorites.

This is a variation on an archery or golf minigame.
"""

import cozmo
from cozmo.util import distance_mm, speed_mmps

import color_cycle

import random

import time


def drive_cozmo_straight(robot: cozmo.robot.Robot, distance, speed):

	robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()


class PowerlaunchGame(object):
    
    def __init__(self):

    	self.list_of_identified_cubes = []
    	self.successfully_found_cubes_check = None
    	self.finished_stacking_cubes = None
    	self.random_distance_from_target = None
    	self.user_defined_launch_power = None
    	self.did_win = False

    def identify_cubes_and_create_list(self, robot: cozmo.robot.Robot):

        self.successfully_found_cubes_check = False

        while self.successfully_found_cubes_check == False:

            lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
            print("looking around")

            self.list_of_identified_cubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=60)
            print("cubes identified", self.list_of_identified_cubes)

            lookaround.stop()

            if len(self.list_of_identified_cubes) < 2:
                print("Error: need 2 Cubes but only found", len(self.list_of_identified_cubes), "Cube(s)")
            else:
                print("returning list of", len(self.list_of_identified_cubes), "cubes:", self.list_of_identified_cubes)
                self.successfully_found_cubes_check = True


    def stack_cubes(self, robot: cozmo.robot.Robot):

        self.finished_stacking_cubes = False

        while self.finished_stacking_cubes == False:

            current_action = robot.pickup_object(self.list_of_identified_cubes[0])
            current_action.wait_for_completed()
            if current_action.has_failed:
                code, reason = current_action.failure_reason
                print("Pickup Cube failed: code=%s reason=%s" % (code, reason))

            current_action = robot.place_on_object(self.list_of_identified_cubes[1])
            current_action.wait_for_completed()
            if current_action.has_failed:
                code, reason = current_action.failure_reason
                print("Place On Cube failed: code=%s reason=%s" % (code, reason))
            else:
            	self.finished_stacking_cubes = True                


    def make_cube_cycle_through_colors(self, robot: cozmo.robot.Robot, cycle_time_in_seconds, cube):

        color_cycle.run_color_cycle(robot, cycle_time_in_seconds, cube)


    def move_into_launch_position(self, robot: cozmo.robot.Robot, distance_range_tuple, angle_range_tuple):

    	#creates random distance away from target, within distance range
    	self.random_distance_from_target = random.randint(distance_range_tuple[0], distance_range_tuple[1])
    	print("moving", self.random_distance_from_target, "mm away from target")

    	#moves cozmo a random distance away from target, within distance range
    	drive_cozmo_straight(robot, -(self.random_distance_from_target), 50)


    def launch_cozmo_towards_target(self, robot: cozmo.robot.Robot, distance_range_tuple, angle_range_tuple):

    	#power 1 = 0% over smallest disance in range. power 10 = at 100% largest distance in range.
    	launch_distance_percent_max = (self.user_defined_launch_power-1) * (1/9)
    	print("launch distance percent of max possible:", launch_distance_percent_max)

    	#distance the min distance in range, plus a percentange of the distance range
    	launch_distance = (launch_distance_percent_max * (distance_range_tuple[1]-distance_range_tuple[0])) + distance_range_tuple[0]
    	print("launch distance:", launch_distance)

    	#speed is faster with higher power, but does not affect distance traveled
    	launch_speed = 10 + (20 * self.user_defined_launch_power)
    	print("launch speed:", launch_speed)

    	drive_cozmo_straight(robot, launch_distance, launch_speed)

    	if launch_distance > self.random_distance_from_target:
    		self.did_win = True


def cozmo_program(robot: cozmo.robot.Robot):

	distance_range_tuple = (100, 300)
	angle_range_tuple = (0, 0)

	new_game = PowerlaunchGame()

	drive_cozmo_straight(robot, 150, 50)

	new_game.identify_cubes_and_create_list(robot)

	new_game.stack_cubes(robot)

	robot.play_anim("anim_explorer_getin_01", in_parallel=True)

	new_game.make_cube_cycle_through_colors(robot, 4, new_game.list_of_identified_cubes[0])

	new_game.move_into_launch_position(robot, distance_range_tuple, angle_range_tuple)

	new_game.user_defined_launch_power = int(input("\n\n\n-------->POWER! How many electroids will you give Cozmo (1-10)? "))
	print("-------->Charging Cozmo with", new_game.user_defined_launch_power, "electroids!\n\n\n")
	
	new_game.launch_cozmo_towards_target(robot, distance_range_tuple, angle_range_tuple)

	robot.play_anim("anim_keepaway_fakeout_06").wait_for_completed()

	if new_game.did_win:
	    print("You and Cozmo Win!")
	    robot.play_anim_trigger(cozmo.anim.Triggers.NamedFaceInitialGreeting).wait_for_completed()
	else:
		print("Try Again!")

cozmo.run_program(cozmo_program)


