"""
POWERLAUNCH

Ready...Aim...POWER!

With this minigame, power up Cozmo and launch your little buddy towards a cube tower target! Don't worry, you can't hurt him - powerlaunching is one of Cozmo's favorites.

This is a variation on an archery or golf minigame.
"""

import cozmo
from cozmo.util import distance_mm, speed_mmps, degrees

import color_cycle
import random
import time
import sys



def drive_cozmo_distance_angle(robot: cozmo.robot.Robot, distance, speed, angle=0):

	robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

	#to do: add turning at an angle to increase game difficulty

class PowerlaunchGame(object):
	
	def __init__(self):

		self.list_of_identified_cubes = []
		self.random_distance_from_target = None
		self.user_defined_launch_power = None
		self.launch_distance = None
		self.did_win = None

	def identify_cubes_and_create_list(self, robot: cozmo.robot.Robot):

		for attempt in range(3):

			lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
			print("\n-------->Cozmo is helping by setting up the cube stack as a target.", "Try", attempt + 1, "of 3.")

			self.list_of_identified_cubes = robot.world.wait_until_observe_num_objects(num=2, object_type=cozmo.objects.LightCube, timeout=10)
			print("cubes identified", self.list_of_identified_cubes)

			lookaround.stop()

			if len(self.list_of_identified_cubes) < 2:
				print("Error: need 2 Cubes but only found", len(self.list_of_identified_cubes), "Cube(s)")
			else:
				print("returning list of", len(self.list_of_identified_cubes), "cubes:", self.list_of_identified_cubes)
				print("\n-------->Cozmo found his cubes! He'll stack them to make our target.")
				return
		print("\n-------->Cozmo didn't find the cubes after 3 tries. He's a bit astigmatic. He'll be okay - but try putting the cubes farther away from his power station.")
		input("\n-------->Press enter to quit game. Then reposition the cubes and rerun the game.")
		sys.exit()

	def stack_cubes(self, robot: cozmo.robot.Robot):

		for attempt in range(3):

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
				print("returning list of", len(self.list_of_identified_cubes), "cubes:", self.list_of_identified_cubes)
				print("\n-------->Cozmo found his cubes! He'll stack them to make our target.")
				return
		print("\n-------->Cozmo didn't stack is cubes correctly after 3 tries.")
		input("\n-------->Press enter to quit game. Then place him on his charging station and rerun the game.")
		sys.exit()             


	def make_cube_cycle_through_colors(self, robot: cozmo.robot.Robot, cycle_time_in_seconds, cube, cycle_speed):

		color_cycle.run_color_cycle(robot, cycle_time_in_seconds, cube, cycle_speed)


	def move_into_launch_position(self, robot: cozmo.robot.Robot, distance_range_tuple, angle_range_tuple):

		#creates random distance away from target, within distance range
		self.random_distance_from_target = random.randint(distance_range_tuple[0], distance_range_tuple[1])
		print("moving", self.random_distance_from_target, "mm away from target")

		drive_cozmo_distance_angle(robot, -(self.random_distance_from_target), 50)


	def launch_cozmo_towards_target(self, robot: cozmo.robot.Robot, distance_range_tuple, angle_range_tuple, tunable_margin_of_error=0):

		#power 1 = 0% over smallest disance in range. power 10 = at 100% largest distance in range.
		launch_distance_percent_max = (self.user_defined_launch_power-1) * (1/9)
		print("launch distance travelled within range (percent of max possible within range):", launch_distance_percent_max)

		#distance the min distance in range, plus a percentange of the distance range
		self.launch_distance = (launch_distance_percent_max * (distance_range_tuple[1]-distance_range_tuple[0])) + distance_range_tuple[0]
		print("launch distance:", self.launch_distance)

		#speed is faster with higher power, but does not affect distance traveled
		launch_speed = 10 + (20 * self.user_defined_launch_power)
		print("launch speed:", launch_speed)

		drive_cozmo_distance_angle(robot, (self.launch_distance), launch_speed)

		offset_from_target = self.launch_distance - self.random_distance_from_target
		print("missed target by", offset_from_target)

		if abs(offset_from_target) <= tunable_margin_of_error:
			self.did_win = "win"
			print("missed target by", offset_from_target, "within acceptable margin of error of", tunable_margin_of_error)
		elif offset_from_target < 0:
			self.did_win = "under"
			print("missed target by", offset_from_target, "which is under acceptable margin of error of", tunable_margin_of_error)
		else:
			self.did_win = "over"
			print("missed target by", offset_from_target, "which is over acceptable margin of error of", tunable_margin_of_error)


