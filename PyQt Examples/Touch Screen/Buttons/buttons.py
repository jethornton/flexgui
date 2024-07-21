#!/usr/bin/env python3

import sys, os

# disable cache usage must be before any local imports
sys.dont_write_bytecode = True

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic

import resources

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setGeometry(50, 150, 400, 400)
		self.setWindowTitle('Touch Screen File Selector')
		uic.loadUi(os.path.join(os. getcwd(), 'buttons.ui'), self)

		with open('buttons.qss','r') as fh:
			self.setStyleSheet(fh.read())

		self.show()

app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec())

