import os

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMessageBox, QCheckBox, QSpinBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from libflexgui import number_pad
from libflexgui import gcode_pad
from libflexgui import keyboard_pad
from libflexgui import utilities

def spinbox_numbers(parent, obj):
	np = number_pad.number_pad()
	print(type(obj))
	stylesheet = os.path.join(parent.lib_path, 'touch.qss')
	with open(stylesheet,'r') as fh:
		np.setStyleSheet(fh.read())
	result = np.exec()
	if result:
		number = utilities.convert_string_to_number(np.retval())
		if number:
			if isinstance(obj, QSpinBox): # return an int
				obj.setValue(int(number))
			else:
				obj.setValue(number)

def numbers(parent, obj):
	np = number_pad.number_pad()
	stylesheet = os.path.join(parent.lib_path, 'touch.qss')
	with open(stylesheet,'r') as fh:
		np.setStyleSheet(fh.read())
	result = np.exec()
	if result:
		obj.setText(np.retval())

def gcode(parent, obj):
	gp = gcode_pad.gcode_pad()
	stylesheet = os.path.join(parent.lib_path, 'touch.qss')
	with open(stylesheet,'r') as fh:
		gp.setStyleSheet(fh.read())
	result = gp.exec()
	if result:
		obj.setText(gp.retval())

def keyboard(parent, obj):
	kb = keyboard_pad.keyboard_pad()
	result = kb.exec()
	if result:
		obj.setText(kb.retval())

def question_msg_yes_no_check(body_text, chkbx_text, title=None):
	chkBox = QCheckBox()
	chkBox.setText(chkbx_text)
	msg_box = QMessageBox()
	msg_box.setCheckBox(chkBox)
	msg_box.setIcon(QMessageBox.Icon.Question)
	msg_box.setWindowTitle(title)
	msg_box.setText(body_text)
	msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
	returnValue = msg_box.exec()
	answer = True if returnValue == QMessageBox.StandardButton.Yes else False
	return answer, chkBox.isChecked()

def info_msg_ok(text, title=None):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Icon.Information)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.StandardButton.Ok:
		return True
	else:
		return False

def warn_msg_ok(text, title=None):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Icon.Warning)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.StandardButton.Ok:
		return True
	else:
		return False

def warn_msg_cancel_ok(text, title=None):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Icon.Warning)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.StandardButton.Cancel | QMessageBox.StandardButton.Ok)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.StandardButton.Ok:
		return True
	else:
		return False

def warn_msg_yes_no(text, title=None):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Icon.Warning)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.StandardButton.Yes:
		return True
	else:
		return False

def warn_msg_yes_no_check(body_text, chkbx_text, title=None):
	chkBox = QCheckBox()
	chkBox.setText(chkbx_text)
	msg_box = QMessageBox()
	msg_box.setCheckBox(chkBox)
	msg_box.setIcon(QMessageBox.Icon.Warning)
	msg_box.setWindowTitle(title)
	msg_box.setText(body_text)
	msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
	returnValue = msg_box.exec()
	answer = True if returnValue == QMessageBox.StandardButton.Yes else False
	return answer, chkBox.isChecked()

def critical_msg_ok(text, title=None):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Icon.Critical)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.StandardButton.Ok:
		return True
	else:
		return False

def about_dialog(parent):
	dialog_box = QDialog()
	dialog_box.setMinimumSize(300, 300)
	dialog_box.setWindowTitle('About')

	layout = QVBoxLayout(dialog_box)

	titleLabel =  QLabel()
	titleLabel.setText('FlexGUI')
	titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	layout.addWidget(titleLabel)

	imageLabel = QLabel()
	imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

	image_path = os.path.join(parent.lib_path, 'flexgui.jpg')
	pixmap = QPixmap(image_path)
	pixmap = pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio)
	imageLabel.setPixmap(pixmap)
	layout.addWidget(imageLabel)

	authorLabel =  QLabel()
	authorLabel.setText('Author: John Thornton')
	authorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	layout.addWidget(authorLabel)

	versionLabel =  QLabel()
	versionLabel.setText(f'Version: {parent.flex_version}')
	versionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	layout.addWidget(versionLabel)

	aboutLabel =  QLabel()
	aboutLabel.setText('Flexible Graphical User Interface\nfor LinuxCNC')
	aboutLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	layout.addWidget(aboutLabel)

	websiteLabel =  QLabel()
	websiteLabel.setText("<a href='https://gnipsel.com/'>Authors Website</a>")
	websiteLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	websiteLabel.setOpenExternalLinks(True)
	layout.addWidget(websiteLabel)

	docsLabel =  QLabel()
	docsLabel.setText("<a href='https://gnipsel.com/linuxcnc/flexgui/index.html'>Documents</a>")
	docsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	docsLabel.setOpenExternalLinks(True)
	layout.addWidget(docsLabel)

	repoLabel =  QLabel()
	repoLabel.setText("<a href='https://github.com/jethornton/flexgui'>Code Website</a>")
	repoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	repoLabel.setOpenExternalLinks(True)
	layout.addWidget(repoLabel)

	videoLabel =  QLabel()
	videoLabel.setText("<a href='https://www.youtube.com/@Gnipsel/videos'>Youtube Videos</a>")
	videoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	videoLabel.setOpenExternalLinks(True)
	layout.addWidget(videoLabel)

	from datetime import datetime
	year = datetime.today().year
	copyrightLabel =  QLabel()
	copyrightLabel.setText(f'Copyright © 1953-{year} John Thornton')
	copyrightLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	layout.addWidget(copyrightLabel)

	layout.addStretch()

	buttonBox = QDialogButtonBox()
	buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
	buttonBox.setCenterButtons(True)
	#buttonBox.addButton("Credits", QDialogButtonBox.ActionRole)
	buttonBox.accepted.connect(dialog_box.close)
	layout.addWidget(buttonBox)

	dialog_box.exec()

def quick_reference_dialog(parent):
	dialog_box = QDialog()
	dialog_box.setMinimumSize(300, 300)
	dialog_box.setWindowTitle('Keyboard Shortcuts')

	layout = QVBoxLayout(dialog_box)

	titleLabel =  QLabel()
	titleLabel.setText('FlexGUI')
	titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	layout.addWidget(titleLabel)

	shortcutsLabel =  QLabel()
	if len(parent.shortcuts) > 0:
		shortcutsLabel.setText('  \n'.join(parent.shortcuts))
	else:
		shortcutsLabel.setText('No Keyboard Shortcuts Found')
	#shortcutsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
	layout.addWidget(shortcutsLabel)

	layout.addStretch()

	buttonBox = QDialogButtonBox()
	buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)
	buttonBox.setCenterButtons(True)
	buttonBox.accepted.connect(dialog_box.close)
	layout.addWidget(buttonBox)

	dialog_box.exec()


