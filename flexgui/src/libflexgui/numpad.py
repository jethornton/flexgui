import sys, os

from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6.uic import loadUi

class number_pad(QDialog):
	def __init__(self, lib_path):
		super().__init__()

		loadUi(os.path.join(lib_path, 'numpad.ui'), self)
		self.save_pb.clicked.connect(self.accept)
		self.cancel_pb.clicked.connect(self.reject)
		self.clear_pb.clicked.connect(self.clear)
		self.minus.clicked.connect(self.dash)
		self.left_arrow_pb.clicked.connect(self.left_arrow)
		self.right_arrow_pb.clicked.connect(self.right_arrow)
		self.backspace_pb.clicked.connect(self.backspace)
		for item in self.findChildren(QPushButton):
			if item.objectName().startswith('key_'):
				getattr(self, item.objectName()).clicked.connect(self.post)

		# Variable to store the position
		self.exit_pos = None

	def post(self):
		self.numbers_le.insert(self.sender().text())
		self.numbers_le.setFocus()

	def clear(self):
		self.numbers_le.clear()
		self.numbers_le.setFocus()

	def dash(self):
		txt = self.numbers_le.text()
		self.numbers_le.setText(f'-{txt}')
		self.numbers_le.setFocus()

	def left_arrow(self):
		# Move one step backward from the current position
		current_pos = self.numbers_le.cursorPosition()
		self.numbers_le.setCursorPosition(max(0, current_pos - 1)) # Ensure position is not negative
		self.numbers_le.setFocus()

	def right_arrow(self):
		# Move one step forward from the current position
		current_pos = self.numbers_le.cursorPosition()
		self.numbers_le.setCursorPosition(current_pos + 1)
		self.numbers_le.setFocus()

	def backspace(self):
		self.numbers_le.backspace()
		self.numbers_le.setFocus()

	def retval(self):
		try:
			return self.numbers_le.text()
		except:
			return False

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		super().moveEvent(event) # Call the base class implementation


