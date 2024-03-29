import os

from PyQt6.QtCore import Qt

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
	num_joints = parent.status.joints
	for i, h in enumerate(parent.status.homed):
		if i >= num_joints: break
		if h == 0:
			all_homed = False
			break
		elif h == 1: all_homed = True
	return all_homed

def all_unhomed(parent):
	parent.status.poll()
	num_joints = parent.status.joints
	for i,h in enumerate(parent.status.homed):
		if i >= num_joints: break
		if h == 1:
			all_unhomed = False
			break
		elif h == 0: all_unhomed = True
	return all_unhomed

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

def spindle_speed(parent):
	parent.spindle_speed = parent.spindle_speed_sb.value()

def clear_errors(parent):
	parent.errors_pte.clear()
	parent.statusbar.clearMessage()

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

def print_states(parent, state):
	parent.print_states = parent.print_states_cb.isChecked()

def feed_override(parent, value):
	# feedrate(float) set the feedrate override, 1.0 = 100%.
	parent.command.feedrate(float(value / 100))





