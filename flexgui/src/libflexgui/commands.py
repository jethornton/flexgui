import threading

import linuxcnc as emc

from libflexgui import dialogs
from libflexgui import utilities

def home(parent):
	#print('home')
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 0: # joint not homed
		parent.command.home(joint)

def home_all(parent):
	#print('home_all')
	parent.command.home(-1)

def unhome(parent):
	#print('unhome')
	joint = int(parent.sender().objectName()[-1])
	if parent.status.homed[joint] == 1: # joint is homed
		if parent.status.motion_mode != emc.TRAJ_MODE_FREE:
			parent.command.teleop_enable(False)
			parent.command.wait_complete()
		parent.command.unhome(joint)

def unhome_all(parent):
	#print('unhome_all')
	if parent.status.motion_mode != emc.TRAJ_MODE_FREE:
		parent.command.teleop_enable(False)
		parent.command.wait_complete()
	parent.command.unhome(-1)

def run_mdi(parent, cmd=''):
	if cmd:
		mdi_command = cmd
	else:
		if 'mdi_command_le' in parent.child_names:
			mdi_command = parent.mdi_command_le.text()
	if mdi_command:
		parent.mdi_command = mdi_command
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode == emc.MODE_MANUAL:
				parent.command.mode(emc.MODE_MDI)
				parent.command.wait_complete()
				parent.command.mdi(mdi_command)
	else:
		msg = 'No MDI command was found!'
		dialogs.warn_msg_ok(parent, msg, 'Error')

def add_mdi(parent): # when you click on the mdi history list widget
	parent.mdi_command_le.setText(f'{parent.mdi_history_lw.currentItem().text()}')

def mdi_button(parent):
	mdi_command = parent.sender().property('command')
	parent.status.poll()
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode == emc.MODE_MANUAL:
			parent.command.mode(emc.MODE_MDI)
			parent.command.wait_complete()
			parent.command.mdi(mdi_command)

def jog_check(parent):
	if 'jog_vel_sl' in parent.child_names:
		if parent.jog_vel_sl.value() > 0.0:
			return True
		else:
			msg = ('Can not jog at Zero Velocity!')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			return False
	else:
		msg = ('Can not jog without a\njog velocity slider.')
		dialogs.warn_msg_ok(msg, 'Error')
		return False

def set_jog_override(parent):
	if 'override_limits_cb' in parent.child_names:
		parent.override_limits_cb.setChecked(False)
		parent.override_limits_cb.setEnabled(False)

def jog(parent): # only do jog check if button is down
	jog_command = parent.sender().objectName().split('_')
	joint = int(jog_command[-1])
	increment = parent.jog_modes_cb.currentData()
	joint_jog_mode = True if parent.motion_mode == emc.TRAJ_MODE_FREE else False
	vel = parent.jog_vel_sl.value() / 60
	if 'minus' in jog_command:
		vel = -vel
	if parent.sender().isDown():
		if jog_check(parent):
			if increment:
				parent.command.jog(emc.JOG_INCREMENT, joint_jog_mode, joint, vel, increment)
			else:
				parent.command.jog(emc.JOG_CONTINUOUS, joint_jog_mode, joint, vel)
	else:
		parent.command.jog(emc.JOG_STOP, joint_jog_mode, joint)
		set_jog_override(parent)

def jog_selected(parent):
	joint = int(parent.axes_group.checkedButton().objectName().split('_')[-1])
	direction = parent.sender().objectName().split('_')[-1]
	vel = parent.jog_vel_sl.value() / 60
	if direction == 'minus':
		vel = -vel
	increment = parent.jog_modes_cb.currentData()
	joint_jog_mode = True if parent.motion_mode == emc.TRAJ_MODE_FREE else False

	if parent.sender().isDown():
		if jog_check(parent):
			if increment:
				parent.command.jog(emc.JOG_INCREMENT, joint_jog_mode, joint, vel, increment)
			else:
				parent.command.jog(emc.JOG_CONTINUOUS, joint_jog_mode, joint, vel)
	else:
		parent.command.jog(emc.JOG_STOP, joint_jog_mode, joint)
		set_jog_override(parent)

