import asyncio
import sys
import time
import cozmo

def run_color_cycle(robot: cozmo.robot.Robot, cycle_time_in_seconds, cube, cycle_speed):
    
    #Set up an RGB array
    set_rgb = [255,0,0]  	#start with red
    decColor = 0  		#This variable will decrement one of the RGB values
    incColor = decColor + 1     #This variable will increment one of the RGB values
    
    #set number of seconds color will cycle
    time_light_cycle_ends = time.time() + cycle_time_in_seconds

    #Cycle the Light Cube colors
    while time.time() < time_light_cycle_ends:
        print("Seconds left until light cycle ends:", int(time_light_cycle_ends - time.time()))

        for x in range(1, 254): # 0 - 255 is the full range, but this looks smoother
    		
    		#cross-fade between the two values
            set_rgb[decColor] -= 1 #decrement this rgb value
            set_rgb[incColor] += 1 #increment this rgb value
			
		#create a light color and tell the cube to display it
            new_color = cozmo.lights.Color(rgb=(set_rgb[0],set_rgb[1],set_rgb[2]))
            new_light = cozmo.lights.Light(on_color=new_color)
            cube.set_lights(new_light)
    		
    		#wait for a moment to see the change
            time.sleep(cycle_speed) 
    	
    	#pick the next RGB value to decrement and increment
        decColor = decColor + 1
        incColor = incColor + 1  
    	
    	# handle the wrap around cases
        if decColor == 3: 
            decColor = 0
        elif incColor == 3:
            incColor = 0  
    
if __name__ == '__main__':
    
    cozmo.run_program(run_color_cycle)