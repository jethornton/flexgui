import os, sys
from math import pi

from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

class feed_speed_calc(QWidget):
	def __init__(self):
		super().__init__()
		self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
		if self.path == '/usr/bin':
			self.lib_path = '/usr/lib/libflexgui'
		else:
			self.lib_path = os.path.join(self.path, 'libflexgui')
		loadUi(os.path.join(self.lib_path, 'fsc.ui'), self)

		self.fsc_diameter_le.setText('0.5')
		self.fsc_flutes_le.setText('4')
		self.fsc_rpm_le.setText('4000')
		self.fsc_feed_le.setText('60')
		self.fsc_load_le.setText('0.005')
		self.fsc_cl_lb.setText('')
		self.fsc_feed_lb.setText('')
		self.fsc_sfm_lb.setText('')
		self.fsc_calc_cl_pb.clicked.connect(self.calc_cl)
		self.fsc_calc_fr_pb.clicked.connect(self.calc_fr)
		self.fsc_calc_sfm_pb.clicked.connect(self.calc_sfm)
		self.fsc_units_pb.clicked.connect(self.units)

	def calc_cl(self):
		feed = float(self.fsc_feed_le.text())
		rpm = float(self.fsc_rpm_le.text())
		flutes = int(self.fsc_flutes_le.text())
		if self.fsc_units_pb.text() == 'Inch':
			# Chip Load = inches per minute / (RPM x number of flutes)
			cl = feed / (rpm * flutes)
			self.fsc_cl_lb.setText(f'{cl:.4f} FPT')
		elif self.fsc_units_pb.text() == 'Metric':
			# Chip Load = Milimeters per Minute / (RPM x number of flutes)
			cl = (feed * 1000) / (rpm * flutes)
			self.fsc_cl_lb.setText(f'{cl:.3f} mm/PT')

	def calc_fr(self):
		print('calc_fr')

	def calc_sfm(self):
		dia = float(self.fsc_diameter_le.text())
		rpm = float(self.fsc_rpm_le.text())
		if self.fsc_units_pb.text() == 'Inch':
			sfm = (rpm * dia)/3.82
			self.fsc_sfm_lb.setText(f'{sfm:.2f} SFM')
		elif self.fsc_units_pb.text() == 'Metric':
			# pi * diam * rpm / 1000
			smm = (pi * dia * rpm) /1000
			self.fsc_sfm_lb.setText(f'{smm:.2f} MPM')

	def units(self):
		if self.fsc_units_pb.isChecked():
			self.fsc_units_pb.setText('Metric')
			self.fsc_sfm_lb.setText('SMM')
			self.fsc_feed_lb.setText('MPM')
			self.fsc_feed_unit_lb.setText('Feed MPM')
			self.fsc_chip_load_units_lb.setText('Chip Load mm')
		else:
			self.fsc_units_pb.setText('Inch')
			self.fsc_sfm_lb.setText('SFM')
			self.fsc_feed_lb.setText('IPM')
			self.fsc_feed_unit_lb.setText('Feed IPM')
			self.fsc_chip_load_units_lb.setText('Chip Load in')



