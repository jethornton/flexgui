import math, statistics

from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor, QAction
from PyQt6.QtWidgets import QLCDNumber, QAbstractSpinBox, QCheckBox, QSlider

import linuxcnc as emc
import hal

from libflexgui import utilities
from libflexgui import dialogs

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
	7: 'EXEC_WAITING_FOR_MOTION_AND_IO', 8: 'EXEC_WAITING_FOR_DELAY',
	9: 'EXEC_WAITING_FOR_SYSTEM_CMD', 10: 'EXEC_WAITING_FOR_SPINDLE_ORIENTED', }
MOTION_MODES = {1: 'TRAJ_MODE_FREE', 2: 'TRAJ_MODE_COORD', 3: 'TRAJ_MODE_TELEOP'}
MOTION_TYPES = {0: 'MOTION_TYPE_NONE', 1: 'MOTION_TYPE_TRAVERSE',
	2: 'MOTION_TYPE_FEED', 3: 'MOTION_TYPE_ARC', 4: 'MOTION_TYPE_TOOLCHANGE',
	5: 'MOTION_TYPE_PROBING', 6: 'MOTION_TYPE_INDEXROTARY'}

STATES = {1: 'RCS_DONE', 2: 'RCS_EXEC', 3: 'RCS_ERROR'}

# Axes
X = 0
Y = 1
Z = 2
A = 3
B = 4
C = 5
U = 6
V = 7
W = 8
R = 9


