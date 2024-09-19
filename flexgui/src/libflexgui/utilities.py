import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor, QPalette, QTextFormat
from PyQt6.QtWidgets import QApplication, QTextEdit

import linuxcnc as emc

def is_float(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def all_homed(parent):
	parent.status.poll()
	return parent.status.homed.count(1) == parent.status.joints

def all_unhomed(parent):
	parent.status.poll()
	num_joints = parent.status.joints
	home_status = parent.status.homed[:num_joints]
	test_list = []
	for i in range(num_joints):
		test_list.append(0)
	test_tuple = tuple(test_list)
	return home_status == test_tuple

def home_all_check(parent):
	parent.status.poll()
	for i in range(parent.status.joints):
		if parent.inifile.find(f'JOINT_{i}', 'HOME_SEQUENCE') is None:
			return False
	return True

def set_enables(parent): # FIXME this may handle enables dunno
	print('set_enables')
	if parent.status.task_state == emc.STATE_ESTOP:
		# everything disabled except the E Stop
		print('STATE_ESTOP')

	elif parent.status.task_state == emc.STATE_ESTOP_RESET:
		# everything disabled except the Power
		print('STATE_ESTOP_RESET')

	elif parent.status.task_state == emc.STATE_ON:
		print('STATE_ON')
		if parent.status.motion_mode == emc.TRAJ_MODE_TELEOP:
			# all joints are homed
			print('All Homed')
			for item in parent.home_required:
				getattr(parent, item).setEnabled(True)
			if parent.status.file:
				for item in parent.run_controls:
					getattr(parent, item).setEnabled(True)
		elif parent.status.motion_mode == emc.TRAJ_MODE_FREE:
			# a joint is not homed
			print('All NOT Homed')
			for item in parent.home_required:
				getattr(parent, item).setEnabled(False)
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(False)



	# STATE_ON
	# ALL HOMED
	# FILE LOADED


def set_homed_enable(parent):
	for item in parent.home_controls:
		getattr(parent, item).setEnabled(False)
	for item in parent.unhome_controls:
		getattr(parent, item).setEnabled(True)
	for item in parent.home_required:
		getattr(parent, item).setEnabled(True)
	if parent.status.file:
		for item in parent.run_controls:
			getattr(parent, item).setEnabled(True)

def update_jog_lb(parent):
	parent.jog_vel_lb.setText(f'{parent.jog_vel_sl.value()} {parent.units}/min')

def add_mdi(parent):
	parent.mdi_command_le.setText(f'{parent.mdi_history_lw.currentItem().text()}')

def copy_errors(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.errors_pte.toPlainText())
	parent.statusbar.showMessage('Errors copied to clipboard')

def clear_errors(parent):
	parent.errors_pte.clear()
	parent.statusbar.clearMessage()

def clear_info(parent):
	parent.info_pte.clear()

def update_mdi(parent):
	if 'mdi_history_lw' in parent.children:
		parent.mdi_history_lw.addItem(parent.mdi_command)
		path = os.path.dirname(parent.status.ini_filename)
		mdi_file = os.path.join(path, 'mdi_history.txt')
		mdi_codes = []
		for index in range(parent.mdi_history_lw.count()):
			mdi_codes.append(parent.mdi_history_lw.item(index).text())
		with open(mdi_file, 'w') as f:
			f.write('\n'.join(mdi_codes))
		parent.mdi_command_le.setText('')
		parent.command.mode(emc.MODE_MANUAL)
		parent.command.wait_complete()
		parent.mdi_command = ''

def print_states(parent, state):
	parent.print_states = parent.print_states_cb.isChecked()

def feed_override(parent, value):
	parent.command.feedrate(float(value / 100))

def rapid_override(parent, value):
	parent.command.rapidrate(float(value / 100))

def spindle_override(parent, value):
	parent.command.spindleoverride(float(value / 100), 0)

def update_qcode_pte(parent):
	extraSelections = []
	if not parent.gcode_pte.isReadOnly():
		selection = QTextEdit.ExtraSelection()
		lineColor = QColor('yellow').lighter(160)
		selection.format.setBackground(lineColor)
		selection.format.setForeground(QColor('black'))
		selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
		selection.cursor = parent.gcode_pte.textCursor()
		selection.cursor.clearSelection()
		extraSelections.append(selection)
	parent.gcode_pte.setExtraSelections(extraSelections)
	if 'start_line_lb' in parent.children:
		cursor = parent.gcode_pte.textCursor()
		selected_block = cursor.blockNumber() # get current block number
		parent.start_line_lb.setText(f'{selected_block}')

def read_dir(parent):
	if os.path.isdir(parent.gcode_dir):
		file_list = []
		# get directories
		for item in sorted(os.listdir(parent.gcode_dir)):
			path = os.path.join(parent.gcode_dir, item)
			if os.path.isdir(path):
				file_list.append(f'{item} ...')
		# get gcode files
		for item in sorted(os.listdir(parent.gcode_dir)):
			if os.path.splitext(item)[1].lower() in parent.extensions:
				file_list.append(item)
		parent.file_lw.clear()
		parent.file_lw.addItem('Parent Directory')
		parent.file_lw.addItems(file_list)
		parent.file_lw.setMinimumWidth(parent.file_lw.sizeHintForColumn(0)+60)

def sync_checkboxes(parent, sender, receiver):
	parent.settings.setValue(f'PLOT/{sender}',getattr(parent, sender).isChecked())
	if receiver in parent.children:
		getattr(parent, receiver).setChecked(getattr(parent, sender).isChecked())
		parent.settings.setValue(f'PLOT/{receiver}', getattr(parent, sender).isChecked())

def update_hal_spinbox(parent, value):
	setattr(parent.halcomp, parent.sender().property('pin_name'), value)

	#parent.halcomp.pin_seek = 123.5


