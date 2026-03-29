import os
from functools import partial

from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6.uic import loadUi

class keyboard_pad(QDialog):
	def __init__(self, lib_path):
		super().__init__()

		loadUi(os.path.join(lib_path, 'keyboard.ui'), self)
		self.keyboard_le.setReadOnly(False)
		self.save_pb.clicked.connect(self.accept)
		self.cancel_pb.clicked.connect(self.reject)
		self.clear_pb.clicked.connect(self.clear)
		self.space_pb.clicked.connect(self.space)
		self.backspace_pb.clicked.connect(self.backspace)
		self.left_arrow_pb.clicked.connect(self.left_arrow)
		self.right_arrow_pb.clicked.connect(self.right_arrow)
		self.gcode_pb.clicked.connect(partial(self.change_page, 0))
		self.capital_letters_pb.clicked.connect(partial(self.change_page, 1))
		self.lower_letters_pb.clicked.connect(partial(self.change_page, 2))
		self.symbols_pb.clicked.connect(partial(self.change_page, 3))

		for item in self.findChildren(QPushButton):
			if item.objectName().startswith('key_'):
				getattr(self, f'{item.objectName()}').clicked.connect(self.post)

		# Variable to store the position
		self.exit_pos = None

	def post(self):
		self.keyboard_le.insert(self.sender().text())

	def clear(self):
		self.keyboard_le.clear()

	def space(self):
		self.keyboard_le.insert(' ')

	def backspace(self):
		self.keyboard_le.backspace()
		self.keyboard_le.setFocus()

	def left_arrow(self):
		# Move one step backward from the current position
		current_pos = self.keyboard_le.cursorPosition()
		self.keyboard_le.setCursorPosition(max(0, current_pos - 1)) # Ensure position is not negative
		self.keyboard_le.setFocus()

	def right_arrow(self):
		# Move one step forward from the current position
		current_pos = self.keyboard_le.cursorPosition()
		self.keyboard_le.setCursorPosition(current_pos + 1)
		self.keyboard_le.setFocus()

	def change_page(self, index):
		self.keyboard_sw.setCurrentIndex(index)

	def retval(self):
		try:
			return(self.keyboard_le.text())
		except:
			return False

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		super().moveEvent(event) # Call the base class implementation

