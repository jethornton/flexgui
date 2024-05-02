import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor

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
	'''
	num_joints = parent.status.joints
	home_status = parent.status.homed[:num_joints]
	test_list = []
	for i in range(num_joints):
		test_list.append(1)
	test_tuple = tuple(test_list)
	return home_status == test_tuple
	'''
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

def update_jog_lb(parent):
	parent.jog_vel_lb.setText(f'{parent.jog_vel_sl.value()} {parent.units}/min')

def add_mdi(parent):
	parent.mdi_command_le.setText(f'{parent.mdi_history_lw.currentItem().text()}')

def clear_errors(parent):
	parent.errors_pte.clear()
	parent.statusbar.clearMessage()

def update_mdi(parent):
	if parent.mdi_history:
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

def print_states(parent, state):
	parent.print_states = parent.print_states_cb.isChecked()

def feed_override(parent, value):
	# feedrate(float) set the feedrate override, 1.0 = 100%.
	parent.command.feedrate(float(value / 100))
	parent.command.wait_complete()

def rapid_override(parent, value):
	parent.command.rapidrate(float(value / 100))
	parent.command.wait_complete()

def spindle_override(parent, value):
	parent.command.spindleoverride(float(value / 100), 0)
	parent.command.wait_complete()

def update_qcode_pte(parent):
	cursor = parent.gcode_pte.textCursor()
	selected_block = cursor.blockNumber() # get current block number
	#print(f'Current line number: {selected_block}')
	format_normal = QTextBlockFormat()
	format_normal.setBackground(QColor('white'))
	cursor.select(QTextCursor.SelectionType.Document)
	cursor.setBlockFormat(format_normal)
	cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(selected_block))
	highlight_format = QTextBlockFormat()
	highlight_format.setBackground(QColor('yellow'))
	cursor.setBlockFormat(highlight_format)



