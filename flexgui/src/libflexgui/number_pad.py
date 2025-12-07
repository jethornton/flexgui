import sys, os

from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi

class number_pad(QDialog):
	def __init__(self, lib_path):
		super().__init__()

		'''
		self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
		print(f'lib_path {lib_path}')
		print(f'sys.argv {sys.argv}')
		if len(sys.argv) > 0:
			for arg in sys.argv:
				if arg.endswith('flexgui'):
					print('bingo')

		# set the library path
		if self.path == '/usr/bin':
			self.lib_path = '/usr/lib/libflexgui'
			self.gui_path = '/usr/lib/libflexgui'
		else:
			self.lib_path = os.path.join(self.path, 'libflexgui')
			self.gui_path = self.path

		print(f'self.path {self.path}')
		print(f'self.lib_path {self.lib_path}')
		print(f'self.gui_path {self.gui_path}')
		print(f'num_ui_path {num_ui_path}')
		return
		'''

		loadUi(os.path.join(lib_path, 'numbers.ui'), self)
		self.buttonBox.accepted.connect(self.accept)
		self.buttonBox.rejected.connect(self.reject)
		self.clear_pb.clicked.connect(self.clear)
		self.key_dot.clicked.connect(self.dot)
		self.key_dash.clicked.connect(self.dash)
		self.backspace_pb.clicked.connect(self.backspace)
		for i in range(10):
			getattr(self, f'key_{i}').clicked.connect(self.post)

		# Variable to store the position
		self.exit_pos = None

	def post(self):
		txt = self.numbers_lb.text()
		self.numbers_lb.setText(f'{txt}{self.sender().objectName()[-1]}')

	def clear(self):
		self.numbers_lb.clear()

	def dot(self):
		txt = self.numbers_lb.text()
		self.numbers_lb.setText(f'{txt}.')

	def dash(self):
		txt = self.numbers_lb.text()
		self.numbers_lb.setText(f'-{txt}')

	def backspace(self):
		txt = self.numbers_lb.text()
		if len(txt) > 0:
			self.numbers_lb.setText(txt[:-1])

	def retval(self):
		try:
			return self.numbers_lb.text()
		except:
			return False

	def moveEvent(self, event):
		# This method is called when the dialog moves.
		self.exit_pos = self.pos()
		super().moveEvent(event) # Call the base class implementation


