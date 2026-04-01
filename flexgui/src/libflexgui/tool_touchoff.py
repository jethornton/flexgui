import sys, os

from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

# called by dialogs.tool_touchoff_selected

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

		tto_ui_path = os.path.join(self.gui_path, 'tool_touchoff.ui')
		loadUi(tto_ui_path, self)

		# Variable to store the position
		self.exit_pos = None
		self.exit_size = None

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		super().moveEvent(event) # Call the base class implementation

	def resizeEvent(self, event):
		# This method is called when the dialog size changes.
		self.exit_size = self.size()
		super().resizeEvent(event) # Call the base class implementation

