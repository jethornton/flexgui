#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

import hal

class test(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.hal_test = hal.component('test')
		self.hal_test.newpin('out', hal.HAL_BIT, hal.HAL_OUT)
		self.hal_test.newpin('speed', hal.HAL_U32, hal.HAL_IN)
		self.hal_test.ready()
		print(f'test exists {hal.component_exists("test")}')
		print(f'test ready {hal.component_is_ready("test")}')
		hal.new_sig("out_signal",hal.HAL_BIT)
		hal.connect('test.out','out_signal')
		#print(f'Pin Dir {test.out.get_dir()}')

		self.test_value = QPushButton('Test Value')
		self.test_value.setCheckable(True)
		self.test_value.clicked.connect(self.set_value)

		self.layout.addWidget(self.test_value)

		self.test_state = QPushButton('Test State')
		#self.test_state.setCheckable(True)
		#self.test_state.clicked.connect(self.set_state)
		#self.test_state.toggled.connect(self.set_state)
		#self.test_state.toggled.connect(self.toggled)
		self.test_state.pressed.connect(self.pressed)
		self.test_state.released.connect(self.released)

		self.layout.addWidget(self.test_state)

		self.show()

	def set_value(self, state):
		print(state)
		if state:
			self.hal_test['speed'] = 10
		else:
			self.hal_test['speed'] = 0 

	def pressed(self):
		print('pressed')

	def released(self):
		print('released')

	def toggled(self):
		print(self.sender().objectName())

	def set_state(self, state):
		print(self.sender().objectName())
		print(state)
		if state:
			self.hal_test['out'] = True
		else:
			self.hal_test['out'] = False 

	def closeEvent(self, event):
		print('by by')
		event.accept()
		self.hal_test.exit()

app = QApplication([])
x = test()
app.exec()
