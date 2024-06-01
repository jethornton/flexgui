#!/usr/bin/env python3

import sys, math

from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class main(QMainWindow):
	verticies = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1),
	(1, 1, 1), (-1, -1, 1), (-1, 1, 1))

	edges = ((0,1), (0,3), (0,4), (2,1), (2,3), (2,7), (6,3), (6,4), (6,7),
	(5,1), (5,4), (5,7))

	width = 500
	height = 500

	def __init__(self):
		super().__init__()
		self.setGeometry(50, 50, self.width, self.height)

		self.openGLWidget = QOpenGLWidget(self)
		self.openGLWidget.setGeometry(0, 0, self.width, self.height)
		self.openGLWidget.initializeGL()
		self.openGLWidget.paintGL = self.paintGL
		print(self.openGLWidget.size().width())
		print(self.openGLWidget.size().height())

		self.x_angle = 0
		self.y_angle = 0
		self.z_angle = 0
		self.zoom = 1.0

		self.show()

	def rotate_x(self, angle):
		self.x_angle = angle
		self.openGLWidget.update()

	def rotate_y(self, angle):
		self.y_angle = angle
		self.openGLWidget.update()

	def rotate_z(self, angle):
		self.z_angle = angle
		self.openGLWidget.update()

	def keyPressEvent(self, event):

		if event.key() == Qt.Key.Key_0:
			print(self.size().width())
			print(self.size().height())

		if event.key() == Qt.Key.Key_Up:
			self.x_angle -= 5
		if event.key() == Qt.Key.Key_Down:
			self.x_angle += 5
		if event.key() == Qt.Key.Key_Left:
			self.y_angle += 5
		if event.key() == Qt.Key.Key_Right:
			self.y_angle -= 5
		if event.key() == Qt.Key.Key_Plus:
			self.zoom += 0.1
		if event.key() == Qt.Key.Key_Minus:
			self.zoom -= 0.1
		self.openGLWidget.update()

	def mousePressEvent(self, event):
		self.lastPos = event.pos()

	def mouseMoveEvent(self, event):
		dx = event.pos().x() - self.lastPos.x()
		dy = event.pos().y() - self.lastPos.y()
		if Qt.MouseButton.LeftButton:
			self.rotate_x(dx)
			self.rotate_y(dy)

		'''
		y1 = self.lastPos.y()
		y2 = event.pos().y()
		x1 = self.lastPos.x()
		x2 = event.pos().x()
		if event.buttons() & Qt.MouseButton.LeftButton:
			self.angle = math.degrees(math.atan2(y2-y1, x2-x1))
			self.openGLWidget.update()
		'''

	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		glScale(self.zoom, self.zoom, self.zoom)
		# gluPerspective(	GLdouble fovy, GLdouble aspect, GLdouble zNear, GLdouble zFar)
		# fovy Specifies the field of view angle, in degrees, in the y direction. 
		# aspect Specifies the aspect ratio that determines the field of view in the x direction
		# The aspect ratio is the ratio of x (width) to y (height)
		# zNear Specifies the distance from the viewer to the near clipping plane (always positive)
		# zFar Specifies the distance from the viewer to the far clipping plane (always positive)
		gluPerspective(45, self.width / self.height, 0.1, 50.0)
		# glTranslatef(	GLfloat x, GLfloat y, GLfloat z)
		# x, y, z Specify the x, y, and z coordinates of a translation vector. 
		glTranslatef(0, 0, -10)
		# glRotatef(GLfloat angle, GLfloat x, GLfloat y, GLfloat z)
		# angle Specifies the angle of rotation, in degrees
		# x, y, z Specify the x, y, and z coordinates of a vector, respectively
		#print(self.angle)
		glRotated(self.x_angle, 1.0, 0.0, 0.0)
		glRotated(self.y_angle, 0.0, 1.0, 0.0)
		glRotated(self.z_angle, 0.0, 0.0, 1.0)
		#glRotatef(self.angle, 1, 1, 0)

		glBegin(GL_LINES)
		for edge in self.edges:
			for vertex in edge:
				glVertex3fv(self.verticies[vertex])
		glEnd()

app = QApplication([])
window = main()
sys.exit(app.exec())

