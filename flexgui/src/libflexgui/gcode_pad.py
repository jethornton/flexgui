import os

from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6.uic import loadUi

class gcode_pad(QDialog):
	def __init__(self, lib_path):
		super().__init__()

		loadUi(os.path.join(lib_path, 'gcode.ui'), self)
		self.save_pb.clicked.connect(self.accept)
		self.cancel_pb.clicked.connect(self.reject)
		self.clear_pb.clicked.connect(self.clear)
		self.backspace_pb.clicked.connect(self.backspace)
		self.left_arrow_pb.clicked.connect(self.left_arrow)
		self.right_arrow_pb.clicked.connect(self.right_arrow)
		self.space_pb.clicked.connect(self.space)

		for item in self.findChildren(QPushButton):
			if item.objectName().startswith('key_'):
				getattr(self, f'{item.objectName()}').clicked.connect(self.post)
			elif item.objectName().startswith('next_'):
				getattr(self, f'{item.objectName()}').clicked.connect(self.next)
			elif item.objectName().startswith('back_'):
				getattr(self, f'{item.objectName()}').clicked.connect(self.back)

		# Variable to store the position
		self.exit_pos = None

	def next(self):
		self.letters_sw.setCurrentIndex(self.letters_sw.currentIndex() + 1)

	def back(self):
		self.letters_sw.setCurrentIndex(self.letters_sw.currentIndex() - 1)

	def post(self):
		self.gcode_le.insert(self.sender().text())
		self.gcode_le.setFocus()

	def clear(self):
		self.gcode_le.clear()
		self.gcode_le.setFocus()

	def backspace(self):
		self.gcode_le.backspace()
		self.gcode_le.setFocus()

	def left_arrow(self):
		# Move one step backward from the current position
		current_pos = self.gcode_le.cursorPosition()
		self.gcode_le.setCursorPosition(max(0, current_pos - 1)) # Ensure position is not negative
		self.gcode_le.setFocus()

	def right_arrow(self):
		# Move one step forward from the current position
		current_pos = self.gcode_le.cursorPosition()
		self.gcode_le.setCursorPosition(current_pos + 1)
		self.gcode_le.setFocus()

	def space(self):
		self.gcode_le.insert(' ')
		self.gcode_le.setFocus()

	def retval(self):
		try:
			return(self.gcode_le.text())
		except:
			return False

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		super().moveEvent(event) # Call the base class implementation

