"""
POWERLAUNCH

With this minigame, power up Cozmo and launch your little buddy towards a target! Don't worry, you can't hurt him - powerboosing is one of Cozmo's favorites.

This is a variation on an archery or golf minigame.
"""

import cozmo
from cozmo.util import distance_mm, speed_mmps

import asyncio
import sys
import time

def make_cube_cycle_through_colors(robot: cozmo.robot.Robot):

    #Set up an RGB array
    set_rgb = [255,0,0]  	#start with red
    decColor = 0  		#This variable will decrement one of the RGB values
    incColor = decColor + 1     #This variable will increment one of the RGB values

   #Find a Light Cube to color
    cube = None
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    try:
    	cube = robot.world.wait_for_observed_light_cube(timeout=60)
    except asyncio.TimeoutError:
        print("Didn't find a cube :-(")
        return
    finally:
        look_around.stop()
    
    #Cycle the Light Cube colors
    for y in range(0,10): #repeat the color cycle 10 times
    	for x in range(1, 254): # 0 - 255 is the full range, but this looks smoother
    		
    		#cross-fade between the two values
    		set_rgb[decColor] -= 1 #decrement this rgb value
    		set_rgb[incColor] += 1 #increment this rgb value
			
		#create a light color and tell the cube to display it
    		new_color = cozmo.lights.Color(rgb=(set_rgb[0],set_rgb[1],set_rgb[2]))
    		new_light = cozmo.lights.Light(on_color=new_color)
    		cube.set_lights(new_light)
    		
    		#wait for a moment to see the change
    		time.sleep(0.005) 
    	
    	#pick the next RGB value to decrement and increment
    	decColor = decColor + 1
    	incColor = incColor + 1  
    	
    	# handle the wrap around cases
    	if decColor == 3: 
    		decColor = 0
    	elif incColor == 3:
    	    incColor = 0  

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