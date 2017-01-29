"""
POWERLAUNCH

Ready...Aim...POWER!

With this minigame, power up Cozmo and launch your little buddy towards a cube tower target! Don't worry, you can't hurt him - powerlaunching is one of Cozmo's favorites.

This is a variation on an archery or golf minigame.
"""

#to do: add "no animation" version for demo

import cozmo
from cozmo.util import distance_mm, speed_mmps, degrees

import color_cycle
import random
import time
import sys



def drive_cozmo_distance_angle(robot: cozmo.robot.Robot, distance, speed, angle=0):

	robot.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()

	#to do: add turning at an angle

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

		#moves cozmo a random distance away from target, within distance range. The -30 is to account for movement during the cubediscovery animation.
		drive_cozmo_distance_angle(robot, -(self.random_distance_from_target - 60), 50)


	def launch_cozmo_towards_target(self, robot: cozmo.robot.Robot, distance_range_tuple, angle_range_tuple):

		#power 1 = 0% over smallest disance in range. power 10 = at 100% largest distance in range.
		launch_distance_percent_max = (self.user_defined_launch_power-1) * (1/9)
		print("launch distance travelled within range (percent of max possible within range):", launch_distance_percent_max)

		#distance the min distance in range, plus a percentange of the distance range
		self.launch_distance = (launch_distance_percent_max * (distance_range_tuple[1]-distance_range_tuple[0])) + distance_range_tuple[0]
		print("launch distance:", self.launch_distance)

		#speed is faster with higher power, but does not affect distance traveled
		launch_speed = 10 + (20 * self.user_defined_launch_power)
		print("launch speed:", launch_speed)

		drive_cozmo_distance_angle(robot, self.launch_distance, launch_speed)

		if self.random_distance_from_target - 5 <= self.launch_distance >= self.random_distance_from_target + 5:
			self.did_win = "win"
		elif self.launch_distance < self.random_distance_from_target - 5:
			self.did_win = "under"
		else:
			self.did_win = "over"


def cozmo_program(robot: cozmo.robot.Robot):

	distance_range_tuple = (100, 300)
	angle_range_tuple = (0, 0)
	#to do: put the margin of error in the tuning, not the launch_cozmo_towards_target method

	user_menu_input = None

	drive_cozmo_distance_angle(robot, 150, 50)

	robot.play_anim("anim_reacttoblock_success_01", in_parallel=True)

	user_menu_input = input("\n\n\n-------->Welcome to Powerlaunch!\n\n-------->The goal is to topple a cube stack by powering up Cozmo with just the right amount of electroids.\n-------->After Cozmo gets a cube stack ready, take aim, and decide how much power.\n-------->Careful not to be underpowered or overpowered!\n\n-------->Press return to begin.")

	while user_menu_input != "q":

		new_game = PowerlaunchGame()

		new_game.identify_cubes_and_create_list(robot)

		new_game.stack_cubes(robot)

		robot.play_anim("anim_launch_cubediscovery", in_parallel=True)

		new_game.make_cube_cycle_through_colors(robot, 4, new_game.list_of_identified_cubes[0], 0.003)

		new_game.did_win = None

		while new_game.did_win != "win":

			new_game.move_into_launch_position(robot, distance_range_tuple, angle_range_tuple)

			robot.play_anim("anim_launch_cubediscovery")

			new_game.user_defined_launch_power = int(input("\n\n\n-------->Time to Powerlaunch!\n-------->Remember, too little power and he won't reach the target.\n-------->Too much and he'll be overpowered!\n\n-------->How many electroids will you give Cozmo (1-10)? "))
			print("-------->Charging Cozmo with", new_game.user_defined_launch_power, "electroids!\n\n\n")

			robot.play_anim("anim_sparking_getin_01").wait_for_completed()
			#turns cozmo to correct for movement during animation.
			#to do: remove "wait for completed" redunancies. look at SDK for info on parallel and WFC.
			robot.turn_in_place(degrees(-27)).wait_for_completed()
			
			new_game.launch_cozmo_towards_target(robot, distance_range_tuple, angle_range_tuple)

			robot.play_anim("anim_keepaway_fakeout_06").wait_for_completed()

			if new_game.did_win == "win":
				
				robot.play_anim("anim_reacttoblock_success_01", in_parallel=True).wait_for_completed() #to do: look up in parallel
				#to do: sometimes he doesn't flip the cube right

				new_game.make_cube_cycle_through_colors(robot, 4, new_game.list_of_identified_cubes[0], 0.001)

				user_menu_input = input('\n\n\n-------->You and Cozmo won! Press "return" to play again! Press "q" to quit.\n\n\n')

				break

			elif new_game.did_win == "under":

				robot.play_anim("anim_rtpmemorymatch_no_01", in_parallel=True)

				user_menu_input = input('\n\n\n-------->Not enough power! Press "return" to try again! Press "q" to quit.\n\n\n')
				#moves Cozmo to cube so he can restart game
				robot.turn_in_place(degrees(5)).wait_for_completed()
				drive_cozmo_distance_angle(robot, (new_game.random_distance_from_target - new_game.launch_distance + 60), 50)

				break

			else:
				#to do: going over registers as a win.
				#new_game.did_win == "over"
				#to do: the cozmo waits for the light cycle to be dome before continuing on
				robot.play_anim("anim_rtpmemorymatch_no_01", in_parallel=True)

				user_menu_input = input('\n\n\n-------->Careful! Too much power! Press "return" to try again! Press "q" to quit.\n\n\n')

				break


if __name__ == '__main__':

	cozmo.run_program(cozmo_program)