def keyboard_jog(parent, action, axis=None, direction=None):
	vel = parent.jog_vel_sl.value() / 60
	increment = parent.jog_modes_cb.currentData()
	if direction == 'neg':
		vel = -vel
	joint_jog_mode = True if parent.motion_mode == emc.TRAJ_MODE_FREE else False

	if parent.status.task_mode == emc.MODE_MANUAL and action:
		if jog_check(parent):
			if increment:
				parent.command.jog(emc.JOG_INCREMENT, joint_jog_mode, axis, vel, increment)
			else:
				parent.command.jog(emc.JOG_CONTINUOUS, joint_jog_mode, axis, vel)
	elif axis == None: # stop all jogging
		for i in range(parent.status.joints):
			parent.command.jog(emc.JOG_STOP, joint_jog_mode, i)
	else:
		parent.command.jog(emc.JOG_STOP, joint_jog_mode, axis)
		set_jog_override(parent)

def change_cs(parent):
	cs = parent.sender().objectName()[-1]
	cd_dict = {'1': 'G54', '2': 'G55', '3': 'G56', '4': 'G57', '5': 'G58',
		'6': 'G59', '7': 'G59.1', '8': 'G59.2', '9': 'G59.3', }
	mdi_command = cd_dict[cs]
	parent.status.poll()
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_MDI:
			parent.command.mode(emc.MODE_MDI)
			parent.command.wait_complete()
		parent.command.mdi(mdi_command)
		parent.command.wait_complete()

def clear_axis_offset(parent, axis):
	mdi_command = f'G10 L2 P0 {axis}0'
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_MDI:
			parent.command.mode(emc.MODE_MDI)
			parent.command.wait_complete()
		parent.command.mdi(mdi_command)
		parent.command.wait_complete()

def clear_cs(parent):
	cs = parent.sender().objectName().split("_")[-1]
	axes = ''
	for axis in parent.axis_letters:
		axes += f'{axis}0 '
	if int(cs) < 10:
		cmd = f'G10 L2 P{cs} {axes}'
	elif int(cs) == 10:
		cmd = 'G92.1'
	elif int(cs) == 11:
		cmd = 'G10 L2 P0 R0'
	run_mdi(parent, cmd)

def tool_change(parent): # Tool Change Buttons
	parent.status.poll()
	tool_len = len(parent.status.tool_table)
	tools = [0]
	for i in range(1, tool_len):
		tools.append(parent.status.tool_table[i][0])
	if parent.sender().objectName().split('_')[-1].isdigit(): # tool button
		parent.new_tool_number = int(parent.sender().objectName().split('_')[-1])
		parent.tool_button = True
		if 'tool_change_cb' in parent.child_names:
			if parent.new_tool_number in tools:
				parent.tool_change_cb.setCurrentIndex(parent.tool_change_cb.findData(parent.new_tool_number))
	else: # using tool change cb
		parent.new_tool_number = parent.tool_change_cb.currentData()
	if parent.new_tool_number not in tools:
		msg = (f'Tool {parent.new_tool_number} is not in the Tool Table.')
		dialogs.warn_msg_ok(parent, msg, 'Tool Change Aborted')
		return

	if parent.new_tool_number != parent.status.tool_in_spindle:
		mdi_command = f'M6 T{parent.new_tool_number}'
		if parent.status.task_mode != emc.MODE_MDI:
			parent.command.mode(emc.MODE_MDI)
			parent.command.wait_complete()
		parent.command.mdi(mdi_command)
	else:
		msg = (f'Tool {parent.new_tool_number} is already in the Spindle.')
		dialogs.warn_msg_ok(parent, msg, 'Tool Change Aborted')

