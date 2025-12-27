import sys, os

from PyQt6.QtWidgets import QDialog, QPushButton
from PyQt6.uic import loadUi

class gcode_pad(QDialog):
	def __init__(self, lib_path):
		super().__init__()

		loadUi(os.path.join(lib_path, 'gcode.ui'), self)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.clear_pb.clicked.connect(self.clear)
		self.backspace_pb.clicked.connect(self.backspace)
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
		txt = self.gcode_lb.text()
		self.gcode_lb.setText(f'{txt}{self.sender().text()}')

	def clear(self):
		self.gcode_lb.clear()

	def backspace(self):
		txt = self.gcode_lb.text()
		if len(txt) > 0:
			self.gcode_lb.setText(txt[:-1])

	def space(self):
		txt = self.gcode_lb.text()
		self.gcode_lb.setText(f'{txt} ')

	def retval(self):
		try:
			return(self.gcode_lb.text())
		except:
			return False

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		super().moveEvent(event) # Call the base class implementation

