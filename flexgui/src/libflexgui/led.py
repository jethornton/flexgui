
from PyQt6.QtCore import Qt, pyqtProperty, pyqtSignal, QPointF, QEvent
from PyQt6.QtGui import QRadialGradient, QPainter, QColor, QBrush, QPainter
from PyQt6.QtWidgets import QPushButton, QLabel

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

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		x_center = size.width() - ((self._diameter / 2) + self._right_offset)
		y_center = (self._diameter / 2) + self._top_offset
		x = size.width() - self._diameter - self._right_offset
		y = self._top_offset
		gradient = QRadialGradient(x + self._diameter / 2, y + self._diameter / 2,
			self._diameter * 0.4, self._diameter * 0.4, self._diameter * 0.4)
		gradient.setColorAt(0, Qt.GlobalColor.white)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		if self._led:
			gradient.setColorAt(1, self._on_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(self._on_color)
			# Draws the ellipse positioned at center with radii rx and ry.
			painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)
		else:
			gradient.setColorAt(1, self._off_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(self._off_color)
			painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)

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

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		x_center = size.width() - ((self._diameter / 2) + self._right_offset)
		y_center = (self._diameter / 2) + self._top_offset
		x = size.width() - self._diameter - self._right_offset
		y = self._top_offset
		gradient = QRadialGradient(x + self._diameter / 2, y + self._diameter / 2,
			self._diameter * 0.4, self._diameter * 0.4, self._diameter * 0.4)
		gradient.setColorAt(0, Qt.GlobalColor.white)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		if self._led:
			gradient.setColorAt(1, self._on_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(self._on_color)
			# Draws the ellipse positioned at center with radii rx and ry.
			painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)
		else:
			gradient.setColorAt(1, self._off_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(self._off_color)
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

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		x_center = size.width() - ((self._diameter / 2) + self._right_offset)
		y_center = (self._diameter / 2) + self._top_offset
		x = size.width() - self._diameter - self._right_offset
		y = self._top_offset
		gradient = QRadialGradient(x + self._diameter / 2, y + self._diameter / 2,
			self._diameter * 0.4, self._diameter * 0.4, self._diameter * 0.4)
		gradient.setColorAt(0, Qt.GlobalColor.white)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		if self._led:
			gradient.setColorAt(1, self._on_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(self._on_color)
			# Draws the ellipse positioned at center with radii rx and ry.
			painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)
		else:
			gradient.setColorAt(1, self._off_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(self._off_color)
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

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		size = self.rect()
		# get the diameter that will make a full circle
		dia = min(size.width(), size.height()) - self._margin
		# get the center of the label
		x_center = size.width() / 2
		y_center = size.height() / 2
		x = size.width() - dia
		y = size.height() - dia
		# QRadialGradient(center_x, center_y, radius, focal_x, focal_y)
		gradient = QRadialGradient(x_center, y_center, dia * 0.5, dia * 0.9, dia * 0.2)
		# setColorAt(pos, color) Creates a stop point at the given position with the given color.
		# The given position must be in the range 0 to 1.
		gradient.setColorAt(0, Qt.GlobalColor.white)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		if self._led:
			gradient.setColorAt(1, self._on_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(self._on_color)
			# Draws the ellipse positioned at center with radii rx and ry.
			#painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)
			painter.drawEllipse(QPointF(x_center, y_center), dia / 2, dia / 2)
		else:
			gradient.setColorAt(1, self._off_color)
			painter.setBrush(QBrush(gradient))
			painter.setPen(self._off_color)
			painter.drawEllipse(QPointF(x_center, y_center), dia / 2, dia / 2)

	def setLed(self, val):
		self._led = val
		self.update()

	def getLed(self):
		self.update()
		return self._led

	led = pyqtProperty(bool, getLed, setLed)

