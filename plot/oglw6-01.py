#!/usr/bin/env python3

import sys

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import pyqtSignal, QPoint, Qt

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class mainWindow(QMainWindow):	#Main class.
	verticies = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1),
	(1, 1, 1), (-1, -1, 1), (-1, 1, 1))

	edges = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7),
	(5,1), (5,4), (5,7))

	colors = ((1,0,0), (0,1,0), (0,0,1), (0,1,0), (1,1,1), (0,1,1), (1,0,0),
	(0,1,0), (0,0,1), (1,0,0), (1,1,1), (0,1,1), )

	surfaces = ((0,1,2,3), (3,2,7,6), (6,7,5,4), (4,5,1,0), (1,5,7,2), (4,0,3,6))

	def __init__(self):
		super(mainWindow, self).__init__()
		self.width = 700	#Variables used for the setting of the size of everything
		self.height = 600
		self.setGeometry(0, 0, self.width, self.height)	#Set the window size

		self.openGLWidget = QOpenGLWidget(self)	#Create the GLWidget
		self.openGLWidget.setGeometry(0, 0, self.width, self.height)	#Size it the same as the window.
		self.openGLWidget.initializeGL()
		self.openGLWidget.resizeGL(self.width, self.height)	#Resize GL's knowledge of the window to match the physical size?
		self.openGLWidget.paintGL = self.paintGL	#override the default function with my own?

		self.xRot = 0
		self.yRot = 0
		self.zRot = 0
		self.lastPos = QPoint()

		self.show()

	def mousePressEvent(self, event):
		self.lastPos = event.pos()

	def mouseMoveEvent(self, event):
		dx = event.pos().x() - self.lastPos.x()
		dy = event.pos().y() - self.lastPos.y()

		if event.buttons() & Qt.MouseButton.LeftButton:
			self.setXRotation(self.xRot + 8 * dy)
			self.setYRotation(self.yRot + 8 * dx)
		elif event.buttons() & Qt.MouseButton.RightButton:
			self.setXRotation(self.xRot + 8 * dy)
			self.setZRotation(self.zRot + 8 * dx)

	def setXRotation(self, angle):
		angle = self.normalizeAngle(angle)
		if angle != self.xRot:
			self.xRot = angle
			self.update()

	def setYRotation(self, angle):
		angle = self.normalizeAngle(angle)
		if angle != self.yRot:
			self.yRot = angle
			self.update()

	def setZRotation(self, angle):
		angle = self.normalizeAngle(angle)
		if angle != self.zRot:
			self.zRot = angle
			self.update()

	def normalizeAngle(self, angle):
		while angle < 0:
			angle += 360 * 16
		while angle > 360 * 16:
			angle -= 360 * 16
		return angle

	def paintGL(self):
		glLoadIdentity()
		gluPerspective(45, self.width / self.height, 0.1, 50.0)	#set perspective?
		glTranslatef(0, 0, -5)	#I used -10 instead of -2 in the PyGame version.
		#glRotatef(-90, 1, 0, 0)	#I used 2 instead of 1 in the PyGame version.
		glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
		glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
		glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)	#Straight from the PyGame version, with 'self' inserted occasionally
		glBegin(GL_LINES) #tell GL to draw lines
		for edge in self.edges:
			for vertex in edge:
				glVertex3fv(self.verticies[vertex])
		glEnd()	#tell GL to stop drawing lines.

app = QApplication([])
window = mainWindow()
sys.exit(app.exec())
