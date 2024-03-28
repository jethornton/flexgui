import os

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton

import linuxcnc as emc

from libflexgui import dialogs
from libflexgui import utilities

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

def home(parent): # FIXME if joint is homed ask to home again
	parent.status.poll()
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 0:
		if parent.status.task_mode != emc.MODE_MANUAL:
			parent.command.mode(emc.MODE_MANUAL)
			parent.command.wait_complete()
		parent.command.home(joint)
		parent.command.wait_complete()
		if f'unhome_pb_{joint}' in parent.children:
			getattr(parent, f'unhome_pb_{joint}').setEnabled(True)
		if utilities.all_homed(parent) and parent.status.file:
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(True)
		if utilities.all_homed(parent):
			if 'run_mdi_pb' in parent.children:
				parent.run_mdi_pb.setEnabled(True)
			if 'unhome_all_pb' in parent.children:
				parent.unhome_all_pb.setEnabled(True)

def home_all(parent): # FIXME if joint is homed ask to home again
		set_mode(parent,emc.MODE_MANUAL)
		parent.command.teleop_enable(False)
		parent.command.wait_complete()
		parent.command.home(-1)
		parent.command.wait_complete()
		parent.status.poll()
		if utilities.all_homed(parent):
			if 'run_mdi_pb' in parent.children:
				parent.run_mdi_pb.setEnabled(True)
			for item in parent.unhome_controls:
				getattr(parent, item).setEnabled(True)
			if parent.status.file:
				if parent.status.task_state == emc.STATE_ON:
					for item in parent.file_loaded:
						getattr(parent, item).setEnabled(True)
				for item in parent.run_controls:
					getattr(parent, item).setEnabled(True)

def unhome(parent):
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
	if 'run_mdi_pb' in parent.children:
		parent.run_mdi_pb.setEnabled(False)
	for item in parent.unhome_controls:
		getattr(parent, item).setEnabled(False)
	for item in parent.run_controls:
		getattr(parent, item).setEnabled(False)

def run_mdi(parent, cmd=''):
	if cmd:
		mdi_command = cmd
	else:
		if 'mdi_command_le' in parent.children:
			if parent.mdi_command_le.text():
				mdi_command = parent.mdi_command_le.text()
			else:
				msg = 'No MDI command was found!'
				dialogs.warn_msg_ok(msg, 'Error')
		else:
			msg = 'QLineEdit mdi_command_le not found!'
			dialogs.warn_msg_ok(msg, 'Error')
			return

	if mdi_command:
		parent.mdi_command = mdi_command
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode != emc.MODE_MDI:
				parent.command.mode(emc.MODE_MDI)
				parent.command.wait_complete()
			parent.command.mdi(mdi_command)

def set_motion_teleop(parent, value):
	# 1:teleop, 0: joint
	parent.command.teleop_enable(value)
	parent.command.wait_complete()
	parent.status.poll()

def get_jog_mode(parent):
	parent.status.poll()
	if parent.status.kinematics_type == emc.KINEMATICS_IDENTITY and utilities.all_homed(parent):
		teleop_mode = 1
		jjogmode = False
	else:
		# check motion_mode since other guis (halui) could alter it
		if parent.status.motion_mode == emc.TRAJ_MODE_FREE:
			teleop_mode = 0
			jjogmode = True
		else:
			teleop_mode = 1
			jjogmode = False
	if ((jjogmode and parent.status.motion_mode != emc.TRAJ_MODE_FREE)
		or (not jjogmode and parent.status.motion_mode != emc.TRAJ_MODE_TELEOP) ):
		set_motion_teleop(parent, teleop_mode)
	return jjogmode

def jog(parent):
	if 'jog_vel_s' in parent.children:
		vel = parent.jog_vel_s.value() / 60
	else:
		msg = ('Can not jog without a\njog velocity slider.')
		dialogs.warn_msg_ok(msg, 'Error')
		return

	jog_command = parent.sender().objectName().split('_')
	joint = int(jog_command[-1])
	increment = parent.jog_modes_cb.currentData()
	if 'minus' in jog_command:
		vel = -vel

	jjogmode = get_jog_mode(parent)
	if parent.sender().isDown():
		if increment:
			parent.command.jog(emc.JOG_INCREMENT, jjogmode, joint, vel, increment)
		else:
			parent.command.jog(emc.JOG_CONTINUOUS, jjogmode, joint, vel)

	else:
		parent.command.jog(emc.JOG_STOP, jjogmode, joint)

