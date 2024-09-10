#!/usr/bin/env python3

import sys, os

# importing libraries 
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt6.QtGui import QIcon 
#from PyQt6.QtCore import * 

## Syntax : button.setStyleSheet(“background-image : url(image.png);”)
## Argument : It takes string as argument.
## Action performed : It sets background image to the button.  

class Window(QMainWindow): 
	def __init__(self): 
		super().__init__() 
  
		# setting title 
		self.setWindowTitle("Python ") 
  
		# setting geometry 
		self.setGeometry(100, 100, 600, 400) 
  
		# calling method 
		self.UiComponents() 
  
		# showing all the widgets 
		self.show() 

	# method for widgets 
	def UiComponents(self): 

		# creating a push button 
		button = QPushButton("CLICK", self) 

		# setting geometry of button 
		#button.setGeometry(200, 150, 100, 30) 
		button.setGeometry(200, 150, 70, 70) 
		#button.setGeometry(200, 150, 63, 63) 
  
		# adding action to a button 
		button.clicked.connect(self.clickme) 
  
		# setting image to the button 
		#button.setStyleSheet("background-image : url(image.png);") 
		#button.setStyleSheet("background-image : url(/home/tom/linuxcnc/configs/test_gui/inHole.png);") 
		#image_path = os.path.join(os.getcwd(),'inHole.png')
		#print(image_path)
		#button.setStyleSheet("background-image : url(image_path);")
		button.setIcon(QIcon('inHole.jpg'))

		# action method 
	def clickme(self): 

		# printing pressed 
		print("pressed") 

# create pyqt5 app 
App = QApplication(sys.argv) 

# create the instance of our Window 
window = Window() 

# start the app 
sys.exit(App.exec()) 

## Notes
## another possible method
## button.setStyleSheet("qproperty-icon: url(:/path/to/images.png);");
