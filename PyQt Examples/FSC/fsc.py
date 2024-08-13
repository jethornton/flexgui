#!/usr/bin/env python3

import sys, os
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic

class main(QWidget):
	def __init__(self):
		super().__init__()
		uic.loadUi(os.path.join(os. getcwd(), 'fsc.ui'), self)
		self.setGeometry(50, 50, 500, 300)
		self.setWindowTitle("Feed and Speed Calculator!")
		#with open('style.qss','r') as fh:
		#	self.setStyleSheet(fh.read())

		self.fsc_calc_cl_pb.clicked.connect(self.calc_cl)
		self.fsc_calc_fr_pb.clicked.connect(self.calc_fr)
		self.fsc_calc_sfm_pb.clicked.connect(self.calc_sfm)
		self.fsc_diameter_le.setText('0.5')
		self.fsc_flutes_le.setText('4')
		self.fsc_rpm_le.setText('4000')
		self.fsc_feed_le.setText('60')
		self.fsc_load_le.setText('0.005')
		self.show()

	def calc_cl (self):
		print('calc_cl')

	def calc_fr (self):
		print('calc_fr')

	def calc_sfm (self):
		print('calc_sfm')
		dia = float(self.fsc_diameter_le.text())
		rpm = float(self.fsc_rpm_le.text())
		sfm = (rpm * dia)/3.82
		self.fsc_sfm_lb.setText(f'{sfm:.2f} SFM')

app = QApplication(sys.argv)
gui = main()
sys.exit(app.exec())
