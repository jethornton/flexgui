
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import glnav
from rs274 import glcanon

class plotter(QOpenGLWidget, glcanon.GlCanonDraw, glnav.GlNavBase):
	def __init__(self):
		super().__init__()
		glnav.GlNavBase.__init__(self)

		parent.plot = QOpenGLWidget()
		layout = QVBoxLayout(parent.plot_widget)
		layout.addWidget(parent.plot)
    self.timer = QTimer()
    self.timer.timeout.connect(self.poll)
    self.timer.start(100)