def touchoff(parent):
	#print('touchoff')
	if 'touchoff_system_cb' in parent.child_names:
		coordinate_system = parent.touchoff_system_cb.currentData()
	else:
		coordinate_system = 0
	axis = parent.sender().objectName()[-1].upper()
	btn = parent.sender()

	if btn.property('source') is not None:
		source = btn.property('source')
		offset = getattr(parent, source).text()
	elif 'touchoff_le' in parent.child_names:
		offset = parent.touchoff_le.text()

	mdi_command = f'G10 L20 P{coordinate_system} {axis}{offset}'
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_MDI:
			parent.command.mode(emc.MODE_MDI)
			parent.command.wait_complete()
		parent.command.mdi(mdi_command)
		parent.command.wait_complete()

def tool_touchoff(parent):
	#print('tool_touchoff')
	parent.status.poll()
	axis = parent.sender().objectName()[-1].upper()
	cur_tool = parent.status.tool_in_spindle
	btn = parent.sender()

	if btn.property('source') is not None:
		source = btn.property('source')
		offset = getattr(parent, source).text()
	elif 'tool_touchoff_le' in parent.child_names:
		offset = parent.tool_touchoff_le.text()

	if offset == '':
		msg = ('Tool Touchoff Offset\ncan not be blank!')
		dialogs.warn_msg_ok(parent, msg, 'Error')
		return

	if cur_tool > 0:
		mdi_command = f'G10 L10 P{cur_tool} {axis}{offset} G43'
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode != emc.MODE_MDI:
				parent.command.mode(emc.MODE_MDI)
				parent.command.wait_complete()
			parent.command.mdi(mdi_command)
			parent.command.wait_complete()
	else:
		msg = ('No Tool in Spindle.')
		dialogs.warn_msg_ok(parent, msg, 'Touch Off Aborted')

def spindle_control(parent, spindle, action): # Fwd Rev Off Plus Minus
	#print(f'spindle {spindle}')
	match action:
		case 'fwd':
			#print(f'Spindle:{spindle} Action:{action}')
			rpm = getattr(parent, f'spindle_rpm_{spindle}')
			parent.command.spindle(emc.SPINDLE_FORWARD, float(rpm), spindle)

		case 'rev':
			#print(f'Spindle:{spindle} Action:{action}')
			rpm = getattr(parent, f'spindle_rpm_{spindle}')
			parent.command.spindle(emc.SPINDLE_REVERSE, float(rpm), spindle)

		case 'stop':
			#print(f'Spindle:{spindle} Action:{action}')
			parent.command.spindle(emc.SPINDLE_OFF, spindle)

		case 'plus':
			#print(f'Spindle:{spindle} Action:{action}')
			current = getattr(parent, f'spindle_rpm_{spindle}')
			#print(f'current {current}')
			increment = getattr(parent, f'spindle_{spindle}_rpm_increment')
			max_rpm =  getattr(parent, f'spindle_{spindle}_max_fwd_rpm')
			new_rpm = current + increment
			if new_rpm > max_rpm:
				new_rpm = max_rpm
			setattr(parent, f'spindle_rpm_{spindle}', new_rpm)
			if parent.status.spindle[spindle]['direction'] == 1:
				parent.command.spindle(emc.SPINDLE_FORWARD, float(new_rpm), spindle)
			elif parent.status.spindle[spindle]['direction'] == -1:
				parent.command.spindle(emc.SPINDLE_REVERSE, float(new_rpm), spindle)
			if f'spindle_speed_{spindle}_sb' in parent.child_names:
				getattr(parent, f'spindle_speed_{spindle}_sb').setValue(new_rpm)

		case 'minus':
			#print(f'Spindle:{spindle} Action:{action}')
			current = getattr(parent, f'spindle_rpm_{spindle}')
			increment = getattr(parent, f'spindle_{spindle}_rpm_increment')
			min_rpm =  getattr(parent, f'spindle_{spindle}_min_fwd_rpm')
			new_rpm = current - increment
			if new_rpm < min_rpm:
				new_rpm = min_rpm
			setattr(parent, f'spindle_rpm_{spindle}', new_rpm)
			if parent.status.spindle[spindle]['direction'] == 1:
				parent.command.spindle(emc.SPINDLE_FORWARD, float(new_rpm), spindle)
			elif parent.status.spindle[spindle]['direction'] == -1:
				parent.command.spindle(emc.SPINDLE_REVERSE, float(new_rpm), spindle)
			if f'spindle_speed_{spindle}_sb' in parent.child_names:
				getattr(parent, f'spindle_speed_{spindle}_sb').setValue(new_rpm)

		case 'speed':
			#print(f'Spindle:{spindle} Action:{action}')
			new_rpm = getattr(parent, f'spindle_speed_{spindle}_sb').value()
			setattr(parent, f'spindle_rpm_{spindle}', new_rpm)
			if parent.status.spindle[spindle]['direction'] == 1:
				parent.command.spindle(emc.SPINDLE_FORWARD, float(new_rpm), spindle)
			elif parent.status.spindle[spindle]['direction'] == -1:
				parent.command.spindle(emc.SPINDLE_REVERSE, float(new_rpm), spindle)

