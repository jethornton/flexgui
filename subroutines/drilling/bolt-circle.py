#!/usr/bin/env python3

import math
	
def generate_bolt_circle_gcode(diameter, num_holes, center_x, center_y, start_angle=0):
	"""Generates G-code for a bolt circle."""

	radius = diameter / 2
	angle_increment = 360 / num_holes
	gcode = []

	gcode.append("G90")  # Absolute positioning
	gcode.append("G00 X{} Y{}".format(center_x + radius * math.cos(math.radians(start_angle)), center_y + radius * math.sin(math.radians(start_angle))))

	for i in range(num_holes):
		angle = start_angle + i * angle_increment
		x = center_x + radius * math.cos(math.radians(angle))
		y = center_y + radius * math.sin(math.radians(angle))
		gcode.append("G01 X{} Y{}".format(x, y)) 
		gcode.append("G81 Z-5 R2 F100")  # Drilling cycle (adjust Z, R, and F as needed)

	gcode.append("G80")  # Cancel drilling cycle
	gcode.append("G00 X0 Y0")  # Return to origin

	return "\n".join(gcode)

if __name__ == "__main__":
	diameter = 2.5  # Diameter of the bolt circle
	num_holes = 4   # Number of holes
	center_x = 50   # X coordinate of the center
	center_y = 50   # Y coordinate of the center

	gcode = generate_bolt_circle_gcode(diameter, num_holes, center_x, center_y)
	print(gcode)


