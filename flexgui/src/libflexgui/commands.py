
from PyQt6.QtWidgets import QLabel

import linuxcnc as emc

def abort(parent):
	parent.command.abort()

def estop_toggle(parent):
	if parent.status.task_state == emc.STATE_ESTOP:
		parent.command.state(emc.STATE_ESTOP_RESET)
		parent.command.wait_complete()
	else:
		parent.command.state(emc.STATE_ESTOP)
		parent.command.wait_complete()

def power_toggle(parent):
	if parent.status.task_state == emc.STATE_ESTOP_RESET:
		parent.command.state(emc.STATE_ON)
		parent.command.wait_complete()
	else:
		parent.command.state(emc.STATE_OFF)
		parent.command.wait_complete()

def run(parent):
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
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_AUTO:
			parent.command.mode(emc.MODE_AUTO)
			parent.command.wait_complete()
		parent.command.auto(emc.AUTO_STEP)

def pause(parent):
	if parent.status.state == emc.RCS_EXEC: # program is running
		parent.command.auto(emc.AUTO_PAUSE)

def resume(parent):
	if parent.status.paused:
		parent.command.auto(emc.AUTO_RESUME)

def stop(parent):
	parent.command.abort()

def set_mode(parent, mode=None):
	if mode is None:
		if parent.sender().objectName() == 'manual_mode_pb':
			mode = emc.MODE_MANUAL
	if parent.status.task_mode != mode:
		parent.command.mode(mode)
		parent.command.wait_complete()

def home(parent):
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 0:
		if parent.status.task_mode != emc.MODE_MANUAL:
			parent.command.mode(emc.MODE_MANUAL)
			parent.command.wait_complete()
		#if parent.status.motion_mode != emc.TRAJ_MODE_FREE:
		#	parent.command.traj_mode(emc.TRAJ_MODE_FREE)
		parent.command.home(joint)
		parent.command.wait_complete()
		#parent.sender().setStyleSheet('background-color: rgba(0, 255, 0, 25%);')
		#getattr(parent, f'unhome_pb_{joint}').setEnabled(True)
		#parent.unhome_all_pb.setEnabled(True)

	# homed (returns tuple of integers) - currently homed joints, 0 = not homed, 1 = homed.
	#parent.status.poll()
	#print(f'Homed: {parent.status.homed}')
	# home(int) home a given joint.

def home_all(parent): # only works if the home sequence is set for all axes
		set_mode(parent,emc.MODE_MANUAL)
		parent.command.teleop_enable(False)
		parent.command.wait_complete()
		parent.command.home(-1)
		#for i in range(parent.joints):
		#	getattr(parent, f'home_pb_{i}').setStyleSheet('background-color: rgba(0, 255, 0, 25%);')
		#	getattr(parent, f'unhome_pb_{i}').setEnabled(True)
		#parent.unhome_all_pb.setEnabled(True)

def unhome(parent):
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 1:
		set_mode(parent, emc.MODE_MANUAL)
		parent.command.teleop_enable(False)
		parent.command.wait_complete()
		parent.command.unhome(joint)
		#getattr(parent, f'home_pb_{joint}').setStyleSheet('background-color: ;')
		#getattr(parent, f'unhome_pb_{joint}').setEnabled(False)

def unhome_all(parent):
		set_mode(parent, emc.MODE_MANUAL)
		parent.command.teleop_enable(False)
		parent.command.wait_complete()
		parent.command.unhome(-1)
		#for i in range(parent.joints):
		#	getattr(parent, f'home_pb_{i}').setStyleSheet('background-color: ;')
		#	getattr(parent, f'unhome_pb_{i}').setEnabled(False)
		#parent.unhome_all_pb.setEnabled(False)

def run_mdi(parent):
	pass

def touchoff(parent):
	pass

def tool_touchoff(parent):
	pass

def tool_change(parent):
	pass

def spindle(parent):
	pass

def flood_toggle(parent):
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