def touchoff(parent):
	g5x = parent.status.g5x_index
	axis = parent.sender().objectName()[-1].upper()
	value = parent.touchoff_dsb.value()
	mdi_command = f'G10 L20 P{g5x} {axis}{value}'
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_MDI:
			parent.command.mode(emc.MODE_MDI)
			parent.command.wait_complete()
		parent.command.mdi(mdi_command)
		parent.command.wait_complete()
		parent.command.mode(emc.MODE_MANUAL)
		parent.command.wait_complete()

def tool_change(parent):
	if utilities.is_int(parent.sender().objectName().split('_')[-1]):
		tool_number = int(parent.sender().objectName().split('_')[-1])
	else:
		tool_number = parent.next_tool_sb.value()
	parent.status.poll()

	if tool_number > 0: # make sure tool is in the tool table
		tool_table = parent.status.tool_table
		tool_found = False
		for i in range(len(tool_table)):
			if tool_table[i].id == tool_number:
				tool_found = True
				break
		if not tool_found:
			msg = (f'The requested tool {tool_number} was\n'
				'not found in the tool table')
			dialogs.warn_msg_ok(msg, 'Tool Change Aborted')
			return

	if tool_number != parent.status.tool_in_spindle:
		mdi_command = f'M6 T{tool_number}'
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode != emc.MODE_MDI:
				parent.command.mode(emc.MODE_MDI)
				parent.command.wait_complete()
			parent.command.mdi(mdi_command)
			parent.command.wait_complete()
			parent.command.mode(emc.MODE_MANUAL)
			parent.command.wait_complete()
	else:
		msg = (f'Tool {tool_number} is already in the Spindle.')
		dialogs.warn_msg_ok(msg, 'Tool Change Aborted')

def tool_touchoff(parent):
	parent.status.poll()
	axis = parent.sender().objectName()[0].upper()
	cur_tool = parent.status.tool_in_spindle
	offset = parent.tool_touchoff_dsb.value()
	if cur_tool > 0:
		mdi_command = f'G10 L10 P{cur_tool} {axis}{offset}'
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode != emc.MODE_MDI:
				parent.command.mode(emc.MODE_MDI)
				parent.command.wait_complete()
			parent.command.mdi(mdi_command)
			parent.command.wait_complete()
			parent.command.mode(emc.MODE_MANUAL)
			parent.command.wait_complete()
	else:
		msg = ('No Tool in Spindle.')
		dialogs.warn_msg_ok(msg, 'Touch Off Aborted')

def spindle(parent):
	# spindle(direction: int, speed: float=0, spindle: int=0, wait_for_speed: int=0)
	# Direction: [SPINDLE_FORWARD, SPINDLE_REVERSE, SPINDLE_OFF, SPINDLE_INCREASE, SPINDLE_DECREASE, or SPINDLE_CONSTANT]

	pb_name = parent.sender().objectName()
	if pb_name == 'spindle_fwd_pb':
		parent.command.spindle(emc.SPINDLE_FORWARD, float(parent.spindle_speed))
	if pb_name == 'spindle_rev_pb':
		parent.command.spindle(emc.SPINDLE_REVERSE, float(parent.spindle_speed))
	elif pb_name == 'spindle_stop_pb':
		parent.command.spindle(emc.SPINDLE_OFF)
	elif pb_name == 'spindle_plus_pb':
		parent.spindle_speed += 100
		parent.command.spindle(emc.SPINDLE_INCREASE)
	elif pb_name == 'spindle_minus_pb':
		parent.command.spindle(emc.SPINDLE_DECREASE)
		if parent.spindle_speed >= 200:
			parent.spindle_speed -= 100
	if 'spindle_speed_sb' in parent.children:
		parent.spindle_speed_sb.setValue(parent.spindle_speed) 

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



