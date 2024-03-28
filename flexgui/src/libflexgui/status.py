import sys, os

from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor, QAction

import linuxcnc as emc

from libflexgui import utilities

'''

// types for EMC_TASK execState
EMC_TASK_EXEC_ERROR = 1,
EMC_TASK_EXEC_DONE = 2,
EMC_TASK_EXEC_WAITING_FOR_MOTION = 3,
EMC_TASK_EXEC_WAITING_FOR_MOTION_QUEUE = 4,
EMC_TASK_EXEC_WAITING_FOR_IO = 5,
EMC_TASK_EXEC_WAITING_FOR_MOTION_AND_IO = 7,
EMC_TASK_EXEC_WAITING_FOR_DELAY = 8,
EMC_TASK_EXEC_WAITING_FOR_SYSTEM_CMD = 9,
EMC_TASK_EXEC_WAITING_FOR_SPINDLE_ORIENTED = 10

// types for motion control
EMC_TRAJ_MODE_FREE = 1,	// independent-axis motion,
EMC_TRAJ_MODE_COORD = 2,	// coordinated-axis motion,
EMC_TRAJ_MODE_TELEOP = 3	// velocity based world coordinates motion,

interp_state
INTERP_IDLE = 1
INTERP_READING = 2
INTERP_PAUSED = 3
INTERP_WAITING = 4

interpreter_errcode
INTERP_OK = 0,
INTERP_EXIT = 1,
INTERP_EXECUTE_FINISH = 2,
INTERP_ENDFILE = 3,
INTERP_FILE_NOT_OPEN = 4,
INTERP_ERROR = 5,

kinematics_type
KINEMATICS_IDENTITY 0
KINEMATICS_FORWARD_ONLY 1
KINEMATICS_INVERSE_ONLY 2
KINEMATICS_BOTH 3

// types for emcIoAbort() reasons
EMC_ABORT_TASK_EXEC_ERROR = 1,
EMC_ABORT_AUX_ESTOP = 2,
EMC_ABORT_MOTION_OR_IO_RCS_ERROR = 3,
EMC_ABORT_TASK_STATE_OFF = 4,
EMC_ABORT_TASK_STATE_ESTOP_RESET = 5,
EMC_ABORT_TASK_STATE_ESTOP = 6,
EMC_ABORT_TASK_STATE_NOT_ON = 7,
EMC_ABORT_TASK_ABORT = 8,
EMC_ABORT_INTERPRETER_ERROR = 9,	// interpreter failed during readahead
EMC_ABORT_INTERPRETER_ERROR_MDI = 10,	// interpreter failed during MDI execution
EMC_ABORT_USER = 100  // user-defined abort codes start here

motion_mode
TRAJ_MODE_FREE 1
TRAJ_MODE_COORD 2
TRAJ_MODE_TELEOP 3

motion_type
MOTION_TYPE_NONE 0
MOTION_TYPE_TRAVERSE 1
MOTION_TYPE_FEED 2
MOTION_TYPE_ARC 3
MOTION_TYPE_TOOLCHANGE 4
MOTION_TYPE_PROBING 5
MOTION_TYPE_INDEXROTARY 6

program_units
CANON_UNITS_INCHES=1
CANON_UNITS_MM=2
CANON_UNITS_CM=3

state
linuxcnc.RCS_DONE 1
linuxcnc.RCS_EXEC 2
linuxcnc.RCS_ERROR 3

task_mode
linuxcnc.MODE_MANUAL 1
linuxcnc.MODE_AUTO 2
linuxcnc.MODE_MDI 3

task_state
linuxcnc.STATE_ESTOP 1
linuxcnc.STATE_ESTOP_RESET 2
linuxcnc.STATE_ON 4

motion_mode
TRAJ_MODE_FREE = 1
TRAJ_MODE_COORD = 2
TRAJ_MODE_TELEOP = 3

linuxcnc.

: '', 
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

	# task_state STATE_ESTOP, STATE_ESTOP_RESET, STATE_ON, STATE_OFF
	if parent.task_state != parent.status.task_state:
		if parent.print_states:
			print(f'task state changed to {TASK_STATES[parent.status.task_state]}')
		# update button and action text
		if 'estop_pb' in parent.children:
			if parent.status.task_state == 1:
				parent.estop_pb.setText('E Stop\nOpen')
			else:
				parent.estop_pb.setText('E Stop\nClosed')

		if 'actionE_Stop' in parent.children:
			if parent.status.task_state == 1:
				parent.actionE_Stop.setText('E Stop\nOpen')
			else:
				parent.actionE_Stop.setText('E Stop\nClosed')

		if 'power_pb' in parent.children:
			if parent.status.task_state == 4:
				parent.power_pb.setText('Power\nOn')
			else:
				parent.power_pb.setText('Power\nOff')

		if 'actionPower' in parent.children:
			if parent.status.task_state == 4:
				parent.actionPower.setText('Power\nOn')
			else:
				parent.actionPower.setText('Power\nOff')

		# enable/disable controls and actions based on task state
		# state_estop_open estop is open
		if parent.status.task_state == emc.STATE_ESTOP:
			for item in parent.state_estop_open:
				getattr(parent, item).setEnabled(False)

		# state_estop_closed estop is closed and power is off
		if parent.status.task_state == emc.STATE_ESTOP_RESET:
			for item in parent.state_estop_closed:
				getattr(parent, item).setEnabled(True)
			for item in parent.state_power_on:
				getattr(parent, item).setEnabled(False)
			for item in parent.state_all_homed:
				if utilities.all_homed(parent):
					getattr(parent, item).setEnabled(False)

		# state_power_on power is on
		if parent.status.task_state == emc.STATE_ON:
			for item in parent.state_power_on:
				getattr(parent, item).setEnabled(True)
			for item in parent.state_all_homed:
				if utilities.all_homed(parent):
					getattr(parent, item).setEnabled(True)
				else:
					getattr(parent, item).setEnabled(False)

			# if a file is loaded and machine is homed enable run and step
			if parent.status.file and utilities.all_homed(parent):
				for item in parent.file_loaded:
					getattr(parent, item).setEnabled(True)

			# home all push button
			if 'home_all_pb' in parent.children:
				if utilities.home_all_check(parent):
					parent.home_all_pb.setEnabled(True)

		parent.task_state = parent.status.task_state

	# exec_state EXEC_ERROR, EXEC_DONE, EXEC_WAITING_FOR_MOTION,
	# EXEC_WAITING_FOR_MOTION_QUEUE, EXEC_WAITING_FOR_IO,
	# EXEC_WAITING_FOR_MOTION_AND_IO, EXEC_WAITING_FOR_DELAY,
	# EXEC_WAITING_FOR_SYSTEM_CMD, EXEC_WAITING_FOR_SPINDLE_ORIENTED
	if parent.exec_state != parent.status.exec_state:
		if parent.print_states:
			print(f'exec state changed to {EXEC_STATES[parent.status.exec_state]}')
		if parent.status.exec_state == emc.EXEC_WAITING_FOR_MOTION:
			# program is running
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(False)
			for item in parent.program_running:
				getattr(parent, item).setEnabled(True)
		elif parent.status.exec_state == emc.EXEC_DONE:
			# program is not running or estop was toggled
			if parent.status.task_state == emc.STATE_ON:
				if parent.status.file:
					for item in parent.run_controls:
						getattr(parent, item).setEnabled(True)
				for item in parent.program_running:
					getattr(parent, item).setEnabled(False)
		parent.exec_state = parent.status.exec_state

	# interp_state INTERP_IDLE, INTERP_READING, INTERP_PAUSED, INTERP_WAITING
	if parent.interp_state != parent.status.interp_state:
		if parent.print_states:
			print(f'interpter state changed to {INTERP_STATES[parent.status.interp_state]}')
		if parent.status.interp_state == emc.INTERP_PAUSED:
			for item in parent.program_paused:
				getattr(parent, item).setEnabled(True)
			for item in parent.program_running:
				getattr(parent, item).setEnabled(False)
		elif parent.status.interp_state == emc.INTERP_WAITING:
			for item in parent.program_paused:
				getattr(parent, item).setEnabled(False)
			for item in parent.program_running:
				getattr(parent, item).setEnabled(True)
		elif parent.status.interp_state == emc.INTERP_IDLE:
			if parent.status.task_mode == emc.MODE_MDI:
				utilities.update_mdi(parent)
		parent.interp_state = parent.status.interp_state

	# motion_mode TRAJ_MODE_COORD, TRAJ_MODE_FREE, TRAJ_MODE_TELEOP
	if parent.motion_mode != parent.status.motion_mode:
		if parent.print_states:
			print(f'motion mode changed to {MOTION_MODES[parent.status.motion_mode]}')
		parent.motion_mode = parent.status.motion_mode

	# task_mode MODE_MDI, MODE_AUTO, MODE_MANUAL
	if parent.task_mode != parent.status.task_mode:
		if parent.print_states:
			print(f'task mode changed to {TASK_MODES[parent.status.task_mode]}')
		#print(f'interp state is {INTERP_STATES[parent.status.interp_state]}')
		if parent.status.task_mode == emc.MODE_MDI:
			if parent.status.interp_state == emc.INTERP_IDLE:
				utilities.update_mdi(parent)
		parent.task_mode = parent.status.task_mode

	# state RCS_DONE, RCS_EXEC, RCS_ERROR
	if parent.state != parent.status.state:
		if parent.print_states:
			print(f'state changed to {STATES[parent.status.state]}')
		parent.state = parent.status.state

	for key, value in parent.status_labels.items(): # update all status labels
		# key is the status item and value is the label
		# get the label and set the text to the status value of the key
		if key in parent.stat_dict:
			stat_value = getattr(parent.status, f'{key}')
			if stat_value in parent.stat_dict[key]:
				getattr(parent, f'{value}').setText(f'{parent.stat_dict[key][stat_value]}')
		else:
			getattr(parent, f'{value}').setText(f'{getattr(parent.status, f"{key}")}')

	for key, value in parent.status_axes.items():
		if key == 'velocity':
			vel = abs(round(getattr(parent, 'status').axis[int(value[5])][key] * 60, 1))
			getattr(parent, f'{value}').setText(f'{vel}')
		else:
			getattr(parent, f'{value}').setText(f'{getattr(parent, "status").axis[int(value[-4])][key[0:-2]]}')

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

	# axis position no offsets
	for key, value in parent.status_position.items(): # key is label value tuple position & precision
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

	# axis s.axis[0]['velocity'] FIXME precision
	for key, value in parent.status_axes.items(): # hmm max is 9 I think...
		key = key[0:-2]
		getattr(parent, f'{value}').setText(f'{getattr(parent, "status").axis[int(value[-4])][key]}')

	# joints s.joint[0]['units']
	for key, value in parent.status_joints.items(): # up to 16 items
		if int(key.split('_')[-1]) > 9: # determine how many chars to strip
			key = key[0:-3]
		else:
			key = key[0:-2]
		getattr(parent, f'{value}').setText(f'{getattr(parent, "status").joint[int(value[-4])][key]}')

	# joints precision items
	for key, value in parent.status_joint_prec.items(): # key is label value tuple position & precision
		if int(key.split('_')[-1]) > 9: # determine how many chars to strip
			key = key[0:-3]
		else:
			key = key[0:-2]
		# if velocity * 60 FIXME
		getattr(parent, f'joint_{key}_{value[0]}_lb').setText(f'{getattr(parent, "status").joint[value[0]][key]:.{value[1]}f}')

		# print(f'{getattr(parent, "status").joint[value[0]][key]:.{value[1]}f}')
		# getattr(parent, f'{key}').setText(f'{getattr(parent, "status").joint[value[0]]:.{value[1]}f}')

	# current tool offsets FIXME
	for key, value in parent.status_tool_offset.items(): # key is label value tuple position & precision
		getattr(parent, f'{key}').setText(f'{getattr(parent, "status").tool_offset[value[0]]:.{value[1]}f}')

	# i/o s.ain[0] FIXME precision
	for key, value in parent.status_io.items(): # up to 64 items
		# there might be more than one underscore
		if int(key.split('_')[-1]) > 9: # determine how many chars to strip
			key = key[0:-3]
		else:
			key = key[0:-2]
		getattr(parent, f'{value}').setText(f'{getattr(parent.status, f"{key}")[int(value[-4])]}')

	# i/o s.aout[0] FIXME precision
	# i/o s.din[0]
	# i/o s.dout[0]

	# spindle s.spindle[0]['brake']
	for key, value in parent.status_spindles.items():
		key = key[0:-2]
		getattr(parent, f'{value}').setText(f'{getattr(parent, "status").spindle[int(value[-4])][key]}')

	# tool table s.tool_table[0].id
	for key, value in parent.tool_table.items():
		tool = int(key.split('_')[-1])
		key = key.split('_')[0] # get the status name from key xoffset_0
		tr = getattr(parent.status, 'tool_table')[tool]
		getattr(parent, f'{value}').setText(f'{getattr(tr, key)}')

	# STATE_ESTOP STATE_ESTOP_RESET STATE_ON
	if parent.status.state == emc.STATE_ESTOP:
		pass

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
			#tabname = 'status_tab'
			#print(parent.tabWidget.findChild(QWidget, 'status_tab'))
			#page = parent.tabWidget.findChild(QWidget, tabname)
			#print(page)
			#index = parent.tabWidget.indexOf(page)
			#print(index)
			#if isinstance(parent.tabWidget.findChild(QWidget, 'status_tab'), QWidget):
			#	parent.tabWidget.setCurrentWidget(parent.tabWidget.findChild(QWidget, 'status_tab'))

