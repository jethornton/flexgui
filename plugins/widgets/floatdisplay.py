
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import pyqtProperty, QSize

class FlexFloatDisplay(QLabel):
	def __init__(self, parent=None):
		super(FlexFloatDisplay, self).__init__(parent)

		# variables used by properties
		self.decimal_precision = 0

	# these are used when you drag and drop a widget into the window
	def minimumSizeHint(self):
		return QSize(50, 25)

	def sizeHint(self):
		return QSize(125, 25)

	# start of property definition
	def get_precision(self):
		return self.decimal_precision

	def set_precision(self, data):
		# Sometime Validation is good here
		if 0 <= data <=10:
			self.decimal_precision = data
		else:
			print('error')

	# this creates the property for the widget
	precision = pyqtProperty(int, get_precision, set_precision)

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	fd = FlexFloatDisplay()
	fd.show()
	sys.exit(app.exec_())