def update(parent):
	parent.status.poll()

	# **** TASK STATE ****
	# task_state STATE_ESTOP, STATE_ESTOP_RESET, STATE_ON, STATE_OFF
	if parent.task_state != parent.status.task_state:
		#print(f'TASK STATE: {TASK_STATES[parent.status.task_state]}')

		# e stop open
		if parent.status.task_state == emc.STATE_ESTOP:
			#print('status update STATE_ESTOP')
			for key, value in parent.state_estop.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_estop_names.items():
				getattr(parent, key).setText(value)
			for key, value in parent.state_estop_checked.items():
				getattr(parent, key).setChecked(value)

			if 'estop_pb' in parent.child_names:
				if parent.estop_pb.isChecked():
					parent.estop_pb.blockSignals(True)
					parent.estop_pb.setChecked(False)
					parent.estop_pb.blockSignals(False)

			if parent.probe_enable_off_color: # if False just don't bother
				if 'probing_enable_pb' in parent.child_names:
					parent.probing_enable_pb.setStyleSheet(parent.probe_enable_off_color)

			# FIXME there must be a better way to show the toolbar toolbuttons
			if 'flex_E_Stop' in parent.child_names:
				parent.flex_E_Stop.setStyleSheet(parent.selected_style)
			if 'flex_Power' in parent.child_names:
				parent.flex_Power.setStyleSheet(parent.deselected_style)

			# FIXME find a better way to set leds when estop is tripped
			if 'estop_pb' in parent.child_names and hasattr(parent.estop_pb, 'led'):
				parent.estop_pb.led = False
			if 'power_pb' in parent.child_names and hasattr(parent.power_pb, 'led'):
				parent.power_pb.led = False
			if 'probing_enable_pb' in parent.child_names and hasattr(parent.probing_enable_pb, 'led'):
				parent.probing_enable_pb.led = False

		# e stop closed power off
		if parent.status.task_state == emc.STATE_ESTOP_RESET:
			#print('status update STATE_ESTOP_RESET')
			for key, value in parent.state_estop_reset.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_estop_reset_names.items():
				getattr(parent, key).setText(value)
			for key, value in parent.state_estop_reset_checked.items():
				getattr(parent, key).setChecked(value)

			if 'estop_pb' in parent.child_names:
				parent.estop_pb.blockSignals(True)
				parent.estop_pb.setChecked(True)
				parent.estop_pb.blockSignals(False)
			if 'power_pb' in parent.child_names:
				parent.power_pb.blockSignals(True)
				parent.power_pb.setChecked(False)
				parent.power_pb.blockSignals(False)

			if parent.probe_enable_off_color: # if False just don't bother
				if 'probing_enable_pb' in parent.child_names:
					parent.probing_enable_pb.setStyleSheet(parent.probe_enable_off_color)

			if 'flex_E_Stop' in parent.child_names:
				parent.flex_E_Stop.setStyleSheet(parent.deselected_style)
			if 'flex_Power' in parent.child_names:
				parent.flex_Power.setStyleSheet(parent.deselected_style)

			if 'estop_pb' in parent.child_names and hasattr(parent.estop_pb, 'led'):
				parent.estop_pb.led = True
			if 'power_pb' in parent.child_names and hasattr(parent.power_pb, 'led'):
				parent.power_pb.led = False

		# e stop closed power on
		if parent.status.task_state == emc.STATE_ON:
			#print('status update STATE_ON')
			for key, value in parent.state_on.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_on_names.items():
				getattr(parent, key).setText(value)

			if 'power_pb' in parent.child_names:
				parent.power_pb.blockSignals(True)
				parent.power_pb.setChecked(True)
				parent.power_pb.blockSignals(False)

			if 'flex_Power' in parent.child_names:
				parent.flex_Power.setStyleSheet(parent.selected_style)

			if 'power_pb' in parent.child_names and hasattr(parent.power_pb, 'led'):
				parent.power_pb.led = True
			if parent.status.task_mode == emc.MODE_MANUAL:
				if 'manual_mode_pb' in parent.child_names and hasattr(parent.manual_mode_pb, 'led'):
					parent.manual_mode_pb.led = True

			if utilities.all_homed(parent):
				#print('status update ALL HOMED')
				utilities.set_homed_enable(parent)
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

	# **** MOTION MODE ****
	# motion_mode TRAJ_MODE_COORD, TRAJ_MODE_FREE, TRAJ_MODE_TELEOP
	if parent.motion_mode != parent.status.motion_mode:
		#print(f'MOTION MODE: {MOTION_MODES[parent.status.motion_mode]}')
		# this sets up home related items
		if parent.status.motion_mode == emc.TRAJ_MODE_TELEOP:
			#print('status update TRAJ_MODE_TELEOP')
			# FIXME releasing estop enables home required hal buttons
			if not parent.probing:
				for item in parent.home_required:
					getattr(parent, item).setEnabled(True)
			if parent.status.file and not parent.probing:
				for item in parent.run_controls:
					getattr(parent, item).setEnabled(True)
		elif parent.status.motion_mode == emc.TRAJ_MODE_FREE:
			#print('status update TRAJ_MODE_FREE')
			for item in parent.home_required:
				getattr(parent, item).setEnabled(False)
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(False)

		parent.motion_mode = parent.status.motion_mode

	# **** MOTION TYPE ****
	if parent.motion_type != parent.status.motion_type:
		#print(f'MOTION TYPE: {MOTION_TYPES[parent.status.motion_type]}')
		parent.motion_type = parent.status.motion_type

	# **** INTERP STATE ****
	# interp_state INTERP_IDLE, INTERP_READING, INTERP_PAUSED, INTERP_WAITING
	if parent.interp_state != parent.status.interp_state:
		#print(f'INTERP STATE: {INTERP_STATES[parent.status.interp_state]}')

		if parent.status.interp_state == emc.INTERP_IDLE:
			if parent.status.task_mode == emc.MODE_AUTO: # program has finished
				#print('status update INTERP_IDLE MODE_AUTO')
				parent.command.mode(emc.MODE_MANUAL)
				#print('status.py 195 parent.command.mode(emc.MODE_MANUAL)')
				parent.command.wait_complete()
				#print('status.py 198 parent.command.wait_complete()')
				#print(f'{TASK_MODES[parent.status.task_mode]}')

			if parent.status.task_mode == emc.MODE_MDI: # mdi is done
				#print('status update INTERP_IDLE MODE_MDI')
				if parent.tool_button:
					parent.tool_button = False
					parent.command.mode(emc.MODE_MANUAL)
					#print('status.py 205 parent.command.mode(emc.MODE_MANUAL)')
					parent.command.wait_complete()
					#print('status.py 207 parent.command.wait_complete()')
				elif parent.tool_changed:
					parent.tool_changed = False
					parent.command.mode(emc.MODE_MANUAL)
					parent.command.wait_complete()
				else:
					parent.command.mode(emc.MODE_MANUAL)
					parent.command.wait_complete()


		if parent.status.task_mode == emc.MODE_AUTO:
			# program is running
			if 'run_pb' in parent.child_names and hasattr(parent.run_pb, 'led'):
				parent.run_pb.led = True

			if parent.status.interp_state == emc.INTERP_WAITING:
				#print('INTERP_WAITING MODE_AUTO')
				for key, value in parent.program_paused.items():
					getattr(parent, key).setEnabled(value)
				if parent.status.exec_state != emc.EXEC_WAITING_FOR_IO:
					for key, value in parent.program_running.items():
						getattr(parent, key).setEnabled(value)

		# program is paused in either auto or mdi
		if parent.status.interp_state == emc.INTERP_PAUSED:
			#print('INTERP_PAUSED MODE_AUTO')
			for key, value in parent.program_paused.items():
				getattr(parent, key).setEnabled(value)
			if 'pause_pb' in parent.child_names and hasattr(parent.pause_pb, 'led'):
				parent.pause_pb.led = True
			if 'resume_pb' in parent.child_names and hasattr(parent.resume_pb, 'led'):
				parent.resume_pb.led = True
		else: # not paused
			if 'pause_pb' in parent.child_names and hasattr(parent.pause_pb, 'led'):
				parent.pause_pb.led = False
			if 'resume_pb' in parent.child_names and hasattr(parent.resume_pb, 'led'):
				parent.resume_pb.led = False

		if parent.status.interp_state == emc.INTERP_READING:
			#print('INTERP_READING')
			if parent.status.task_mode == emc.MODE_AUTO:
				for key, value in parent.program_running.items():
					getattr(parent, key).setEnabled(value)

		parent.interp_state = parent.status.interp_state

	# **** TASK MODE ****
	# task_mode MODE_MDI, MODE_AUTO, MODE_MANUAL
	if parent.task_mode != parent.status.task_mode:
		#print(f'TASK MODE: {TASK_MODES[parent.status.task_mode]}')
		if parent.status.task_mode == emc.MODE_MANUAL:
			if 'manual_mode_pb' in parent.child_names and hasattr(parent.manual_mode_pb, 'led'):
				parent.manual_mode_pb.led = True
			if 'mdi_mode_pb' in parent.child_names and hasattr(parent.mdi_mode_pb, 'led'):
				parent.mdi_mode_pb.led = False
			if 'auto_mode_pb' in parent.child_names and hasattr(parent.auto_mode_pb, 'led'):
				parent.auto_mode_pb.led = False
			if 'run_pb' in parent.child_names and hasattr(parent.run_pb, 'led'):
				parent.run_pb.led = False
			# enable flood and mist buttons

		if parent.status.task_mode == emc.MODE_MDI:
			if 'manual_mode_pb' in parent.child_names and hasattr(parent.manual_mode_pb, 'led'):
				parent.manual_mode_pb.led = False
			if 'mdi_mode_pb' in parent.child_names and hasattr(parent.mdi_mode_pb, 'led'):
				parent.mdi_mode_pb.led = True
			if 'auto_mode_pb' in parent.child_names and hasattr(parent.auto_mode_pb, 'led'):
				parent.auto_mode_pb.led = False
			if 'run_pb' in parent.child_names and hasattr(parent.run_pb, 'led'):
				parent.run_pb.led = False
			for item in parent.probe_controls:
				getattr(parent, item).setEnabled(False)

		if parent.status.task_mode == emc.MODE_AUTO:
			if 'manual_mode_pb' in parent.child_names and hasattr(parent.manual_mode_pb, 'led'):
				parent.manual_mode_pb.led = False
			if 'mdi_mode_pb' in parent.child_names and hasattr(parent.mdi_mode_pb, 'led'):
				parent.mdi_mode_pb.led = False
			if 'auto_mode_pb' in parent.child_names and hasattr(parent.auto_mode_pb, 'led'):
				parent.auto_mode_pb.led = True
			if 'run_pb' in parent.child_names and hasattr(parent.run_pb, 'led'):
				parent.run_pb.led = True
			# disable flood and mist buttons

		if parent.status.task_state == emc.STATE_ON:
			if parent.status.task_mode == emc.MODE_MANUAL:
				if parent.status.interp_state == emc.INTERP_IDLE:
					if parent.probing:
						#print(f'parent.probing {parent.probing}')
						for item in parent.probe_controls:
							getattr(parent, item).setEnabled(True)
					else:
						#print('Task Mode Manual, Not Probing')
						for key, value in parent.state_on.items():
							getattr(parent, key).setEnabled(value)
						if parent.status.file:
							#print('status update FILE LOADED')
							for item in parent.file_edit_items:
								getattr(parent, item).setEnabled(True)
							if utilities.all_homed(parent):
								#print('status update FILE LOADED and ALL HOMED')
								for item in parent.run_controls:
									getattr(parent, item).setEnabled(True)

		if parent.status.task_mode == emc.MODE_MANUAL:
			if 'manual_mode_pb' in parent.child_names and hasattr(parent.manual_mode_pb, 'led'):
				parent.manual_mode_pb.led = True
			if 'run_pb' in parent.child_names and hasattr(parent.run_pb, 'led'):
				parent.run_pb.led = False

		parent.task_mode = parent.status.task_mode

	# **** EXEC STATE ****
	#exec_state EXEC_ERROR, EXEC_DONE, EXEC_WAITING_FOR_MOTION,
	#EXEC_WAITING_FOR_MOTION_QUEUE, EXEC_WAITING_FOR_IO,
	#EXEC_WAITING_FOR_MOTION_AND_IO, EXEC_WAITING_FOR_DELAY,
	#EXEC_WAITING_FOR_SYSTEM_CMD, EXEC_WAITING_FOR_SPINDLE_ORIENTED.
	if parent.exec_state != parent.status.exec_state:
		#print(f'EXEC STATE: {EXEC_STATES[parent.status.exec_state]}')
		if parent.status.exec_state == emc.EXEC_WAITING_FOR_MOTION:
			for key, value in parent.program_running.items():
				getattr(parent, key).setEnabled(value)
		parent.exec_state = parent.status.exec_state

	# **** STATE ****
	# state RCS_DONE, RCS_EXEC, RCS_ERROR
	if parent.state != parent.status.state:
		#print(f'STATE: {STATES[parent.status.state]}')
		parent.state = parent.status.state

	# **** MDI CHANGE ****
	if parent.mdi_command != '':
		if parent.status.task_mode == emc.MODE_MDI:
			if parent.status.interp_state == emc.INTERP_IDLE:
				utilities.update_mdi(parent)

	# **** TOOL CHANGE ****
	if parent.manual_tool_change:
		if parent.tool_change != hal.get_value('tool-change.change'):
			if hal.get_value('iocontrol.0.tool-changed'):
				hal.set_p('iocontrol.0.tool-changed','false')
			else:
				dialogs.manual_tool_change(parent)
			parent.tool_change = hal.get_value('tool-change.change')

	# **** TOOL IN SPINDLE CHANGE ****
	if parent.tool_in_spindle != parent.status.tool_in_spindle:
		tool = parent.status.tool_in_spindle
		if 'touchoff_selected_tool_pb' in parent.child_names:
			if tool > 0:
				parent.touchoff_selected_tool_pb.setEnabled(True)
			else:
				parent.touchoff_selected_tool_pb.setEnabled(False)
		parent.tool_in_spindle = parent.status.tool_in_spindle

	# **** FLOOD_OFF or FLOOD_ON **** 
	if parent.flood_state != parent.status.flood:
		if 'flood_pb' in parent.child_names:
			if parent.status.flood == emc.FLOOD_OFF:
				parent.flood_pb.setChecked(False)
				if hasattr(parent.flood_pb, 'led'):
					parent.flood_pb.led = False
			elif parent.status.flood == emc.FLOOD_ON:
				parent.flood_pb.setChecked(True)
				if hasattr(parent.flood_pb, 'led'):
					parent.flood_pb.led = True
		parent.flood_state = parent.status.flood

	# **** MIST_OFF or MIST_ON ****
	if parent.mist_state != parent.status.mist:
		if 'mist_pb' in parent.child_names: 
			if parent.status.mist == emc.MIST_OFF:
				parent.mist_pb.setChecked(False)
				if hasattr(parent.mist_pb, 'led'):
					parent.mist_pb.led = False
			elif parent.status.mist == emc.MIST_ON:
				parent.mist_pb.setChecked(True)
				if hasattr(parent.mist_pb, 'led'):
					parent.mist_pb.led = True
		parent.mist_state = parent.status.mist

	# **** SPINDLE SETTINGS ****
	# spindle status
	if parent.status_spindle != parent.status.spindle:

		# spindle brake
		if 'spindle_brake_0_lb' in parent.child_names:
			match parent.status.spindle[0]['brake']:
				case b if b == 1:
					parent.spindle_brake_0_lb.setText('On')
				case b if b == 0:
					parent.spindle_brake_0_lb.setText('Off')
		parent.spindle_brake = parent.status.spindle[0]['brake']

		# spindle direction
		if 'spindle_direction_0_lb' in parent.child_names:
			match parent.status.spindle[0]['direction']:
				case s if s == 1:
					parent.spindle_direction_0_lb.setText('Fwd')
				case s if s == -1:
					parent.spindle_direction_0_lb.setText('Rev')
				case s if s == 0:
					parent.spindle_direction_0_lb.setText('Off')
		parent.spindle_direction = parent.status.spindle[0]['direction']

		# spindle enabled
		if 'spindle_enabled_0_lb' in parent.child_names:
			match parent.status.spindle[0]['enabled']:
				case s if s == 0:
					parent.spindle_enabled_0_lb.setText('False')
				case s if s == 1:
					parent.spindle_enabled_0_lb.setText('True')
		parent.spindle_enabled = parent.status.spindle[0]['enabled']

		for key, value in parent.status_spindles.items():
			getattr(parent, key).setText(f'{getattr(parent, "status").spindle[0][value]}')

		# spindle speed
		for key, value in parent.status_spindle_speed.items():
			getattr(parent, key).setText(f'{abs(getattr(parent, "status").spindle[0][value]):.0f}')

		# spindle lcd
		for key, value in parent.status_spindle_lcd.items():
			getattr(parent, key).display(f'{abs(getattr(parent, "status").spindle[0][value]):.0f}')

		# spindle override parent.spindle[0]['override']
		for key, value in parent.status_spindle_overrides.items():
			getattr(parent, f'{key}').setText(f'{getattr(parent, "status").spindle[value]["override"] * 100:.0f}%')

		# spindle actual speed
		for item in parent.spindle_actual_speed:
			override = parent.spindle_override_sl.value() / 100
			commanded_rpm = abs(parent.status.spindle[0]['speed'])
			override_rpm = commanded_rpm * override
			if override_rpm >= parent.min_rpm:
				getattr(parent, item).setText(f'{override_rpm:.0f}')
			elif override_rpm > 0:
				getattr(parent, item).setText(f'{parent.min_rpm:.0f}')
			else:
				getattr(parent, item).setText('0')

		parent.status_spindle = parent.status.spindle

	# status labels
	# key is label and value is status item
	for key, value in parent.status_labels.items(): # update all status labels
		if value in parent.stat_dict:
			stat_value = getattr(parent.status, f'{value}')
			if stat_value in parent.stat_dict[value]:
				getattr(parent, f'{key}').setText(f'{parent.stat_dict[value][stat_value]}')
		else:
			getattr(parent, f'{key}').setText(f'{getattr(parent.status, f"{value}")}')

	# status exponent labels key is the label and value is the status item
	for key, value in parent.status_exponent_labels.items():
		getattr(parent, f'{key}').setText(f'{getattr(parent.status, value):e}')

	# status float labels
	for key, value in parent.status_float_labels.items():
		getattr(parent, f'{key}_lb').setText(f'{getattr(parent.status, key):.{value}f}')

	# joint status items
	for key, value in parent.status_joints.items():
	#	value = 'joint[0]["enabled"]'
	#	getattr(parent, f'{key}').setText(f'{getattr(parent.status, value)}')
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").joint[0][value]}')

	# joint status items with precision key is item value is [joint, precision]
	for key, value in parent.status_joint_prec.items():
		getattr(parent, f'joint_{value[0]}_{key}_lb').setText(f'{getattr(parent, "status").joint[value[0]][key]:.{value[1]}f}')

	# G codes only update when they change
	if parent.g_codes != parent.status.gcodes:
		g_codes = []
		for i in parent.status.gcodes[1:]:
			if i == -1: continue
			if i % 10 == 0:
				g_codes.append(f'G{(i/10):.0f}')
			else:
				g_codes.append(f'G{(i/10):.0f}.{i%10}')

		if 'gcodes_lb' in parent.child_names:
			parent.gcodes_lb.setText(f'{" ".join(g_codes)}')

		if 'G20' in g_codes:
			parent.program_units = 'INCH'
		else:
			parent.program_units = 'MM'
		
		for units_lb_name in parent.program_units_labels:
			getattr(parent, units_lb_name).setText(parent.program_units)

		parent.g_codes = parent.status.gcodes

	# M codes only update when they change
	if parent.m_codes != parent.status.mcodes:
		if 'mcodes_lb' in parent.child_names:
			m_codes = []
			for i in parent.status.mcodes[1:]:
				if i == -1: continue
				m_codes.append(f'M{i}')
			parent.mcodes_lb.setText(f'{" ".join(m_codes)}')
		parent.m_codes = parent.status.mcodes

	# update gcode_pte only if motion line changes
	if parent.motion_line != parent.status.motion_line:
		parent.motion_line != parent.status.motion_line
		if 'gcode_pte' in parent.child_names:
			if parent.motion_line != parent.last_line:
				cursor = parent.gcode_pte.textCursor()
				cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(parent.motion_line))
				cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor)
				parent.gcode_pte.setTextCursor(cursor)
				parent.last_line = parent.motion_line

	# update hal labels key is label name and value[0] is pin name value[1] is digits
	for key, value in parent.hal_readers.items():
		state = hal.get_value(f'flexhal.{value[0]}')
		if value[1] is not None:
			state = f"{state:0{value[1]}d}"
		if isinstance(getattr(parent, key), QLCDNumber):
			getattr(parent, key).display(f'{state}')
		else: # it's a HAL Label
			getattr(parent, key).setText(f'{state}')

	# update hal average float labels key is label name and value is pin name
	for key, value in parent.hal_avr_float.items():
		cur_val = hal.get_value(f'flexhal.{value[0]}')
		value[1].append(cur_val)
		getattr(parent, key).setText(f'{statistics.fmean(value[1]):.{value[2]}f}')

	# update multi state labels
	# key is label name and value[0] is the pin name
	for key, value in parent.hal_ms_labels.items():
		state = hal.get_value(f'flexhal.{value[0]}')
		if state < len(value[1]):
			getattr(parent, key).setText(f'{value[1][state]}')

	# update hal bool labels
	# key is label name, value[0] is pin name, value[1] is true text, value[2] is false text
	for key, value in parent.hal_bool_labels.items():
		state = hal.get_value(f'flexhal.{value[0]}')
		if state:
			getattr(parent, key).setText(value[1])
		else:
			getattr(parent, key).setText(value[2])

	# update hal progressbars key is the progressbar name and value is the pin name
	for key, value in parent.hal_progressbars.items():
		value = hal.get_value(f'flexhal.{value}')
		getattr(parent, key).setValue(int(value))

	# update hal float labels
	for key, value in parent.hal_floats.items():
		# label [status item, precision]
		hal_value = hal.get_value(f'flexhal.{value[0]}')
		if isinstance(getattr(parent, key), QLCDNumber):
			getattr(parent, key).display(f'{hal_value:.{value[1]}f}')
		else:
			getattr(parent, key).setText(f'{hal_value:.{value[1]}f}')

	# update hal leds
	for key, value in parent.hal_leds.items():
		getattr(parent, key).led = hal.get_value(f'flexhal.{value}')

	# update hal led labels
	for key, value in parent.hal_led_labels.items():
		getattr(parent, key).led = hal.get_value(f'flexhal.{value}')

	# homed status
	for item in parent.home_status:
		if parent.status.homed[int(item[-1])]:
			getattr(parent, item).setText('*')
		else:
			getattr(parent, item).setText('')

	# plotter DRO
	if parent.auto_plot_units and parent.program_units != parent.plot_units:
		if parent.program_units == 'INCH': # inch program units
			parent.plotter.metric_units = False
		elif parent.program_units == 'MM': # metric program units
			parent.plotter.metric_units = True
		parent.plotter.update()
		parent.plot_units = parent.program_units

	# axis position no offsets
	for key, value in parent.status_position.items(): # key is label value precision
		machine_position = getattr(parent, "status").position[value[0]]
		getattr(parent, f'{key}').setText(f'{machine_position:.{value[1]}f}')

	positions = parent.status.position
	positions = [(i-j) for i, j in zip(positions, parent.status.tool_offset)]
	positions = [(i-j) for i, j in zip(positions, parent.status.g5x_offset)]
	t = -parent.status.rotation_xy
	t = math.radians(t)
	_x = positions[X]
	_y = positions[Y]
	positions[X] = _x * math.cos(t) - _y * math.sin(t)
	positions[Y] = _x * math.sin(t) + _y * math.cos(t)
	positions = [(i-j) for i, j in zip(positions, parent.status.g92_offset)]

	# label, tuple position & precision
	for key, value in parent.status_dro.items(): # key is label value list position & precision
		position = positions[value[0]]


		'''
		g5x_offset = getattr(parent, "status").g5x_offset[value[0]]
		g92_offset = getattr(parent, "status").g92_offset[value[0]]
		g43_offset = getattr(parent, "status").tool_offset[value[0]]
		machine_position = getattr(parent, "status").position[value[0]]
		relative_position = machine_position - (g5x_offset + g92_offset + g43_offset)
		'''

		# metric linear units with inch program units
		if parent.status.linear_units == 1 and parent.program_units == 'INCH' and parent.auto_dro_units:
			getattr(parent, f'{key}').setText(f'{position * 0.03937007874015748:.4f}')
		# inch linear units with metric program units
		elif parent.status.linear_units != 1 and parent.program_units == 'MM' and parent.auto_dro_units:
			getattr(parent, f'{key}').setText(f'{position * 25.4:.3f}')
		# linear units and program units are the same
		else:
			getattr(parent, f'{key}').setText(f'{position:.{value[1]}f}')

	# axis g5x offset
	for key, value in parent.status_g5x_offset.items(): # key is label value tuple position & precision
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").g5x_offset[value[0]]:.{value[1]}f}')

	# axis g92 offset
	for key, value in parent.status_g92.items(): # key is label value tuple position & precision
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").g92_offset[value[0]]:.{value[1]}f}')

	# axis DTG
	for key, value in parent.status_dtg.items(): # key is label value tuple position & precision
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").dtg[value[0]]:.{value[1]}f}')

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
		vel = math.sqrt((vel_0 * vel_0) + (vel_1 * vel_1))
		getattr(parent, key).setText(f'{vel * 60:.{value[2]}f}')

	# three joint velocity
	for key, value in parent.three_vel.items():
		vel_0 = getattr(parent, 'status').joint[value[0]]['velocity']
		vel_1 = getattr(parent, 'status').joint[value[1]]['velocity']
		vel_2 = getattr(parent, 'status').joint[value[2]]['velocity']
		vel = math.sqrt((vel_0 * vel_0) + (vel_1 * vel_1) + (vel_2 * vel_2))
		getattr(parent, key).setText(f'{vel * 60:.{value[3]}f}')

	# override items label : status item
	for key, value in parent.overrides.items():
		getattr(parent, key).setText(f'{getattr(parent.status, f"{value}") * 100:.0f}%')

	# dio din_0_lb din[0] dout_0_lb dout[0]
	for key, value in parent.status_dio.items():
		state = getattr(parent.status, f"{value[0]}")[value[1]]
		item = f'{value[0]}[{value[1]}]'
		getattr(parent, f'{key}').setText(f'{parent.stat_dict[item][state]}')

	# aio ain_0_lb aout_0_lb aio[0] aout[0]
	for key, value in parent.status_aio.items():
		getattr(parent, f'{key}').setText(f'{getattr(parent.status, f"{value[0]}")[value[1]]:.{value[2]}f}')

	# current tool info
	if parent.current_tool_info != parent.status.tool_table[0]:
		for key, value in parent.current_tool_intergers.items():
			tr = parent.status.tool_table[0]
			getattr(parent, key).setText(f'{getattr(tr, value)}')

		for key, value in parent.current_tool_floats.items():
			tr = parent.status.tool_table[0]
			getattr(parent, key).setText(f'{getattr(tr, value[0]):.{value[1]}f}')

		parent.current_tool_info = parent.status.tool_table[0]

	# handle errors
	error = parent.error.poll()
	if error:
		kind, text = error
		if kind in (emc.NML_ERROR, emc.OPERATOR_ERROR):
			error_type = 'Error'
		else:
			error_type = 'Info'
		if 'override_limits_cb' in parent.child_names:
			if 'limit switch error' in text:
				parent.override_limits_cb.setEnabled(True)
		if error_type == 'Info':
			if 'info_pte' in parent.child_names:
				parent.info_pte.appendPlainText(error_type)
				parent.info_pte.appendPlainText(text)
			elif 'errors_pte' in parent.child_names:
				parent.errors_pte.appendPlainText(error_type)
				parent.errors_pte.appendPlainText(text)
				parent.errors_pte.setFocus()
				if 'statusbar' in parent.child_names:
					parent.statusbar.showMessage('Error')
		elif error_type == 'Error':
			if 'errors_pte' in parent.child_names:
				parent.errors_pte.appendPlainText(error_type)
				parent.errors_pte.appendPlainText(text)
				parent.errors_pte.setFocus()
				if 'statusbar' in parent.child_names:
					parent.statusbar.showMessage('Error')



