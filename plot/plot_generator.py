#!/usr/bin/env python3
import os
import shutil
import tempfile
import linuxcnc
import gcode

def float_fmt(f):
	if isinstance(f, float): return "% 5.1g" % f
	return "%5s" % f

class Canon:
	def __getattr__(self, attr):
		"""Assume that any unknown attribute is a canon call; just print
		its args and return None"""

		def inner(*args):
			args = list(map(float_fmt, args))
			print("%-17s %s" % (attr, " ".join(args)))
		return inner

	def next_line(self, linecode): 
		pass

	# These can't just return None...
	def get_external_length_units(self): return 1.0
	def get_external_angular_units(self): return 1.0
	def get_axis_mask(self): return 7 # (x y z)
	def get_block_delete(self): return False
	def get_tool(self, pocket):
		return -1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0

class PlotGenerator:

	def __init__(self, inifile):
		self.inifile = linuxcnc.ini(inifile)
		self.inifile_path = os.path.split(inifile)[0]

	def load(self, filename = None):
		linuxcnc.command().task_plan_synch()
		s = linuxcnc.stat()
		s.poll()
		unitcode = "G%d" % (20 + (s.linear_units == 1))
		initcode = self.inifile.find("RS274NGC", "RS274NGC_STARTUP_CODE") or ""

		canon = Canon()
		parameter = tempfile.NamedTemporaryFile()
		canon.parameter_file = parameter.name
		result, seq = gcode.parse(filename, canon, unitcode, initcode, '')
		if result > gcode.MIN_ERROR: 
			raise SystemExit(gcode.strerror(result))


if __name__ == "__main__":
	bp = PlotGenerator('/home/john/linuxcnc/configs/flex_examples/xyzh.ini')
	print(bp.load('/home/john/linuxcnc/nc_files/simple.ngc'))




