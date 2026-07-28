
from PyQt6.QtCore import Qt, pyqtProperty, pyqtSignal, QPointF, QSize, QRectF
from PyQt6.QtGui import QRadialGradient, QLinearGradient, QPainter
from PyQt6.QtGui import QBrush, QColor, QPen, QPalette, QFont
from PyQt6.QtWidgets import QPushButton, QLabel

'''
LED Types
Label LED as background no text, String function=hal_led, Indicator
Label LED as background with text, String function=hal_led_text, LEDTextLabel
Label LED in upper right corner, String function=hal_led_label, IndicatorLabel
Button LED in upper right corner, String function=hal_led_button, LEDButton
Control Button LED, Bool=led_indicator, IndicatorButton
'''

# NEW Helper gradient functions
def linear_gradient(x, y, diameter, color):
	# Using relative ObjectMode ensures it stretches properly with the shape
	gradient = QLinearGradient(QPointF(0.0, 0.0), QPointF(1.0, 1.0))
	gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectMode)
	gradient.setColorAt(0.0, QColor('white'))
	gradient.setColorAt(0.2, QColor(color))
	gradient.setColorAt(1.0, QColor(color).darker(150))
	return gradient

def radial_gtradient(x, y, diameter, color):
	# Fixed coordinates based on the LED bounding box for consistent look
	radius = diameter / 2
	cx = x + radius
	cy = y + radius
	gradient = QRadialGradient(QPointF(cx, cy), radius, QPointF(cx - radius * 0.3, cy - radius * 0.3))
	gradient.setColorAt(0.0, QColor('white'))
	gradient.setColorAt(0.3, QColor(color))
	gradient.setColorAt(1.0, QColor(color).darker(200))
	return gradient

# gradient functions used by LED objects
def makeLinearGradient(size, x, y, color):
	# Create gradient from top-left (0,0) to bottom-right (1,1)
	gradient = QLinearGradient(QPointF(0.0, 0.0), QPointF(1.0, 1.0))
	gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectMode)
	gradient.setColorAt(0.0, QColor(color))
	gradient.setColorAt(0.01, QColor('white'))
	gradient.setColorAt(0.1, QColor('white'))
	gradient.setColorAt(1.0, QColor(color))
	return gradient

def makeRadialGradient(size, x, y, diameter, color):
	gradient = QRadialGradient(x + diameter / 2, y + diameter / 2,
		diameter * 0.5, diameter * 0.9, diameter * 0.2)
	gradient.setColorAt(0, Qt.GlobalColor.white)
	gradient.setColorAt(1, color)
	return gradient

'''
def radial_gradient(size, x, y, color): # FIXME not used anywhere
	# Define the center and focal point of the gradient
	# Offset from the upper-left edge (e.g., 50 pixels down and right)
	cx, cy = 8.0, 8.0
	radius = max(self.width(), self.height())

	# Create the radial gradient
	gradient = QRadialGradient(QPointF(cx, cy), radius)

	# Set colors: Starts white at the center, transitions to blue at the edge
	gradient.setColorAt(0.0, QColor(230, 230, 230, 255))
	gradient.setColorAt(0.08, QColor(color))
	#gradient.setColorAt(1.0, QColor(color))
	return gradient
'''

# A blank QLabel with a LED in the center
class Indicator(QLabel):
	_state = False

	def __init__(self, **kwargs):
		super().__init__()

		self._diameter = kwargs['diameter']
		self._margin = kwargs['margin']
		self._on_color = kwargs['on_color']
		self._off_color = kwargs['off_color']
		self._shape = kwargs['shape']

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True) # new
		size = self.rect()
		is_round = self._shape == 'round' or size.width() == size.height()
		
		# --- 1. SETUP LED GEOMETRY & GRADIENT ---
		# Shrink usable diameter slightly to sit cleanly inside the outer border
		dia = min(size.width(), size.height()) - self._margin - 4
		x_center = size.width() / 2
		y_center = size.height() / 2
		x = x_center - (dia / 2)
		y = y_center - (dia / 2)

		color = self._on_color if self._state else self._off_color
		if is_round:
			gradient = makeRadialGradient(size, x, y, dia, color)
		else:
			gradient = makeLinearGradient(size, 0, 0, color)

		# --- 2. DRAW THE LED FILL ---
		painter.setBrush(QBrush(gradient))
		painter.setPen(Qt.PenStyle.NoPen) # Remove pen to prevent sharp color bleed

		if is_round:
			painter.drawEllipse(QPointF(x_center, y_center), dia / 2, dia / 2)
		else:
			# Shrunk by 2px on all sides to fit cleanly inside the border
			# Uses 5px corner radius for the inner fill
			painter.drawRoundedRect(2, 2, size.width() - 4, size.height() - 4, 5, 5)

		# --- 3. DRAW THE MATCHING BLACK BORDER ---
		border_pen = QPen(QColor("black"))
		border_pen.setWidth(2)
		painter.setPen(border_pen)
		painter.setBrush(Qt.BrushStyle.NoBrush)
		
		if is_round:
			# Match the exact circular shape of the LED, positioned at the outer limit
			border_dia = min(size.width(), size.height()) - 2
			bx = x_center - (border_dia / 2)
			by = y_center - (border_dia / 2)
			painter.drawEllipse(QRectF(bx, by, border_dia, border_dia))
		else:
			# 2px border offset by 1px to stay inside widget boundaries
			# Uses 7px corner radius so it curves smoothly with the inner fill
			painter.drawRoundedRect(1, 1, size.width() - 2, size.height() - 2, 7, 7)

	def setLed(self, val):
		if self._state != val:
			self._state = val
			self.update() # Triggers paintEvent safely

	def getLed(self):
		return self._state

	# expose property
	state = pyqtProperty(bool, getLed, setLed)

