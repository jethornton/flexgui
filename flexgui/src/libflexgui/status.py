from math import sqrt

from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor, QAction

import linuxcnc as emc

from libflexgui import utilities

'''
STATE_ESTOP
STATE_ESTOP_RESET
STATE_ON Not Homed No Program
STATE_ON All Homed No Program
STATE_ON Not Homed Program Loaded
STATE_ON All Homed Program Loaded
MODE_AUTO INTERP_WAITING
MODE_AUTO INTERP_PAUSED
MODE_MDI INTERP_READING
MODE_MDI INTERP_IDLE
'''

TASK_STATES = {1: 'STATE_ESTOP', 2: 'STATE_ESTOP_RESET', 3: 'STATE_OFF',
	4: 'STATE_ON'}
TASK_MODES = {1: 'MODE_MANUAL', 2: 'MODE_AUTO', 3: 'MODE_MDI'}
INTERP_STATES = {1: 'INTERP_IDLE', 2: 'INTERP_READING', 3: 'INTERP_PAUSED',
	4: 'INTERP_WAITING'}
EXEC_STATES = {1: 'EXEC_ERROR', 2: 'EXEC_DONE', 3: 'EXEC_WAITING_FOR_MOTION',
	4: 'EXEC_WAITING_FOR_MOTION_QUEUE', 5: 'EXEC_WAITING_FOR_IO',
	7: 'EXEC_WAITING_FOR_MOTION_AND_IO)', 8: 'EXEC_WAITING_FOR_DELAY',
	9: 'EXEC_WAITING_FOR_SYSTEM_CMD', 10: 'EXEC_WAITING_FOR_SPINDLE_ORIENTED', }
MOTION_MODES = {1: 'TRAJ_MODE_FREE', 2: 'TRAJ_MODE_COORD', 3: 'TRAJ_MODE_TELEOP'}
STATES = {1: 'RCS_DONE', 2: 'RCS_EXEC', 3: 'RCS_ERROR'}