def spindle(parent, value): # value is passed by the spinbox and push button
	#print(f'value {value}')

	'''
	spindle(direction: int, speed: float=0, spindle: int=0, wait_for_speed: int=0)
	Direction: [SPINDLE_FORWARD, SPINDLE_REVERSE, SPINDLE_OFF, SPINDLE_INCREASE,
	SPINDLE_DECREASE, or SPINDLE_CONSTANT]
	'''

	sender_name = parent.sender().objectName()
	parent.status.poll()
	if sender_name == 'spindle_speed_sb':
		#parent.spindle_speed = value
		parent.spindle_rpm_0 = value
		#print(f'parent.spindle_rpm_0 {parent.spindle_rpm_0}')
		if parent.status.spindle[0]['speed'] > 0:
			parent.command.spindle(emc.SPINDLE_FORWARD, float(value))
		if parent.status.spindle[0]['speed'] < 0:
			parent.command.spindle(emc.SPINDLE_REVERSE, float(value))

	elif sender_name == 'spindle_fwd_pb':
		#print('spindle_fwd_pb')
		rpm = parent.spindle_rpm_0
		if rpm == 0:
			msg = ('Can not start spindle\n'
				'at 0 RPM')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			parent.spindle_fwd_pb.setChecked(False)
		else:
			parent.command.spindle(emc.SPINDLE_FORWARD, float(rpm))
			if hasattr(parent.spindle_fwd_pb, 'led'):
				parent.spindle_fwd_pb.led = True
			if 'spindle_rev_pb' in parent.child_names:
				parent.spindle_rev_pb.setChecked(False)
				if hasattr(parent.spindle_rev_pb, 'led'):
					parent.spindle_rev_pb.led = False

	elif sender_name == 'spindle_rev_pb':
		#print('spindle_rev_pb')
		rpm = parent.spindle_rpm_0
		if rpm == 0:
			msg = ('Can not start spindle\n'
				'at 0 RPM')
			dialogs.warn_msg_ok(parent, msg, 'Error')
			parent.spindle_rev_pb.setChecked(False)
		else:
			parent.command.spindle(emc.SPINDLE_REVERSE, float(rpm))
			if hasattr(parent.spindle_rev_pb, 'led'):
				parent.spindle_rev_pb.led = True
			if 'spindle_fwd_pb' in parent.child_names:
				parent.spindle_fwd_pb.setChecked(False)
				if hasattr(parent.spindle_fwd_pb, 'led'):
					parent.spindle_fwd_pb.led = False

	elif sender_name == 'spindle_stop_pb':
		#print('spindle_stop_pb')
		parent.command.spindle(emc.SPINDLE_OFF)
		if 'spindle_fwd_pb' in parent.child_names:
			parent.spindle_fwd_pb.setChecked(False)
			if hasattr(parent.spindle_fwd_pb, 'led'):
				parent.spindle_fwd_pb.led = False
		if 'spindle_rev_pb' in parent.child_names:
			parent.spindle_rev_pb.setChecked(False)
			if hasattr(parent.spindle_rev_pb, 'led'):
				parent.spindle_rev_pb.led = False

	elif sender_name == 'spindle_plus_pb':
		#print('spindle_plus_pb')
		rpm = parent.spindle_rpm_0
		if (rpm + parent.spindle_0_rpm_increment) <= parent.spindle_0_max_fwd_rpm:
			parent.command.spindle(emc.SPINDLE_INCREASE)
			rpm += parent.spindle_0_rpm_increment
			if 'spindle_speed_sb' in parent.child_names:
				parent.spindle_speed_sb.setValue(rpm)
			if 'spindle_speed_setting_lb' in parent.child_names:
				parent.spindle_speed_setting_lb.setText(f'{rpm}')

	elif sender_name == 'spindle_minus_pb':
		#print('spindle_minus_pb')
		rpm = parent.spindle_rpm_0
		if (rpm - parent.spindle_0_rpm_increment) >= parent.spindle_0_min_fwd_rpm: # it's ok
			parent.command.spindle(emc.SPINDLE_DECREASE)
			rpm -= parent.spindle_0_rpm_increment
			if 'spindle_speed_sb' in parent.child_names:
				parent.spindle_speed_sb.setValue(rpm)
			if 'spindle_speed_setting_lb' in parent.child_names:
				parent.spindle_speed_setting_lb.setText(f'{rpm}')
		else:
			rpm = 0
			if 'spindle_fwd_pb' in parent.child_names:
				parent.spindle_fwd_pb.setChecked(False)
			if 'spindle_rev_pb' in parent.child_names:
				parent.spindle_rev_pb.setChecked(False)
				parent.command.spindle(emc.SPINDLE_OFF)

	#if 'spindle_speed_sb' in parent.child_names:
	#	parent.spindle_speed_sb.setValue(rpm)
	#if 'spindle_speed_lb' in parent.child_names:
	#	parent.spindle_speed_lb.setText(f'{rpm}')

