import os

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMessageBox, QCheckBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

def warn_msg_cancel_ok(text, title):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Warning)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.Ok:
		return True
	else:
		return False

def warn_msg_ok(text, title=None):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Warning)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.Ok)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.Ok:
		return True
	else:
		return False

def warn_msg_yes_no(text, title=None):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Warning)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.Yes:
		return True
	else:
		return False

def warn_msg_yes_no_check(title, body_text, chkbx_text):
	chkBox = QCheckBox()
	chkBox.setText(chkbx_text)
	msg_box = QMessageBox()
	msg_box.setCheckBox(chkBox)
	msg_box.setIcon(QMessageBox.Warning)
	msg_box.setWindowTitle(title)
	msg_box.setText(body_text)
	msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
	returnValue = msg_box.exec()
	answer = True if returnValue == QMessageBox.Yes else False
	return answer, chkBox.isChecked()

def question_msg_yes_no_check(title, body_text, chkbx_text):
	chkBox = QCheckBox()
	chkBox.setText(chkbx_text)
	msg_box = QMessageBox()
	msg_box.setCheckBox(chkBox)
	msg_box.setIcon(QMessageBox.Question)
	msg_box.setWindowTitle(title)
	msg_box.setText(body_text)
	msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
	returnValue = msg_box.exec()
	answer = True if returnValue == QMessageBox.Yes else False
	return answer, chkBox.isChecked()

def info_msg_ok(text, title=None):
	msg_box = QMessageBox()
	msg_box.setIcon(QMessageBox.Information)
	msg_box.setWindowTitle(title)
	msg_box.setText(text)
	msg_box.setStandardButtons(QMessageBox.Ok)
	returnValue = msg_box.exec()
	if returnValue == QMessageBox.Ok:
		return True
	else:
		return False

def about_dialog(parent):
	dialog_box = QDialog()
	dialog_box.setMinimumSize(300, 300)
	dialog_box.setWindowTitle('About')

	layout = QVBoxLayout(dialog_box)

	titleLabel =  QLabel()
	titleLabel.setText('Mesa Configuration Tool')
	titleLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(titleLabel)

	imageLabel = QLabel()
	imageLabel.setAlignment(Qt.AlignCenter)

	image_path = os.path.join(parent.lib_path, 'mesact.jpg')
	pixmap = QPixmap(image_path)
	pixmap = pixmap.scaled(256, 256, Qt.KeepAspectRatio)
	imageLabel.setPixmap(pixmap)
	layout.addWidget(imageLabel)

	authorLabel =  QLabel()
	authorLabel.setText('Author: John Thornton')
	authorLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(authorLabel)

	versionLabel =  QLabel()
	versionLabel.setText(f'Version: {parent.version}')
	versionLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(versionLabel)

	aboutLabel =  QLabel()
	aboutLabel.setText('Mesa CT Creates LinuxCNC\nconfigurations for Mesa Boards')
	aboutLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(aboutLabel)

	websiteLabel =  QLabel()
	websiteLabel.setText("<a href='https://gnipsel.com/'>Authors Website</a>")
	websiteLabel.setAlignment(Qt.AlignCenter)
	websiteLabel.setOpenExternalLinks(True)
	layout.addWidget(websiteLabel)

	repoLabel =  QLabel()
	repoLabel.setText("<a href='https://github.com/jethornton/mesact'>Code Website</a>")
	repoLabel.setAlignment(Qt.AlignCenter)
	repoLabel.setOpenExternalLinks(True)
	layout.addWidget(repoLabel)

	copyrightLabel =  QLabel()
	copyrightLabel.setText('Copyright © 1953-2023 John Thornton')
	copyrightLabel.setAlignment(Qt.AlignCenter)
	layout.addWidget(copyrightLabel)

	layout.addStretch()

	buttonBox = QDialogButtonBox()
	buttonBox.setStandardButtons(QDialogButtonBox.Ok)
	buttonBox.setCenterButtons(True)
	#buttonBox.addButton("Credits", QDialogButtonBox.ActionRole)
	buttonBox.accepted.connect(dialogBox.close)
	layout.addWidget(buttonBox)

	dialogBox.exec()

