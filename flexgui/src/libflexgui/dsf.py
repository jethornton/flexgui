# Drill Speed and Feed Calculator

import os, sys

from PyQt6.QtWidgets import QWidget
from PyQt6.uic import loadUi

'''
• Feed equals .001" per revolution for every 1/16" of drill diameter, plus or
  minus .001" on the total.
• Speed equals 80 surface feet per minute in 100 Brinell hardness material and
  the speed should be reduced 10 surface feet per minute for each additional 50
  points Brinell hardness.
• Feed and speed rates should be reduced up to 45-50‰ when drilling holes deeper
  than 4 drill diameters.
• R.P.M. = (3.8197 / Drill Diameter) x S.F.M.
• S.F.M. = 0.2618 x Drill Diameter x R.P.M.
• I.P.M. = I.P.R. (feed) x R.P.M. (speed)
• Machine Time (seconds) = (60 x Feed minus Stroke) / I.P.M.
'''

class dsf_calc(QWidget):
	def __init__(self, touch=False):
		super().__init__()
		self.path = os.path.dirname(os.path.realpath(sys.argv[0]))
		if self.path == '/usr/bin':
			self.lib_path = '/usr/lib/libflexgui'
		else:
			self.lib_path = os.path.join(self.path, 'libflexgui')
		loadUi(os.path.join(self.lib_path, 'dsf.ui'), self)

		self.dsf_units_pb.clicked.connect(self.units)
		self.setup_material()



	def units(self):
		if self.dsf_units_pb.isChecked():
			self.dsf_units_pb.setText('Metric')
		else:
			self.dsf_units_pb.setText('Inch')


	def setup_material(self):
		self.dsf_material_cb.addItem('Select')
		sfm = [
			'Aluminum: 200-300 SFM',
			'Brass and Bronze: 150-300 SFM',
			'Bronze (High Tensile) 70-150 SFM',
			'Iron-Cast (Soft): 75-125 SFM',
			'Plastics: 100-300 SFM',
			'Steel .2 to .3 carbon:  80-110 SFM',
			'Steel .4 to .5 carbon:  70-80 SFM',
			'Tool Steel 1.2 carbon:  50-60 SFM',
			'',
		]

		self.dsf_material_cb.addItems(sfm)