def update(parent):
	parent.status.poll()

	# **************************
	# motion_mode TRAJ_MODE_COORD, TRAJ_MODE_FREE, TRAJ_MODE_TELEOP
	if parent.motion_mode != parent.status.motion_mode:
		# when all joints are homed motion_mode changes
		# from TRAJ_MODE_FREE to TRAJ_MODE_TELEOP
		if parent.status.motion_mode == emc.TRAJ_MODE_TELEOP:
			if utilities.all_homed(parent):
				utilities.set_homed_enable(parent)

		parent.motion_mode = parent.status.motion_mode


	# **************************
	# task_state STATE_ESTOP, STATE_ESTOP_RESET, STATE_ON, STATE_OFF
	if parent.task_state != parent.status.task_state:
		#print(f'task state {TASK_STATES[parent.status.task_state]}')

		# e stop open
		if parent.status.task_state == emc.STATE_ESTOP:
			#print('status update STATE_ESTOP')
			for key, value in parent.state_estop.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_estop_names.items():
				getattr(parent, key).setText(value)

		# e stop closed power off
		if parent.status.task_state == emc.STATE_ESTOP_RESET:
			#print('status update STATE_ESTOP_RESET')
			for key, value in parent.state_estop_reset.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_estop_reset_names.items():
				getattr(parent, key).setText(value)

		# e stop closed power on
		if parent.status.task_state == emc.STATE_ON:
			#print('status update STATE_ON')
			for key, value in parent.state_on.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_on_names.items():
				getattr(parent, key).setText(value)

			if utilities.all_homed(parent):
				#print('status update ALL HOMED')
				for item in parent.unhome_controls:
					getattr(parent, item).setEnabled(True)
				for item in parent.home_controls:
					getattr(parent, item).setEnabled(False)
			else:
				#print('status update NOT HOMED')
				for item in parent.home_controls:
					getattr(parent, item).setEnabled(True)
				for item in parent.unhome_controls:
					getattr(parent, item).setEnabled(False)

			if parent.status.file:
				#print('status update FILE LOADED')
				for item in parent.file_edit_items:
					getattr(parent, item).setEnabled(True)
				if utilities.all_homed(parent):
					#print('status update FILE LOADED and ALL HOMED')
					for item in parent.run_controls:
						getattr(parent, item).setEnabled(True)

			else:
				#print('status update NO FILE LOADED')
				for item in parent.file_edit_items:
					getattr(parent, item).setEnabled(False)

		parent.task_state = parent.status.task_state

	# **************************
	# interp_state INTERP_IDLE, INTERP_READING, INTERP_PAUSED, INTERP_WAITING
	if parent.interp_state != parent.status.interp_state:
		#print(f'interp state {INTERP_STATES[parent.status.interp_state]}')

		if parent.status.interp_state == emc.INTERP_IDLE:
			if parent.status.task_mode == emc.MODE_AUTO: # program has finished
				parent.command.mode(emc.MODE_MANUAL)
				parent.command.wait_complete()
				#parent.status.poll()
				#print(f'{TASK_MODES[parent.status.task_mode]}')

			#if parent.status.task_mode == emc.MODE_MANUAL:
			#	# program is not running
			#	print('status update INTERP_IDLE MODE_MANUAL')

			if parent.status.task_mode == emc.MODE_MDI: # mdi is done
				if parent.mdi_command: # only update mdi if it's configured
					utilities.update_mdi(parent)
				else:
					parent.command.mode(emc.MODE_MANUAL)
					parent.command.wait_complete()
				#print('status update INTERP_IDLE MODE_MANUAL')

		if parent.status.task_mode == emc.MODE_AUTO:
			# program is running
			if parent.status.interp_state == emc.INTERP_WAITING:
				#print('INTERP_WAITING MODE_AUTO')
				if parent.status.exec_state != emc.EXEC_WAITING_FOR_IO:
					for key, value in parent.program_running.items():
						getattr(parent, key).setEnabled(value)

			# program is paused
			if parent.status.interp_state == emc.INTERP_PAUSED:
				#print('INTERP_PAUSED MODE_AUTO')
				for key, value in parent.program_paused.items():
					getattr(parent, key).setEnabled(value)

		if parent.status.interp_state == emc.INTERP_READING:
			#print('INTERP_READING')
			if parent.status.task_mode == emc.MODE_AUTO:
				for key, value in parent.program_running.items():
					getattr(parent, key).setEnabled(value)
			#if parent.status.task_mode == emc.MODE_MDI:
				# mdi is running
				#print('status update MODE_MDI')
		parent.interp_state = parent.status.interp_state

	# **************************
	# task_mode MODE_MDI, MODE_AUTO, MODE_MANUAL
	if parent.task_mode != parent.status.task_mode:
		#print(f'{TASK_MODES[parent.status.task_mode]}')
		# catch MDI commands that don't change the interp state like M53
		if parent.status.task_mode == emc.MODE_MDI:
			if parent.status.interp_state == emc.INTERP_IDLE:
				#print(f'{parent.mdi_command}')
				if parent.mdi_command:
					utilities.update_mdi(parent)
		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode == emc.MODE_MANUAL:
				if parent.status.interp_state == emc.INTERP_IDLE:
					for key, value in parent.state_on.items():
						getattr(parent, key).setEnabled(value)
					for item in parent.run_controls:
						getattr(parent, item).setEnabled(True)
					for item in parent.unhome_controls:
						getattr(parent, item).setEnabled(True)
		parent.task_mode = parent.status.task_mode

	# **************************
	#exec_state EXEC_ERROR, EXEC_DONE, EXEC_WAITING_FOR_MOTION,
	#EXEC_WAITING_FOR_MOTION_QUEUE, EXEC_WAITING_FOR_IO,
	#EXEC_WAITING_FOR_MOTION_AND_IO, EXEC_WAITING_FOR_DELAY,
	#EXEC_WAITING_FOR_SYSTEM_CMD, EXEC_WAITING_FOR_SPINDLE_ORIENTED.
	if parent.exec_state != parent.status.exec_state:
		parent.exec_state = parent.status.exec_state

	# ************************** FLOOD_OFF or FLOOD_ON
	if parent.flood_state != parent.status.flood:
		if 'flood_pb' in parent.children: 
			if parent.status.flood == emc.FLOOD_OFF:
				parent.flood_pb.setChecked(False)
			elif parent.status.flood == emc.FLOOD_ON:
				parent.flood_pb.setChecked(True)
		parent.flood_state = parent.status.flood

	# ************************** MIST_OFF or MIST_ON
	if parent.mist_state != parent.status.mist:
		if 'mist_pb' in parent.children: 
			if parent.status.mist == emc.MIST_OFF:
				parent.mist_pb.setChecked(False)
			elif parent.status.mist == emc.MIST_ON:
				parent.mist_pb.setChecked(True)
		parent.mist_state = parent.status.mist

	# key is label and value is status item
	for key, value in parent.status_labels.items(): # update all status labels
		if value in parent.stat_dict:
			stat_value = getattr(parent.status, f'{value}')
			if stat_value in parent.stat_dict[value]:
				getattr(parent, f'{key}').setText(f'{parent.stat_dict[value][stat_value]}')
		else:
			getattr(parent, f'{key}').setText(f'{getattr(parent.status, f"{value}")}')

	if 'gcodes_lb' in parent.children:
		g_codes = []
		for i in parent.status.gcodes[1:]:
			if i == -1: continue
			if i % 10 == 0:
				g_codes.append(f'G{(i/10):.0f}')
			else:
				g_codes.append(f'G{(i/10):.0f}.{i%10}')
		parent.gcodes_lb.setText(f'{" ".join(g_codes)}')

	if 'mcodes_lb' in parent.children:
		m_codes = []
		for i in parent.status.mcodes[1:]:
			if i == -1: continue
			m_codes.append(f'M{i}')
		parent.mcodes_lb.setText(f'{" ".join(m_codes)}')

	# update gcode_pte
	if 'gcode_pte' in parent.children:
		n = parent.status.motion_line
		if n != parent.last_line:
			format_normal = QTextBlockFormat()
			format_normal.setBackground(QColor('white'))
			highlight_format = QTextBlockFormat()
			highlight_format.setBackground(QColor('yellow'))
			motion_line = parent.status.motion_line
			cursor = parent.gcode_pte.textCursor()
			cursor.select(QTextCursor.SelectionType.Document)
			cursor.setBlockFormat(format_normal)
			cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(motion_line))
			cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor)
			cursor.setBlockFormat(highlight_format)
			parent.gcode_pte.setTextCursor(cursor)
			parent.last_line = n

	# homed status
	for item in parent.home_status:
		if parent.status.homed[int(item[-1])]:
			getattr(parent, item).setText('*')
		else:
			getattr(parent, item).setText('')

	# axis position no offsets
	for key, value in parent.status_position.items(): # key is label value precision
		machine_position = getattr(parent, "status").position[value[0]]
		getattr(parent, f'{key}').setText(f'{machine_position:.{value[1]}f}')

	# axis position including offsets
	for key, value in parent.status_dro.items(): # key is label value tuple position & precision
		g5x_offset = getattr(parent, "status").g5x_offset[value[0]]
		g92_offset = getattr(parent, "status").g92_offset[value[0]]
		machine_position = getattr(parent, "status").position[value[0]]
		relative_position = machine_position - (g5x_offset + g92_offset)
		getattr(parent, f'{key}').setText(f'{relative_position:.{value[1]}f}')

	# axis g5x offset
	for key, value in parent.status_g5x.items(): # key is label value tuple position & precision
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").g5x_offset[value[0]]:.{value[1]}f}')

	# axis g92 offset
	for key, value in parent.status_g92.items(): # key is label value tuple position & precision
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").g92_offset[value[0]]:.{value[1]}f}')

	# axis s.axis[0]['velocity'] parent.status.axis[0]['velocity']
	for key, value in parent.status_axes.items():
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").axis[value[0]][value[1]]:.{value[2]}f}')

	# joint velocity parent.status.joint[0]['velocity'] key label value joint precision
	for key, value in parent.joint_vel_sec.items():
		getattr(parent, key).setText(f'{abs(getattr(parent, "status").joint[value[0]]["velocity"]):.{value[1]}f}')
	for key, value in parent.joint_vel_min.items():
		getattr(parent, key).setText(f'{abs(getattr(parent, "status").joint[value[0]]["velocity"]) * 60:.{value[1]}f}')

	# two joint velocity
	for key, value in parent.two_vel.items():
		vel_0 = getattr(parent, 'status').joint[value[0]]['velocity']
		vel_1 = getattr(parent, 'status').joint[value[1]]['velocity']
		vel = sqrt((vel_0 * vel_0) + (vel_1 * vel_1))
		getattr(parent, key).setText(f'{vel * 60:.{value[2]}f}')

	# three joint velocity
	for key, value in parent.three_vel.items():
		vel_0 = getattr(parent, 'status').joint[value[0]]['velocity']
		vel_1 = getattr(parent, 'status').joint[value[1]]['velocity']
		vel_2 = getattr(parent, 'status').joint[value[2]]['velocity']
		vel = sqrt((vel_0 * vel_0) + (vel_1 * vel_1) + (vel_2 * vel_2))
		getattr(parent, key).setText(f'{vel * 60:.{value[3]}f}')

	# override items label : status item
	for label, stat in parent.overrides.items():
		getattr(parent, label).setText(f'{getattr(parent.status, f"{stat}") * 100:.0f}%')

	# dio din_0_lb din[0] dout_0_lb dout[0]
	for key, value in parent.status_dio.items():
		state = getattr(parent.status, f"{value[0]}")[value[1]]
		item = f'{value[0]}[{value[1]}]'
		getattr(parent, f'{key}').setText(f'{parent.stat_dict[item][state]}')

	# aio ain_0_lb aout_0_lb aio[0] aout[0]
	for key, value in parent.status_aio.items():
		getattr(parent, f'{key}').setText(f'{getattr(parent.status, f"{value[0]}")[value[1]]:.{value[2]}f}')

	# spindle s.spindle[0]['brake']
	for key, value in parent.status_spindles.items():
		getattr(parent, key).setText(f'{getattr(parent, "status").spindle[0][value]}')

	for key, value in parent.status_spindle_speed.items():
		getattr(parent, key).setText(f'{abs(getattr(parent, "status").spindle[0][value])}')

	# spindle lcd
	for key, value in parent.status_spindle_lcd.items():
		getattr(parent, key).display(f'{getattr(parent, "status").spindle[0][value]}')

	# spindle override parent.spindle[0]['override']
	for key, value in parent.status_spindle_overrides.items():
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").spindle[value]["override"] * 100:.0f}%')

	# spindle direction
	for key, value in parent.status_spindle_dir.items():
		if parent.status.spindle[0]['speed'] > 0:
			direction = 'Fwd'
		elif parent.status.spindle[0]['speed'] < 0:
			direction = 'Rev'
		elif parent.status.spindle[0]['speed'] == 0:
			direction = 'Off'
		getattr(parent, f'{key}').setText(direction)

	# spindle actual speed
	for item in parent.spindle_actual_speed:
		override = parent.spindle_override_sl.value() / 100
		commanded_rpm = abs(parent.status.spindle[0]['speed'])
		override_rpm = commanded_rpm * override
		if override_rpm >= parent.min_rpm:
			getattr(parent, item).setText(f'{override_rpm:.1f}')
		elif override_rpm > 0:
			getattr(parent, item).setText(f'{parent.min_rpm:.1f}')
		else:
			getattr(parent, item).setText('0.0')

	# current tool information
	for key, value in parent.current_tool.items():
		tr = parent.status.tool_table[0]
		getattr(parent, key).setText(f'{getattr(tr, value)}')
	# handle errors
	#if parent.status.state == parent.emc.RCS_ERROR:
	if 'errors_pte' in parent.children:
		error = parent.error.poll()
		if error:
			kind, text = error
			if kind in (emc.NML_ERROR, emc.OPERATOR_ERROR):
				error_type = 'Error'
			else:
				error_type = 'Info'
			parent.errors_pte.appendPlainText(error_type)
			parent.errors_pte.appendPlainText(text)
			parent.errors_pte.setFocus()
			parent.statusbar.showMessage('Error')

