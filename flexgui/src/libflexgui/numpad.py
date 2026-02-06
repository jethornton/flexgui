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
		self.key_dot.clicked.connect(self.dot)
		self.key_dash.clicked.connect(self.dash)
		self.backspace_pb.clicked.connect(self.backspace)
		for item in self.findChildren(QPushButton):
			if item.objectName().startswith('key_'):
				getattr(self, item.objectName()).clicked.connect(self.post)

		# Variable to store the position
		self.exit_pos = None

	def post(self):
		txt = self.numbers_le.text()
		self.numbers_le.setText(f'{txt}{self.sender().objectName()[-1]}')

	def clear(self):
		self.numbers_le.clear()

	def dot(self):
		txt = self.numbers_le.text()
		self.numbers_le.setText(f'{txt}.')

	def dash(self):
		txt = self.numbers_le.text()
		self.numbers_le.setText(f'-{txt}')

	def backspace(self):
		txt = self.numbers_le.text()
		if len(txt) > 0:
			self.numbers_le.setText(txt[:-1])

	def retval(self):
		try:
			return self.numbers_le.text()
		except:
			return False

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		super().moveEvent(event) # Call the base class implementation


