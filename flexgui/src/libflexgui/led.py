
from PyQt6.QtCore import Qt, pyqtProperty, pyqtSignal, QPointF, QEvent, QSize
from PyQt6.QtGui import QRadialGradient, QLinearGradient, QPainter, QColor, QBrush, QPainter
from PyQt6.QtWidgets import QPushButton, QLabel

# gradient functions used by LED
# FIXME make the linear gradient come from upper right to lower left or similar to radial gradient
def makeLinearGradient(size, x, y, color):
	if size.width() > size.height():
		start_x = x
		start_y = y + (size.height() / 2.0)
		end_x = x + size.width()
		end_y = start_y
	else:
		start_x = x + (size.width() / 2.0)
		start_y = y
		end_x = start_x
		end_y = y + size.height()

	gradient = QLinearGradient(start_x, start_y, end_x, end_y)

	gradient.setColorAt(0.0, color)
	gradient.setColorAt(0.3, color)
	gradient.setColorAt(0.8, color)
	gradient.setColorAt(1.0, Qt.GlobalColor.white)
	return gradient

def makeRadialGradient(size, x, y, diameter, color):
	gradient = QRadialGradient(x + diameter / 2, y + diameter / 2,
		diameter * 0.5, diameter * 0.9, diameter * 0.2)
	gradient.setColorAt(0, Qt.GlobalColor.white)
	gradient.setColorAt(1, color)
	return gradient

# A QPushButton with a LED in the upper right corner
class LEDButton(QPushButton):

	value_changed = pyqtSignal(bool)
	_led = False

	def __init__(self, **kwargs):
		super().__init__()
		self.setText(kwargs['text'])
		self._diameter = kwargs['diameter']
		self._top_offset = kwargs['top_offset']
		self._right_offset = kwargs['right_offset']
		self._on_color = kwargs['on_color']
		self._off_color = kwargs['off_color']
		self.clicked.connect(lambda checked: self.set_led(checked))
		self.pressed.connect(lambda: self.set_led(True))
		self.released.connect(lambda: self.set_led(False))
		self._shape = kwargs['shape']

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		x_center = size.width() - ((self._diameter / 2) + self._right_offset)
		y_center = (self._diameter / 2) + self._top_offset
		x = size.width() - self._diameter - self._right_offset
		y = self._top_offset
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
		led_size = QSize(self._diameter, self._diameter)

		color = self._on_color if self._led else self._off_color
		if self._shape == 'round':
			gradient = makeRadialGradient(led_size, x, y, self._diameter, color)
		else:
			gradient = makeLinearGradient(led_size, x, y, color)
		
		painter.setBrush(QBrush(gradient))
		painter.setPen(color)

		if self._shape == 'square':
			painter.drawRect(int(x_center - (self._diameter / 2)),
				int(y_center - (self._diameter / 2)), self._diameter, self._diameter)
		else:
			painter.drawEllipse(QPointF(x_center, y_center),
				self._diameter / 2, self._diameter / 2)

	def set_led(self, val):
		self._led = val
		self.update()

# A QPushButton with a LED in the upper right corner
class IndicatorButton(QPushButton):
	_led = False

	def __init__(self, **kwargs):
		super().__init__()
		self.setText(kwargs['text'])
		self._diameter = kwargs['diameter']
		self._top_offset = kwargs['top_offset']
		self._right_offset = kwargs['right_offset']
		self._on_color = kwargs['on_color']
		self._off_color = kwargs['off_color']
		self._shape = kwargs['shape']

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		x_center = size.width() - ((self._diameter / 2) + self._right_offset)
		y_center = (self._diameter / 2) + self._top_offset
		x = size.width() - self._diameter - self._right_offset
		y = self._top_offset
		led_size = QSize(self._diameter, self._diameter)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		color = self._on_color if self._led else self._off_color
		if self._shape == 'round':
			gradient = makeRadialGradient(led_size, x, y, self._diameter, color)
		else:
			gradient = makeLinearGradient(led_size, x, y, color)

		painter.setBrush(QBrush(gradient))
		painter.setPen(color)

		if self._shape == 'square':
			painter.drawRect(int(x_center - (self._diameter / 2)), int(y_center - (self._diameter / 2)), self._diameter, self._diameter)
		else:
			painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)

	def setLed(self, val):
		self._led = val
		self.update()

	def getLed(self):
		self.update()
		return self._led

	led = pyqtProperty(bool, getLed, setLed)

# A QLabel with a LED in the upper right corner
class IndicatorLabel(QLabel):
	_led = False

	def __init__(self, **kwargs):
		super().__init__()
		self.setText(kwargs['text'])
		self._diameter = kwargs['diameter']
		self._top_offset = kwargs['top_offset']
		self._right_offset = kwargs['right_offset']
		self._on_color = kwargs['on_color']
		self._off_color = kwargs['off_color']
		self._shape = kwargs['shape']

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		x_center = size.width() - ((self._diameter / 2) + self._right_offset)
		y_center = (self._diameter / 2) + self._top_offset
		x = size.width() - self._diameter - self._right_offset
		y = self._top_offset
		led_size = QSize(self._diameter, self._diameter)

		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		color = self._on_color if self._led else self._off_color
		if self._shape == 'round' or led_size.width() == led_size.height():
			gradient = makeRadialGradient(led_size, x, y, self._diameter, color)
		else:
			gradient = makeLinearGradient(led_size, x, y, color)
		
		painter.setBrush(QBrush(gradient))
		painter.setPen(color)

		if self._shape == 'square':
			painter.drawRect(int(x_center - (self._diameter / 2)), int(y_center - (self._diameter / 2)), self._diameter, self._diameter)
		else:
			painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)

	def setLed(self, val):
		self._led = val
		self.update()

	def getLed(self):
		self.update()
		return self._led

	led = pyqtProperty(bool, getLed, setLed)

# A blank QLabel with a LED in the center
class Indicator(QLabel):
	_led = False

	def __init__(self, **kwargs):
		super().__init__()
		self._diameter = kwargs['diameter']
		self._margin = kwargs['margin']
		self._on_color = kwargs['on_color']
		self._off_color = kwargs['off_color']
		self._shape = kwargs['shape']

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		# get the diameter that will make a full circle
		dia = min(size.width(), size.height()) - self._margin
		# get the center of the label
		x_center = size.width() / 2
		y_center = size.height() / 2
		x = x_center - (dia / 2)
		y = y_center - (dia / 2)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		color = self._on_color if self._led else self._off_color
		if self._shape == 'round' or size.width() == size.height():
			gradient = makeRadialGradient(size, x, y, dia, color)
		else:
			gradient = makeLinearGradient(size, 0, 0, color)
		
		painter.setBrush(QBrush(gradient))
		painter.setPen(color)

		if self._shape == 'square':
			painter.drawRect(0,0,size.width(), size.height())
		else:
			painter.drawEllipse(QPointF(x_center, y_center), dia / 2, dia / 2)

	def setLed(self, val):
		self._led = val
		self.update()

	def getLed(self):
		self.update()
		return self._led

	led = pyqtProperty(bool, getLed, setLed)