def cozmo_program(robot: cozmo.robot.Robot):

#DESIGN TUNING
	distance_range_tuple = (100, 300)
	angle_range_tuple = (0, 0)
	tunable_margin_of_error = 10


	user_menu_input = None

#assumes cozmo is on charging station, and drives off
	drive_cozmo_distance_angle(robot, 150, 50)

	robot.play_anim("anim_launch_cubediscovery", in_parallel=True)

	user_menu_input = input("\n\n\n-------->Welcome to Powerlaunch!\n\n-------->The goal is to topple a cube stack by powering up Cozmo with just the right amount of electroids.\n-------->After Cozmo gets a cube stack ready, take aim, and decide how much power.\n-------->Careful not to be underpowered or overpowered!\n\n-------->Press return to begin.")

	while user_menu_input != "q":

		new_game = PowerlaunchGame()

		new_game.identify_cubes_and_create_list(robot)

		new_game.stack_cubes(robot)

		robot.play_anim("anim_launch_cubediscovery", in_parallel=True)

		new_game.make_cube_cycle_through_colors(robot, .5, new_game.list_of_identified_cubes[0], 0.003)

		robot.play_anim("anim_reacttocliff_edge_01", in_parallel=True).wait_for_completed()
		#gets cozmo right next to target
		drive_cozmo_distance_angle(robot, 70, 50)
		robot.turn_in_place(degrees(5)).wait_for_completed()

		new_game.did_win = None

		while new_game.did_win != "win":

			new_game.move_into_launch_position(robot, distance_range_tuple, angle_range_tuple)

			new_game.user_defined_launch_power = int(input("\n\n\n-------->Time to Powerlaunch!\n-------->Remember, too little power and he won't reach the target.\n-------->Too much and he'll be overpowered!\n\n-------->How many electroids will you give Cozmo (1-10)? "))
			print("-------->Charging Cozmo with", new_game.user_defined_launch_power, "electroids!\n\n\n")

			robot.set_all_backpack_lights(cozmo.lights.blue_light)
			# robot.play_anim("anim_sparking_getin_01").wait_for_completed()
			# animation is for cozmo to "power up". Commenting out because it makes him turn at an angle.
			
			new_game.launch_cozmo_towards_target(robot, distance_range_tuple, angle_range_tuple, tunable_margin_of_error)
			robot.set_backpack_lights_off()
			
			if new_game.did_win == "win":

				# get close enough to FLIP it
				drive_cozmo_distance_angle(robot, 30, 100)
				robot.set_lift_height(1, duration=0.2).wait_for_completed()
				# do the flipping
				drive_cozmo_distance_angle(robot, 20, 100)
				robot.set_lift_height(0, duration=1.2).wait_for_completed()
				robot.play_anim("anim_reacttoblock_success_01", in_parallel=True) 

				user_menu_input = input('\n\n\n-------->You and Cozmo won! Press "return" to play again! Press "q" to quit.\n\n\n')

			elif new_game.did_win == "under":

				robot.play_anim("anim_rtpmemorymatch_no_01").wait_for_completed()
				robot.turn_in_place(degrees(3)).wait_for_completed()

				user_menu_input = input('\n\n\n-------->Not enough power! Press "return" to try again! Press "q" to quit.\n\n\n')
				#moves Cozmo to cube so he can restart game
				drive_cozmo_distance_angle(robot, (new_game.random_distance_from_target - new_game.launch_distance + 50), 50)

			else:
				robot.play_anim("anim_rtpmemorymatch_no_01").wait_for_completed()
				robot.turn_in_place(degrees(3)).wait_for_completed()

				user_menu_input = input('\n\n\n-------->Careful! Too much power! Press "return" to try again! Press "q" to quit.\n\n\n')



if __name__ == '__main__':

	cozmo.run_program(cozmo_program)


