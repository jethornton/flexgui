#!/usr/bin/env python3

import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt6 import uic

import hal

class main(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi(os.path.join(os. getcwd(), 'hal_test.ui'), self)
		self.setGeometry(50, 50, 250, 250)
		self.setWindowTitle("PyQT6 HAL Test!")
		#with open('style.qss','r') as fh:
		#	self.setStyleSheet(fh.read())
		self.show()

		self.halcomp = hal.component('flexhal')
		#setup_hal_buttons(self)
		count_hal_buttons(self)

	def closeEvent(self, event):
		self.halcomp.exit()


def count_hal_buttons(parent):
	hal_buttons = []
	for button in parent.findChildren(QPushButton):
		if button.property('function') == 'hal_pin':
			hal_buttons.append(button)
	#print(len(hal_buttons))
	for n, button in enumerate(hal_buttons):
		props = button.dynamicPropertyNames()
		for prop in props:
			prop = str(prop, 'utf-8')
			if prop.startswith('pin_'):
				pin_settings = button.property(prop).split(',')
				name = button.objectName()
				pin_name = pin_settings[0]
				pin_type = getattr(hal, f'{pin_settings[1].upper().strip()}')
				pin_dir = getattr(hal, f'{pin_settings[2].upper().strip()}')
				#print(name, pin_name, pin_type, pin_dir)
				setattr(parent, f'{prop}', parent.halcomp.newpin(pin_name, pin_type, pin_dir))
				#print(getattr(parent, f'{prop}')) # <hal.Pin object at 0x7f4fcb53ded0>
				#print(getattr(parent, f'{name}')) # <PyQt6.QtWidgets.QPushButton object at 0x7f79b39117e0>
				getattr(parent, f'{name}').clicked.connect(lambda n=n: getattr(parent, f'{prop}').set(getattr(parent, f'{name}').isDown()))
				#getattr(parent, f'{name}').toggled.connect(lambda num=n: getattr(parent, f'{prop}').set(getattr(parent, f'{name}').isChecked()))
	parent.halcomp.ready()


def setup_hal_buttons(parent):
	for button in parent.findChildren(QPushButton):
		if button.property('function') == 'hal_pin':
			props = button.dynamicPropertyNames()
			#print(button.objectName(), button.text())
			for prop in props:
				prop = str(prop, 'utf-8')
				if prop.startswith('pin_'):
					#print(prop)
					pin_settings = button.property(prop).split(',')
					name = button.objectName()
					#print(name)
					pin_name = pin_settings[0]
					pin_type = getattr(hal, f'{pin_settings[1].upper().strip()}')
					pin_dir = getattr(hal, f'{pin_settings[2].upper().strip()}')
					setattr(parent, f'{prop}', parent.halcomp.newpin(pin_name, pin_type, pin_dir))
					#print(getattr(parent, f'{name}'))
					#print(getattr(parent, f'{prop}'))
					getattr(parent, f'{name}').toggled.connect(lambda: getattr(parent, f'{prop}').set(getattr(parent, f'{name}').isChecked()))
	parent.halcomp.ready()
'''
for number in range(8):
	my_function = lambda num=number: num
	function2.append(my_function)

results2 = [function() for function in function2]
'''

app = QApplication(sys.argv)
gui = main()
sys.exit(app.exec())
