#!/usr/bin/env python3

import sys, os, string, random

# disable cache usage must be before any local imports
sys.dont_write_bytecode = True

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic

import resources

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setGeometry(50, 150, 300, 400)
		self.setWindowTitle('Touch Screen File Selector')
		uic.loadUi(os.path.join(os. getcwd(), 'listwidget.ui'), self)

		with open('listwidget.qss','r') as fh:
			self.setStyleSheet(fh.read())

		# put something in the list widgets
		for i in range(25):
			self.listWidget_1.addItem(''.join(random.choices(string.ascii_letters, k=i+5)))
		for i in range(15):
			self.listWidget_2.addItem(''.join(random.choices(string.ascii_letters, k=i+5)))

		# set width to fit widest item
		#print(self.listWidget_1.sizeHintForColumn(0))
		self.listWidget_1.setMinimumWidth(self.listWidget_1.sizeHintForColumn(0)+60)

		self.show()

app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec())

