import sys, os

from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

# called by dialogs.touchoff_selected

class app(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)

		self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
		# set the library path
		if self.path == '/usr/bin':
			self.lib_path = '/usr/lib/libflexgui'
			self.gui_path = '/usr/lib/libflexgui'
		else:
			self.lib_path = os.path.join(self.path, 'libflexgui')
			self.gui_path = self.path

		to_ui_path = os.path.join(self.gui_path, 'touchoff.ui')
		loadUi(to_ui_path, self)

		cs_names = ['Current', 'G54', 'G55', 'G56', 'G57', 'G58', 'G59', 'G59.1',
		'G59.2', 'G59.3']
		for i in range(10):
			self.coordinate_systems_cb.addItem(f'P{i} {cs_names[i]}', i)

		# Variable to store the position
		self.exit_pos = None
		self.exit_size = None

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		self.exit_size = self.size()
		super().moveEvent(event) # Call the base class implementation

