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
1 inch is exactly 25.4 MM Therefore 1 meter is about 39.37 IN, or 3.281 FT.
1 foot is 0.3048 meters
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

		self.units = 'Inch'
		self.dsf_units_pb.clicked.connect(self.change_units)
		self.setup_material()



	def change_units(self):
		if self.units == 'Inch':
			self.dsf_units_pb.setText('Metric')
			self.units = 'Metric'
		elif self.units == 'Metric':
			self.dsf_units_pb.setText('Inch')
			self.units = 'Inch'
		self.setup_material()


	def setup_material(self):
		self.dsf_material_cb.clear()
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
		smm = [
			'Aluminum: 60-90 SMM',
			'Brass and Bronze: 45-90 SMM',
			'Bronze (High Tensile) 21-45 SMM',
			'Iron-Cast (Soft): 23-38 SMM',
			'Plastics: 30-90 SMM',
			'Steel .2 to .3 carbon:  25-34 SMM',
			'Steel .4 to .5 carbon:  21-25 SMM',
			'Tool Steel 1.2 carbon:  15-18 SMM',
			'',
		]

		if self.units == 'Inch':
			self.dsf_material_cb.addItems(sfm)
		else:
			self.dsf_material_cb.addItems(smm)







