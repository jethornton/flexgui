
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import pyqtProperty, pyqtSignal

import glnav
from rs274 import glcanon

class plotter(QOpenGLWidget, glcanon.GlCanonDraw, glnav.GlNavBase):
		percentLoaded = pyqtSignal(int)
		xRotationChanged = pyqtSignal(int)
		yRotationChanged = pyqtSignal(int)
		zRotationChanged = pyqtSignal(int)
		rotation_vectors = [(1.,0.,0.), (0., 0., 1.)]


	def __init__(self):
		super().__init__()
		glnav.GlNavBase.__init__(self)

		parent.plot = QOpenGLWidget()
		layout = QVBoxLayout(parent.plot_widget)
		layout.addWidget(parent.plot)
		self.timer = QTimer()
		self.timer.timeout.connect(self.poll)
		self.timer.start(100)

	def poll(self):
		pass
