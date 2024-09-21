import sys, os

from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6.uic import loadUi

class keyboard_pad(QDialog):
	def __init__(self):
		super().__init__()

		self.path = os.path.dirname(os.path.realpath(sys.argv[0]))

		# set the library path
		if self.path == '/usr/bin':
			self.lib_path = '/usr/lib/libflexgui'
			self.gui_path = '/usr/lib/libflexgui'
		else:
			self.lib_path = os.path.join(self.path, 'libflexgui')
			self.gui_path = self.path

		num_ui_path = os.path.join(self.gui_path, 'gcode.ui')
		loadUi(num_ui_path, self)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.clear_pb.clicked.connect(self.clear)
		self.backspace_pb.clicked.connect(self.backspace)


	def retval(self):
		try:
			return(self.keyboard_lb.text())
		except:
			return False

