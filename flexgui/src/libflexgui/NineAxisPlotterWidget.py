import os
import sys
import linuxcnc
import gcode  # Native LinuxCNC G-code interpreter utility

from PyQt6.QtCore import Qt
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *

class NineAxisPlotterWidget(QOpenGLWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		try:
			self.lcnc_status = linuxcnc.stat()
		except linuxcnc.error:
			self.lcnc_status = None

		self.tool_path_history = []
		self.camera_distance = -150.0
		self.camera_rot_x = 30.0
		self.camera_rot_y = -45.0
		self.pan_offset_x = 0.0
		self.pan_offset_y = 0.0
		self.last_mouse_pos = None
		self.mouse_action = None

		# Load real travel dimensions from LinuxCNC INI file if available
		self.load_ini_boundaries()

		self.gcode_path_segments = []  # Holds the pre-parsed static G-code lines
		self.tool_path_history = []	# Holds the live machined history trail

	def load_gcode_path(self, filename):
		"""Parses a target G-code file using the native LinuxCNC canonical engine safely."""
		self.gcode_path_segments = []

		if not filename or not os.path.exists(filename):
			return

		try:
			class PathAccumulator:
				def __init__(self, target_list):
					self.target_list = target_list
					self.last_pt = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

				def straight_feed(self, line_no, x, y, z, a, b, c, u, v, w):
					pt = (x, y, z, u, v, w)
					self.target_list.append((self.last_pt, pt))
					self.last_pt = pt
					return 0  # CRITICAL: Must return a value so C doesn't treat callback as failed (NULL)

				def straight_traverse(self, line_no, x, y, z, a, b, c, u, v, w):
					pt = (x, y, z, u, v, w)
					self.target_list.append((self.last_pt, pt))
					self.last_pt = pt
					return 0

				def arc_feed(self, line_no, isa, iea, f_axis, s_axis, rot, end_pt, a, b, c, u, v, w):
					# Approximate arc endpoint fallback mapping for preview
					pt = (end_pt if f_axis==0 else isa, end_pt if f_axis==1 else iea, end_pt if f_axis==2 else 0.0, u, v, w)
					self.target_list.append((self.last_pt, pt))
					self.last_pt = pt
					return 0

				# Safe empty stubs returning integer 0 to satisfy internal C-binding checks
				def set_plane(self, plane): return 0
				def use_length_units(self, units): return 0
				def change_tool(self, pocket=0): return 0
				def select_tool(self, pocket=0): return 0
				def set_feed_rate(self, rate): return 0
				def set_traverse_rate(self, rate): return 0
				def set_feed_mode(self, mode, mode2=0): return 0
				def set_g5x_offset(self, sys, x, y, z, a, b, c, u, v, w): return 0
				def set_g92_offset(self, x, y, z, a, b, c, u, v, w): return 0
				def set_xy_rotation(self, angle): return 0
				def next_line(self, line_obj): return 0

			accumulator = PathAccumulator(self.gcode_path_segments)
			gcode.parse(filename, accumulator)
			print(f"NineAxisPlotter -> Pre-rendered {len(self.gcode_path_segments)} G-code path vectors.")
			self.update()
			
		except Exception as e:
			print(f"NineAxisPlotter -> G-code rendering error: {e}")

	def draw_gcode_preview(self):
		"""Draws the complete pre-parsed file path with bright yellow/gray contrast lines."""
		if not self.gcode_path_segments:
			return

		glLineWidth(2.0)
		glColor3f(1.0, 0.8, 0.0)  # Use high-visibility yellow/orange for file paths
		glBegin(GL_LINES)
		for start, end in self.gcode_path_segments:
			sx, sy, sz, su, sv, sw = start
			ex, ey, ez, eu, ev, ew = end
			glVertex3f(sx + su, sy + sv, sz + sw)
			glVertex3f(ex + eu, ey + ev, ez + ew)
		glEnd()
		glLineWidth(1.0)


	def load_ini_boundaries(self):
		"""Reads MIN_LIMIT and MAX_LIMIT dynamically for XYZ axes from the active INI file."""
		self.min_limits = [-50.0, -50.0, 0.0]
		self.max_limits = [50.0, 50.0, 50.0]
		
		ini_path = os.environ.get("INI_FILE_NAME", "")
		if ini_path and os.path.exists(ini_path):
			try:
				ini = linuxcnc.ini(ini_path)
				for i, axis in enumerate(['X', 'Y', 'Z']):
					sec = f"AXIS_{axis}"

					# LinuxCNC uses .find() to pull INI string data
					mn_str = ini.find(sec, "MIN_LIMIT")
					mx_str = ini.find(sec, "MAX_LIMIT")

					if mn_str is not None:
						self.min_limits[i] = float(mn_str)
					if mx_str is not None:
						self.max_limits[i] = float(mx_str)
			except Exception as e:
				print(f"Could not parse INI limits, using defaults: {e}")

		# Compute initial camera frame to fit 90% of the viewport
		self.fit_camera_to_bounds()

	def fit_camera_to_bounds(self):
		"""Calculates center offset and zoom distance to fit the bounding box at ~90% scale."""
		x_min, y_min, z_min = self.min_limits
		x_max, y_max, z_max = self.max_limits
		
		# Center of the machine workspace
		self.center_x = (x_min + x_max) / 2.0
		self.center_y = (y_min + y_max) / 2.0
		self.center_z = (z_min + z_max) / 2.0
		
		# Invert center offsets for translation matrix application (pans view to center machine)
		self.pan_offset_x = -self.center_x
		self.pan_offset_y = -self.center_y
		
		# Find the maximum span across X, Y, or Z to bound the object size
		max_span = max(x_max - x_min, y_max - y_min, z_max - z_min)
		if max_span <= 0:
			max_span = 100.0
			
		# FOV is 45 degrees. Half-angle in radians = 22.5 deg = 0.3926 rad.
		# We want the object (max_span) to occupy 90% of the view height/width projection.
		fov_factor = 0.3926  # tan(45° / 2)
		desired_radius = max_span / 0.90  # account for 90% view target padding
		self.camera_distance = - (desired_radius / fov_factor)

	def initializeGL(self):
		glClearColor(0.12, 0.12, 0.14, 1.0)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_LINE_SMOOTH)

	def resizeGL(self, width, height):
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45, width / max(1, height), 0.1, 1000.0)
		glMatrixMode(GL_MODELVIEW)

	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		glTranslatef(self.pan_offset_x, self.pan_offset_y, self.camera_distance)
		glRotatef(self.camera_rot_x, 1.0, 0.0, 0.0)
		glRotatef(self.camera_rot_y, 0.0, 1.0, 0.0)

		self.draw_workspace_grid()
		self.draw_dynamic_machine_boundary()

		if self.lcnc_status:
			try:
				self.lcnc_status.poll()
				pos = self.lcnc_status.actual_position
			except linuxcnc.error:
				pos = [0.0] * 9
		else:
			pos = [0.0] * 9

		self.tool_path_history.append(pos)
		self.render_toolpath(pos)

	def draw_workspace_grid(self):
		"""Draws a workspace grid dynamically aligned with the machine's INI travel limits."""
		x_min, y_min, z_min = self.min_limits
		x_max, y_max, z_max = self.max_limits
		
		glColor3f(0.3, 0.3, 0.3)
		glBegin(GL_LINES)
		
		# Calculate dynamic step size based on workspace size (roughly 10 subdivisions)
		x_range = x_max - x_min
		y_range = y_max - y_min
		step_x = max(1.0, x_range / 10.0)
		step_y = max(1.0, y_range / 10.0)
		
		# Draw lines parallel to Y axis along X coordinates
		curr_x = x_min
		while curr_x <= x_max + 1e-5:
			glVertex3f(curr_x, y_min, z_min)
			glVertex3f(curr_x, y_max, z_min)
			curr_x += step_x
			
		# Draw lines parallel to X axis along Y coordinates
		curr_y = y_min
		while curr_y <= y_max + 1e-5:
			glVertex3f(x_min, curr_y, z_min)
			glVertex3f(x_max, curr_y, z_min)
			curr_y += step_y
			
		glEnd()

	def draw_dynamic_machine_boundary(self):
		"""Draws the live 3D boundary box using the fetched INI MIN/MAX limits with a red line."""
		glColor3f(1.0, 0.0, 0.0) # Red line
		glLineWidth(1.0)

		x1, y1, z1 = self.min_limits
		x2, y2, z2 = self.max_limits

		glBegin(GL_LINES)
		# Bottom square perimeter (Z = z1)
		glVertex3f(x1, y1, z1); glVertex3f(x2, y1, z1)
		glVertex3f(x2, y1, z1); glVertex3f(x2, y2, z1)
		glVertex3f(x2, y2, z1); glVertex3f(x1, y2, z1)
		glVertex3f(x1, y2, z1); glVertex3f(x1, y1, z1)

		# Top square perimeter (Z = z2)
		glVertex3f(x1, y1, z2); glVertex3f(x2, y1, z2)
		glVertex3f(x2, y1, z2); glVertex3f(x2, y2, z2)
		glVertex3f(x2, y2, z2); glVertex3f(x1, y2, z2)
		glVertex3f(x1, y2, z2); glVertex3f(x1, y1, z2)

		# Vertical pillars connecting bottom and top corners
		glVertex3f(x1, y1, z1); glVertex3f(x1, y1, z2)
		glVertex3f(x2, y1, z1); glVertex3f(x2, y1, z2)
		glVertex3f(x2, y2, z1); glVertex3f(x2, y2, z2)
		glVertex3f(x1, y2, z1); glVertex3f(x1, y2, z2)
		glEnd()
		glLineWidth(1.0)

	def render_toolpath(self, current_pos):
		"""Renders the active 9-Axis traced path history and a filled cone tool indicator.
		Adjusting Size: You can easily scale the visual presence of your new tool pointer
		by editing cone_height and cone_base_radius to fit your specific viewport sizing preferences.
		"""

		# 1. Draw the toolpath line history trail
		glColor3f(0.0, 0.8, 1.0) # Light blue toolpath trail
		glBegin(GL_LINE_STRIP)
		for pt in self.tool_path_history:
			x, y, z, a, b, c, u, v, w = pt
			total_x = x + u
			total_y = y + v
			total_z = z + w
			glVertex3f(total_x, total_y, total_z)
		glEnd()

		# 2. Render the live tool position as a filled cone pointing down
		glPushMatrix()
		cx, cy, cz, ca, cb, cc, cu, cv, cw = current_pos

		# Translate to the combined tool position centerpoint
		glTranslatef(cx + cu, cy + cv, cz + cw)

		# Apply orientation shifts if rotary offsets A, B, C are active
		glRotatef(ca, 1, 0, 0)
		glRotatef(cb, 0, 1, 0)
		glRotatef(cc, 0, 0, 1)

		# Open GLU draws cones along the +Z axis pointing outward with the base at Z=0.
		# To make it point straight DOWN, we lift the base up by the cone height 
		# and rotate it 180 degrees so the tip touches the exact path point (0,0,0).
		cone_height = 1.0
		cone_base_radius = 0.250

		glRotatef(180.0, 1.0, 0.0, 0.0)	  # Flip upside down to point down
		glTranslatef(0.0, 0.0, -cone_height) # Shift base up so tip sits at (0,0,0)

		# Set cone rendering material style
		glColor3f(1.0, 0.2, 0.2)			 # Bright Red Cone
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) # Force solid fill rendering

		# Create and render the Quadric Cone primitive
		quadric = gluNewQuadric()
		gluQuadricDrawStyle(quadric, GLU_FILL)

		# Parameters: quadric, baseRadius, topRadius (0 for cone), height, slices, stacks
		gluCylinder(quadric, cone_base_radius, 0.0, cone_height, 16, 1)
		
		# Draw a circular cap over the top base of the cone so it looks completely solid
		gluDisk(quadric, 0.0, cone_base_radius, 16, 1)

		gluDeleteQuadric(quadric)
		glPopMatrix()

	def mousePressEvent(self, event):
		self.last_mouse_pos = event.pos()
		if event.button() == Qt.MouseButton.LeftButton:
			self.mouse_action = 'rotate'
		elif event.button() == Qt.MouseButton.RightButton:
			self.mouse_action = 'pan'

	def mouseMoveEvent(self, event):
		if self.last_mouse_pos is None:
			return
		dx = event.position().x() - self.last_mouse_pos.x()
		dy = event.position().y() - self.last_mouse_pos.y()
		if self.mouse_action == 'rotate':
			self.camera_rot_y += dx * 0.5
			self.camera_rot_x += dy * 0.5
		elif self.mouse_action == 'pan':
			self.pan_offset_x += dx * 0.2
			self.pan_offset_y -= dy * 0.2
		self.last_mouse_pos = event.pos()
		self.update()

	def mouseReleaseEvent(self, event):
		self.mouse_action = None
		self.last_mouse_pos = None

	def wheelEvent(self, event):
		self.camera_distance = max(-1000.0, min(-5.0, self.camera_distance + event.angleDelta().y() * 0.1))
		self.update()

