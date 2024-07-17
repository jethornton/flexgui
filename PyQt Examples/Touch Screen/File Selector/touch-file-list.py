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
		uic.loadUi(os.path.join(os. getcwd(), 'touch-file-list.ui'), self)

		home = os.path.expanduser('~')
		self.dir = os.path.join(home, 'linuxcnc', 'nc_files')
		if os.path.isdir(self.dir):
			files = os.listdir(self.dir)
			self.listWidget.addItem('Parent Directory')
			self.listWidget.addItems(files)
			self.listWidget_2.addItem('Parent Directory')
			self.listWidget_2.addItems(files)

		self.label.setText('Select a file or Directory')

		with open('touch-file-list.qss','r') as fh:
			self.setStyleSheet(fh.read())

		self.listWidget.itemClicked.connect(self.row_changed)

		self.show()

	def row_changed(self):
		item = self.listWidget.currentItem().text()
		path = os.path.join(self.dir, item)
		if os.path.isdir(path):
			self.dir = path
			files = os.listdir(self.dir)
			self.listWidget.clear()
			self.listWidget.addItem('Parent Directory')
			self.listWidget.addItems(files)
			self.label.setText(f'Selected Directory: {self.dir}')
		elif os.path.isfile(path):
			self.label.setText(f'Selected File: {path}')
		elif item == 'Parent Directory':
			self.dir = os.path.dirname(self.dir)
			files = os.listdir(self.dir)
			self.listWidget.clear()
			self.listWidget.addItem('Parent Directory')
			self.listWidget.addItems(files)
			self.label.setText(f'Selected Directory: {self.dir}')

app = QApplication(sys.argv)
ex = MainWindow()
sys.exit(app.exec())