# A QLabel with LED background, custom text and a border
class LEDTextLabel(QLabel):
	# On Off state
	_state = False

	def __init__(self, **kwargs):
		super().__init__()
		self._on_bg_color = kwargs['on_bg_color']
		self._off_bg_color = kwargs['off_bg_color']
		self._on_text_color = kwargs['on_text_color']
		self._off_text_color = kwargs['off_text_color']
		self._on_text = kwargs['on_text']
		self._off_text = kwargs['off_text']

		self.setAlignment(kwargs['alignment'])

		custom_font = kwargs['font_family']
		custom_font.setBold(kwargs['font_bold'])
		self.setFont(custom_font)
		self.setText(self._off_text)

	def _sync_label_properties(self):
		# Synchronizes label text matching the active component state.
		if self._state:
			self.setText(self._on_text)
		else:
			self.setText(self._off_text)

		# Update text color via QPalette
		color = self._on_text_color if self._state else self._off_text_color
		palette = self.palette()
		palette.setColor(QPalette.ColorRole.WindowText, color)
		self.setPalette(palette)

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)

		color = self._on_bg_color if self._state else self._off_bg_color

		# Define the center and focal point of the gradient
		# Offset from the upper-left edge (e.g., 8 pixels down and right)
		cx, cy = 8.0, 8.0
		radius = max(self.width(), self.height())

		# Create the radial gradient
		gradient = QRadialGradient(QPointF(cx, cy), radius)

		# Set colors: Starts white at the center, transitions to color
		gradient.setColorAt(0.0, QColor(255, 255, 255, 255))
		gradient.setColorAt(0.1, QColor(color))

		painter.setBrush(QBrush(gradient))

		# Black border pen (width 2)
		pen = QPen(QColor('black'), 2)
		painter.setPen(pen)

		# Offset bounds by half the pen width (2px) to prevent border clipping
		rect = QRectF(self.rect()).adjusted(2, 2, -2, -2)

		# Draw the rounded rectangle shape (8px radius)
		painter.drawRoundedRect(rect, 8.0, 8.0)

		# Close painter before calling super
		painter.end()

		# Draw text on top
		super().paintEvent(event)

	def setLed(self, val):
		if self._state != val:
			self._state = val
			self._sync_label_properties() # Update string resource
			self.update() # Triggers paintEvent safely

	def getLed(self):
		return self._state

	# expose property
	state = pyqtProperty(bool, getLed, setLed)

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

# Control Button with a LED in the upper right corner, Bool=led_indicator
class IndicatorButton(QPushButton):
	_state = False

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
		led_size = QSize(self._diameter, self._diameter)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

		color = self._on_color if self._state else self._off_color
		gradient = makeRadialGradient(led_size, x, y, self._diameter, color)

		painter.setBrush(QBrush(gradient))
		painter.setPen(color)
		painter.drawEllipse(QPointF(x_center, y_center), self._diameter / 2, self._diameter / 2)

	def setLed(self, val):
		if self._state != val:
			self._state = val
			self.update() # only triggers paintEvent when the state changes

	def getLed(self):
		return self._state

	# expose property
	state = pyqtProperty(bool, getLed, setLed)

# A QLabel with a LED in the upper right corner
class IndicatorLabel(QLabel):
	_state = False

	def __init__(self, **kwargs):
		super().__init__()
		self.setText(kwargs['text'])
		self._diameter = kwargs['diameter']
		self._top_offset = kwargs['top_offset']
		self._right_offset = kwargs['right_offset']
		self._on_color = kwargs['on_color']
		self._off_color = kwargs['off_color']
		self._shape = kwargs['shape']
		#self.setSizePolicy(kwargs['size_policy']) # FIXME move to startup

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

		color = self._on_color if self._state else self._off_color
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
		if self._state != val:
			self._state = val
			self.update() # Triggers paintEvent safely

	def getLed(self):
		return self._state

	# expose property
	state = pyqtProperty(bool, getLed, setLed)

