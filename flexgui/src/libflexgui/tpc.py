# Three Point Center Calculator
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.uic import loadUi

import linuxcnc as emc

from libflexgui import commands

class tpc_calc(QWidget):
	def __init__(self, parent):
		super().__init__()
		self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
		if self.path == '/usr/bin':
			self.lib_path = '/usr/lib/libflexgui'
		else:
			self.lib_path = os.path.join(self.path, 'libflexgui')

		loadUi(os.path.join(self.lib_path, 'tpc.ui'), self)

		image_path = os.path.join(self.lib_path, 'tpc.jpg')
		pixmap = QPixmap(image_path)

		# Force alignment to keep the image centered inside its UI frame
		self.tpc_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
		# Scale the pixmap while explicitly preserving its aspect ratio
		# KeepAspectRatio keeps the original proportions intact
		# SmoothTransformation prevents jagged edges when scaling down
		scaled_pixmap = pixmap.scaled(
			self.tpc_lb.size(), 
			Qt.AspectRatioMode.KeepAspectRatio, 
			Qt.TransformationMode.SmoothTransformation
		)
		self.tpc_lb.setPixmap(scaled_pixmap)

		#self.tpc_lb.setPixmap(pixmap)
		#self.tpc_lb.setScaledContents(True)

		self.x_center = None
		self.y_center = None
		self.stat = emc.stat()

		# Connect UI Elements
		self.save_point_1_pb.clicked.connect(self.save_point_1)
		self.save_point_2_pb.clicked.connect(self.save_point_2)
		self.save_point_3_pb.clicked.connect(self.save_point_3)
		self.calculate_center_pb.clicked.connect(self.calculate_center)
		self.move_to_center_pb.clicked.connect(self.move_to_center)
		self.set_to_x0_y0.clicked.connect(self.set_to_x0y0)

		# Initialize coordinates
		self.x1 = 0.0; self.y1 = 0.0
		self.x2 = 0.0; self.y2 = 0.0
		self.x3 = 0.0; self.y3 = 0.0

	def resizeEvent(self, event):
		"""Automatically scales the image whenever the window size changes."""
		super().resizeEvent(event)
		if hasattr(self, 'lib_path'):
			image_path = os.path.join(self.lib_path, 'tpc.jpg')
			pixmap = QPixmap(image_path)
			scaled = pixmap.scaled(
				self.tpc_lb.size(),
				Qt.AspectRatioMode.KeepAspectRatio,
				Qt.TransformationMode.SmoothTransformation
			)
			self.tpc_lb.setPixmap(scaled)

	def get_current_coords(self):
		"""Helper to cleanly poll LinuxCNC Cartesian coordinates."""
		self.stat.poll()
		# Using Cartesian position [x, y] instead of joint positions
		return self.stat.position[0], self.stat.position[1]

	def save_point_1(self):
		self.x1, self.y1 = self.get_current_coords()
		self.point_1_x.setText(f'{self.x1:.4f}')
		self.point_1_y.setText(f'{self.y1:.4f}')

	def save_point_2(self):
		self.x2, self.y2 = self.get_current_coords()
		self.point_2_x.setText(f'{self.x2:.4f}')
		self.point_2_y.setText(f'{self.y2:.4f}')

	def save_point_3(self):
		self.x3, self.y3 = self.get_current_coords()
		self.point_3_x.setText(f'{self.x3:.4f}')
		self.point_3_y.setText(f'{self.y3:.4f}')

	def calculate_center(self):
		x1, y1 = self.x1, self.y1
		x2, y2 = self.x2, self.y2
		x3, y3 = self.x3, self.y3
		
		# Calculate denominator to protect against straight lines / division by zero
		denominator = 2 * (x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2)

		if denominator == 0:
			self.center_x.setText("Error")
			self.center_y.setText("Collinear")
			self.x_center = None
			self.y_center = None
			return

		try:
			self.x_center = ((x1**2 + y1**2) * (y2 - y3) + (x2**2 + y2**2) * (y3 - y1) + (x3**2 + y3**2) * (y1 - y2)) / denominator
			self.y_center = ((x1**2 + y1**2) * (x3 - x2) + (x2**2 + y2**2) * (x1 - x3) + (x3**2 + y3**2) * (x2 - x1)) / denominator
			
			# FIXED: Referencing instance variables self.x_center and self.y_center
			self.center_x.setText(f'{self.x_center:.4f}')
			self.center_y.setText(f'{self.y_center:.4f}')

		except Exception as e:
			self.center_x.setText("Error")
			self.center_y.setText("Calc Fail")
			print(f"Exception Type: {type(e)}, Message: {e}")

	def move_to_center(self): 
		# FIXED: Referencing instance variables instead of local variables
		if self.x_center is not None and self.y_center is not None:
			print(f'move_to_center X {self.x_center:.4f} Y {self.y_center:.4f}')
			# Example MDI command execution if libflexgui supports it:
			commands.run_mdi(parent, f'G0 X{self.x_center:.4f} Y{self.y_center:.4f}')
		else:
			print('Error: Calculate a center point first')

	def set_to_x0y0(self): 
		if self.x_center is not None and self.y_center is not None:
			print(f'Setting current center to X0 Y0')
			# Example MDI offset command (G10 L2 P0 X... Y...) to shift coordinate origin
			commands.run_mdi(parent, f'G10 L20 P0 X0 Y0')
		else:
			print('Error: No center point calculated to set as origin')

