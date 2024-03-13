
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton

import linuxcnc as emc

from libflexgui import dialogs
from libflexgui import utilities

def all_homed(parent):
	parent.status.poll()
	# parent.status.homed returns a tuple of all joints home status 1 is homed
	homed = parent.status.homed
	# parent.status.axis_mask.bit_count() returns the number of axes configured
	for i in range(parent.status.axis_mask.bit_count()):
		if homed[i] == 1:
			all_homed = True
		else:
			all_homed = False
	return all_homed
'''
def estop_toggle(parent):
	parent.status.poll()
	if parent.status.task_state == emc.STATE_ESTOP:
		parent.command.state(emc.STATE_ESTOP_RESET)
		parent.command.wait_complete()
	else:
		parent.command.state(emc.STATE_ESTOP)
		parent.command.wait_complete()

def power_toggle(parent):
	parent.status.poll()
	if parent.status.file:
		file_loaded = True
	else:
		file_loaded = False

	if parent.status.task_state == emc.STATE_ESTOP_RESET:
		parent.command.state(emc.STATE_ON)
		parent.command.wait_complete()
		state = True
	else:
		parent.command.state(emc.STATE_OFF)
		parent.command.wait_complete()
		state = False
	for item in parent.power_enables:
		getattr(parent, item).setEnabled(state)
	for item in parent.home_enables:
		getattr(parent, item).setEnabled(state)
	for item in parent.run_enables:
		getattr(parent, item).setEnabled(file_loaded)
	if parent.home_all_ok:
		parent.home_all_pb.setEnabled(state)

def run(parent):
	parent.status.poll()
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_AUTO:
			parent.command.mode(emc.MODE_AUTO)
			parent.command.wait_complete()
		if parent.findChild(QLabel, 'start_line_lb'):
			if parent.start_line_lb.text():
				n = int(parent.start_line_lb.text())
		else:
			n = 0
		parent.command.auto(emc.AUTO_RUN, n)

def step(parent):
	parent.status.poll()
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_AUTO:
			parent.command.mode(emc.MODE_AUTO)
			parent.command.wait_complete()
		parent.command.auto(emc.AUTO_STEP)

def pause(parent):
	parent.status.poll()
	if parent.status.state == emc.RCS_EXEC: # program is running
		parent.command.auto(emc.AUTO_PAUSE)

def resume(parent):
	parent.status.poll()
	if parent.status.paused:
		parent.command.auto(emc.AUTO_RESUME)

def stop(parent):
	parent.command.abort()
'''

def set_mode_manual(parent):
	if parent.status.task_mode != emc.MODE_MANUAL:
		parent.command.mode(emc.MODE_MANUAL)
		parent.command.wait_complete()

def set_mode(parent, mode=None):
	if mode is None:
		if parent.sender().objectName() == 'manual_mode_pb':
			mode = emc.MODE_MANUAL
	if parent.status.task_mode != mode:
		parent.command.mode(mode)
		parent.command.wait_complete()

def home(parent):
	parent.status.poll()
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 0:
		if parent.status.task_mode != emc.MODE_MANUAL:
			parent.command.mode(emc.MODE_MANUAL)
			parent.command.wait_complete()
		parent.command.home(joint)
		parent.command.wait_complete()
		if parent.findChild(QPushButton, f'unhome_pb_{joint}'):
			getattr(parent, f'unhome_pb_{joint}').setEnabled(True)
		if all_homed(parent):
			if parent.findChild(QPushButton, 'run_mdi_pb'):
				parent.run_mdi_pb.setEnabled(True)
			if parent.findChild(QPushButton, 'unhome_all_pb'):
				parent.unhome_all_pb.setEnabled(True)

def home_all(parent): # only works if the home sequence is set for all axes
		set_mode(parent,emc.MODE_MANUAL)
		parent.command.teleop_enable(False)
		parent.command.wait_complete()
		parent.command.home(-1)
		parent.command.wait_complete()
		parent.status.poll()
		if all_homed(parent):
			if 'run_mdi_pb' in parent.children:
				parent.run_mdi_pb.setEnabled(True)
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(True)
			for item in parent.unhome_controls:
				getattr(parent, item).setEnabled(True)
			if parent.status.file:
				if parent.status.task_state == emc.STATE_ON:
					for item in parent.file_loaded:
						getattr(parent, item).setEnabled(True)

