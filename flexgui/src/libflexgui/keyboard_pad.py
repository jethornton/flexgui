import sys, os
from functools import partial

from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6.uic import loadUi

class keyboard_pad(QDialog):
	def __init__(self, lib_path):
		super().__init__()

		loadUi(os.path.join(lib_path, 'keyboard.ui'), self)
		self.save_pb.clicked.connect(self.accept)
		self.cancel_pb.clicked.connect(self.reject)
		self.clear_pb.clicked.connect(self.clear)
		self.space_pb.clicked.connect(self.space)
		self.backspace_pb.clicked.connect(self.backspace)
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
		txt = self.keyboard_lb.text()
		self.keyboard_lb.setText(f'{txt}{self.sender().text()}')

	def clear(self):
		self.keyboard_lb.clear()

	def space(self):
		txt = self.keyboard_lb.text()
		self.keyboard_lb.setText(f'{txt} ')

	def backspace(self):
		txt = self.keyboard_lb.text()
		if len(txt) > 0:
			self.keyboard_lb.setText(txt[:-1])

	def change_page(self, index):
		self.keyboard_sw.setCurrentIndex(index)

	def retval(self):
		try:
			return(self.keyboard_lb.text())
		except:
			return False

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		super().moveEvent(event) # Call the base class implementation

