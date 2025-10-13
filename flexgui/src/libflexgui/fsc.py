# Feed and Speed Calculator

import os, sys
from math import pi
from functools import partial

from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

from libflexgui import utilities
from libflexgui import dialogs

class fs_calc(QWidget):
	def __init__(self, parent):
		super().__init__()
		self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
		if self.path == '/usr/bin':
			self.lib_path = '/usr/lib/libflexgui'
		else:
			self.lib_path = os.path.join(self.path, 'libflexgui')
		loadUi(os.path.join(self.lib_path, 'fsc.ui'), self)

		self.fsc_cl_lb.setText('')
		self.fsc_feed_lb.setText('')
		self.fsc_sfm_lb.setText('')
		self.fsc_calc_cl_pb.clicked.connect(partial(self.calc_cl, parent))
		self.fsc_calc_fr_pb.clicked.connect(partial(self.calc_fr, parent))
		self.fsc_calc_sfm_pb.clicked.connect(partial(self.calc_sfm, parent))
		self.fsc_units_pb.clicked.connect(self.units)

	def check_cl(self, parent):
		if self.fsc_chip_load_le.text() == '':
			msg = ('Chip Load can not be blank')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False
		if utilities.is_float(self.fsc_chip_load_le.text()):
			return float(self.fsc_chip_load_le.text())
		else:
			msg = ('Chip Load is not a valid number')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False

	def check_feed(self, parent):
		if self.fsc_feed_le.text() == '':
			msg = ('Feed can not be blank')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False
		if utilities.is_float(self.fsc_feed_le.text()):
			return float(self.fsc_feed_le.text())
		else:
			msg = ('Feed is not a valid number')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False

	def check_rpm(self, parent):
		if self.fsc_rpm_le.text() == '':
			msg = ('RPM can not be blank')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False
		if utilities.is_float(self.fsc_rpm_le.text()):
			return float(self.fsc_rpm_le.text())
		else:
			msg = ('RPM is not a valid number')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False

	def check_flutes(self, parent):
		if self.fsc_flutes_le.text() == '':
			msg = ('Flutes can not be blank')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False
		if utilities.is_int(self.fsc_flutes_le.text()):
			return int(self.fsc_flutes_le.text())
		else:
			msg = ('Flutes is not a valid number')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False

	def check_dia(self, parent):
		if self.fsc_diameter_le.text() == '':
			msg = ('Diameter can not be blank')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False
		if utilities.is_float(self.fsc_diameter_le.text()):
			return float(self.fsc_diameter_le.text())
		else:
			msg = ('Diameter is not a valid number')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False

	def calc_cl(self, parent):
		feed = self.check_feed(parent)
		if not feed:
			return
		rpm = self.check_rpm(parent)
		if not rpm:
			return
		flutes = self.check_flutes(parent)
		if not flutes:
			return

		if self.fsc_units_pb.text() == 'Inch':
			# Chip Load = inches per minute / (RPM x number of flutes)
			cl = feed / (rpm * flutes)
			self.fsc_cl_lb.setText(f'{cl:.4f} IPT')
		elif self.fsc_units_pb.text() == 'Metric':
			# Chip Load = Milimeters per Minute / (RPM x number of flutes)
			cl = (feed * 1000) / (rpm * flutes)
			self.fsc_cl_lb.setText(f'{cl:.3f} mm/PT')

	def calc_fr(self, parent):
		cl = self.check_cl(parent)
		if not cl:
			return
		rpm = self.check_rpm(parent)
		if not rpm:
			return
		flutes = self.check_flutes(parent)
		if not flutes:
			return

		if self.fsc_units_pb.text() == 'Inch':
			feed = cl * (rpm * flutes)
			self.fsc_feed_lb.setText(f'{feed:.2f} IPM')
		elif self.fsc_units_pb.text() == 'Metric':
			# pi * diam * rpm / 1000
			feed = (cl * (rpm * flutes)) / 1000
			self.fsc_feed_lb.setText(f'{feed:.2f} MPM')

	def calc_sfm(self, parent):
		dia = self.check_dia(parent)
		if not dia:
			return
		rpm = self.check_rpm(parent)
		if not rpm:
			return

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
			self.fsc_feed_unit_lb.setText('Feed MPM')
			self.fsc_chip_load_units_lb.setText('Chip Load mm')
		else:
			self.fsc_units_pb.setText('Inch')
			self.fsc_feed_unit_lb.setText('Feed IPM')
			self.fsc_chip_load_units_lb.setText('Chip Load in')
		self.fsc_cl_lb.setText('')
		self.fsc_sfm_lb.setText('')
		self.fsc_feed_lb.setText('')



