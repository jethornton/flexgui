#!/usr/bin/env python3

import tempfile

import linuxcnc
import gcode

class Canon:
	def __getattr__(self, attr):
		"""Assume that any unknown attribute is a canon call; just print
		its args and return None"""

		def inner(*args):
			#print(attr, args)
			# I assume open gl could be here
			if attr == 'straight_feed' or attr == 'straight_traverse':
				print(list(args)[:3])
		return inner

	def next_line(self, linecode): # just pass next_line
		pass

	# These can't just return None...
	def get_external_length_units(self): return 1.0
	def get_external_angular_units(self): return 1.0
	def get_axis_mask(self): return 7 # (x y z)
	def get_block_delete(self): return False
	def get_tool(self, pocket):
		return -1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0

class PlotGenerator:
	def __init__(self):
		self.stat = linuxcnc.stat()
		self.stat.poll()
		self.inifile = linuxcnc.ini(self.stat.ini_filename)

	def load(self, filename = None):
		linuxcnc.command().task_plan_synch()
		self.stat.poll()
		unitcode = f'G{20 + (self.stat.linear_units == 1)}'
		initcode = self.inifile.find("RS274NGC", "RS274NGC_STARTUP_CODE") or ""

		canon = Canon()
		parameter = tempfile.NamedTemporaryFile()
		canon.parameter_file = parameter.name
		result, seq = gcode.parse(filename, canon, unitcode, initcode, '')

		if result > gcode.MIN_ERROR: 
			raise SystemExit(gcode.strerror(result))

pg = PlotGenerator()
pg.load('/home/john/linuxcnc/nc_files/cube.ngc')