def unhome(parent): # FIXME turn off home required items
	parent.status.poll()
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 1:
		set_mode(parent, emc.MODE_MANUAL)
		parent.command.teleop_enable(False)
		parent.command.wait_complete()
		parent.command.unhome(joint)
		getattr(parent, f'unhome_pb_{joint}').setEnabled(False)
		for item in parent.run_controls:
			getattr(parent, item).setEnabled(False)
		if 'run_mdi_pb' in parent.children:
			parent.run_mdi_pb.setEnabled(False)
		if utilities.all_unhomed(parent):
			if 'unhome_all_pb' in parent.children:
				parent.unhome_all_pb.setEnabled(False)

def unhome_all(parent):
	set_mode(parent, emc.MODE_MANUAL)
	parent.command.teleop_enable(False)
	parent.command.wait_complete()
	parent.command.unhome(-1)
	if parent.findChild(QPushButton, 'run_mdi_pb'):
		parent.run_mdi_pb.setEnabled(False)
	for item in parent.unhome_controls:
		getattr(parent, item).setEnabled(False)
	for item in parent.run_controls:
		getattr(parent, item).setEnabled(False)

def run_mdi(parent, cmd=''):
	if cmd:
		mdi_command = cmd
	else:
		if parent.findChild(QLineEdit, 'mdi_command_le'):
			if parent.mdi_command_le.text():
				mdi_command = parent.mdi_command_le.text()
			else:
				msg = 'No MDI command was found!'
				dialogs.warn_msg_ok(msg, 'Error')
		else:
			msg = 'QLineEdit mdi_command_le not found!'
			dialogs.warn_msg_ok(msg, 'Error')
			return

	parent.mdi_command = mdi_command

	if mdi_command:
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode != emc.MODE_MDI:
				parent.command.mode(emc.MODE_MDI)
				parent.command.wait_complete()
			parent.pause_pb.setEnabled(True)
			parent.command.mdi(mdi_command)
			parent.command.mode(emc.MODE_MANUAL)

def touchoff(parent):
	pass

def tool_touchoff(parent):
	pass

def tool_change(parent):
	pass

def spindle(parent):
	pb = parent.sender().objectName()
	print(pb)
	parent.spindle_speed = 100
	if pb == 'start_spindle_pb':
		run_mdi(parent, f'M3 S{parent.spindle_speed}')
	elif pb == 'stop_spindle_pb':
		run_mdi(parent, 'M5')
	elif pb == 'spindle_plus_pb':
		parent.spindle_speed_sb.setValue(parent.spindle_speed + 100) 
	elif pb == 'spindle_minus_pb':
		parent.spindle_speed_sb.setValue(parent.spindle_speed - 100) 

def flood_toggle(parent):
	parent.status.poll()
	if parent.sender().isChecked():
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode != emc.MODE_MANUAL:
				parent.command.mode(emc.MODE_MANUAL)
				parent.command.wait_complete()
			parent.command.flood(emc.FLOOD_ON)
			parent.command.wait_complete()
	else:
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode != emc.MODE_MANUAL:
				parent.command.mode(emc.MODE_MANUAL)
				parent.command.wait_complete()
			parent.command.flood(emc.FLOOD_OFF)
			parent.command.wait_complete()

def mist_toggle(parent):
	parent.status.poll()
	if parent.sender().isChecked():
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode != emc.MODE_MANUAL:
				parent.command.mode(emc.MODE_MANUAL)
				parent.command.wait_complete()
			parent.command.mist(emc.MIST_ON)
			parent.command.wait_complete()
	else:
		if parent.status.task_state == emc.STATE_ON:
			parent.command.mode(emc.MODE_MANUAL)
			parent.command.wait_complete()
		parent.command.mist(emc.MIST_OFF)
		parent.command.wait_complete()