def flood_toggle(parent):
	parent.status.poll()
	if parent.sender().isChecked():
		if parent.status.task_state == emc.STATE_ON:
			parent.command.flood(emc.FLOOD_ON)
	else:
		if parent.status.task_state == emc.STATE_ON:
			parent.command.flood(emc.FLOOD_OFF)

def mist_toggle(parent):
	parent.status.poll()
	if parent.sender().isChecked():
		if parent.status.task_state == emc.STATE_ON:
			parent.command.mist(emc.MIST_ON)
	else:
		if parent.status.task_state == emc.STATE_ON:
			parent.command.mist(emc.MIST_OFF)

def optional_stop_toggle(parent):
	if parent.optional_stop_pb.isChecked():
		parent.command.set_optional_stop(True)
	else:
		parent.command.set_optional_stop(False)

def block_delete_toggle(parent):
	if parent.block_delete_pb.isChecked():
		parent.command.set_block_delete(True)
	else:
		parent.command.set_block_delete(False)

def feed_override_toggle(parent):
	if parent.feed_override_pb.isChecked():
		parent.command.set_feed_override(True)
	else:
		parent.command.set_feed_override(False)

def feed_override_preset(parent):
	value = int(parent.sender().objectName().split('_')[-1])
	parent.command.feedrate(float(value / 100))
	parent.command.wait_complete()
	if 'feed_override_sl' in parent.child_names:
		parent.feed_override_sl.setValue(value)

def rapid_override_preset(parent):
	value = int(parent.sender().objectName().split('_')[-1])
	parent.command.rapidrate(float(value / 100))
	parent.command.wait_complete()
	if 'rapid_override_sl' in parent.child_names:
		parent.rapid_override_sl.setValue(value)

def spindle_override_preset(parent):
	value = int(parent.sender().objectName().split('_')[-1])
	parent.command.spindleoverride(float(value / 100))
	parent.command.wait_complete()
	if 'spindle_override_sl' in parent.child_names:
		parent.spindle_override_sl.setValue(value)


