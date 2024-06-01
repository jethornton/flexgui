import re

from OpenGL import GL
from OpenGL import GLU

from PyQt6.QtGui import QColor
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer

import glnav
from rs274 import glcanon
from rs274 import interpret
import linuxcnc
import gcode

class graphics(QOpenGLWidget, glcanon.GlCanonDraw, glnav.GlNavBase):
	def __init__(self, parent=None):
		super().__init__()
		glnav.GlNavBase.__init__(self)

		'''
		self.status = linuxcnc.stat()
		self.status.poll()
		self.ini_filename = self.status.ini_filename
		self.inifile = linuxcnc.ini(self.ini_filename)

		trajcoordinates = self.inifile.find("TRAJ", "COORDINATES").lower().replace(" ","")
		kinsmodule = self.inifile.find("KINS", "KINEMATICS")
		self.foam_option = bool(self.inifile.find("DISPLAY", "FOAM")) or False
		self.lathe_option = self.inifile.find("DISPLAY", "LATHE") or False

		self.current_stat = ()

		# setup and start the status update timer every 0.01 second
		self.timer = QTimer()
		self.timer.timeout.connect(self.poll)
		self.timer.start(10) # milliseconds

		#self.load_preview()
		'''
	def load_preview(self):
		canon = StatCanon(self.colors,
			self.get_geometry(),
			self.foam_option,
			self.lathe_option,
			s, text, random, i,
			progress, arcdivision)


	def poll(self): # check for a change and if changed update plot
		s = self.status
		s.poll()
		current = (s.actual_position, s.joint_actual_position, s.homed,
			s.g5x_offset, s.g92_offset, s.limit, s.tool_in_spindle,
			s.motion_mode, s.current_vel)
		if current != self.current_stat:
			self.current_stat = current

	# called when widget is completely redrawn
	def initializeGL(self):
		#self.realize()
		GL.glEnable(GL.GL_CULL_FACE)
		return

	def get_geometry(self):
		temp = self.inifile.find("DISPLAY", "GEOMETRY") or 'XYZABCUVW'
		print(temp)
		if temp:
			_geometry = re.split(" *(-?[XYZABCUVW])", temp.upper())
			self._geometry = "".join(reversed(_geometry))
		else:
			self._geometry = 'XYZABCUVW'
		print(self._geometry)
		return self._geometry



class StatCanon(glcanon.GLCanon, interpret.StatMixin):
	def __init__(self, colors, geometry, is_foam, lathe_view_option, stat, random, text, linecount, progress, arcdivision):
		glcanon.GLCanon.__init__(self, colors, geometry, is_foam)
		interpret.StatMixin.__init__(self, stat, random)
		self.lathe_view_option = lathe_view_option
		self.text = text
		self.linecount = linecount
		self.progress = progress
		self.aborted = False
		self.arcdivision = arcdivision




