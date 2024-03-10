import sys

from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor, QAction

import linuxcnc

#  (returns integer) - This is the mode of the Motion controller.
# One of TRAJ_MODE_COORD, TRAJ_MODE_FREE, TRAJ_MODE_TELEOP

#print(stat_dict['motion_mode'][getattr(parent.status, 'motion_mode')])
'''
// types for EMC_TASK mode
EMC_TASK_MODE_MANUAL = 1,
EMC_TASK_MODE_AUTO = 2,
EMC_TASK_MODE_MDI = 3

// types for EMC_TASK state
EMC_TASK_STATE_ESTOP = 1,
EMC_TASK_STATE_ESTOP_RESET = 2,
EMC_TASK_STATE_OFF = 3,
EMC_TASK_STATE_ON = 4

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

// types for EMC_TASK interpState
EMC_TASK_INTERP_IDLE = 1,
EMC_TASK_INTERP_READING = 2,
EMC_TASK_INTERP_PAUSED = 3,
EMC_TASK_INTERP_WAITING = 4

// types for motion control
EMC_TRAJ_MODE_FREE = 1,	// independent-axis motion,
EMC_TRAJ_MODE_COORD = 2,	// coordinated-axis motion,
EMC_TRAJ_MODE_TELEOP = 3	// velocity based world coordinates motion,

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


linuxcnc.

: '', 
'''

def update(parent):
	parent.status.poll()

	# STATE_ESTOP, STATE_ESTOP_RESET, STATE_ON, STATE_OFF
	if parent.task_state != parent.status.task_state:
		if parent.findChild(QPushButton, 'estop_pb'):
			if parent.status.task_state == 1:
				parent.estop_pb.setText('E Stop\nOpen')
			else:
				parent.estop_pb.setText('E Stop\nClosed')

		if parent.findChild(QAction, 'actionE_Stop'):
			if parent.status.task_state == 1:
				parent.actionE_Stop.setText('E Stop\nOpen')
			else:
				parent.actionE_Stop.setText('E Stop\nClosed')

		if parent.findChild(QPushButton, 'power_pb'):
			if parent.status.task_state == 4:
				parent.power_pb.setText('Power\nOn')
			else:
				parent.power_pb.setText('Power\nOff')
		if parent.findChild(QAction, 'actionPower'):
			if parent.status.task_state == 4:
				parent.actionPower.setText('Power\nOn')
			else:
				parent.actionPower.setText('Power\nOff')

		# enable/disable controls and actions
		if parent.status.task_state == linuxcnc.STATE_ESTOP:
			for item in parent.state_estop_list:
				getattr(parent, item).setEnabled(False)
		if parent.status.task_state == linuxcnc.STATE_ESTOP_RESET:
			for item in parent.state_estop_reset_list:
				getattr(parent, item).setEnabled(True)
		if parent.status.task_state == linuxcnc.STATE_ON:
			for item in parent.state_on_list:
				getattr(parent, item).setEnabled(True)

		parent.task_state = parent.status.task_state

	stat_dict = {'adaptive_feed_enabled': {0: False, 1: True},
	'motion_mode': {1: 'TRAJ_MODE_FREE', 2: 'TRAJ_MODE_COORD', 3: 'TRAJ_MODE_TELEOP'},
	'exec_state': {1: 'EXEC_ERROR', 2: 'EXEC_DONE', 3: 'EXEC_WAITING_FOR_MOTION',
		4: 'EXEC_WAITING_FOR_MOTION_QUEUE', 5: 'EXEC_WAITING_FOR_IO',
		7: 'EXEC_WAITING_FOR_MOTION_AND_IO', 8: 'EXEC_WAITING_FOR_DELAY',
		9: 'EXEC_WAITING_FOR_SYSTEM_CMD', 10: 'EXEC_WAITING_FOR_SPINDLE_ORIENTED',},
	'estop': {0: False, 1: True},
	'flood': {0: 'FLOOD_OFF', 1: 'FLOOD_ON'},
	'g5x_index': {1: 'G54', 2: 'G55', 3: 'G56', 4: 'G57', 5: 'G58', 6: 'G59',
		7: 'G59.1', 8: 'G59.2', 9: 'G59.3'},
	'interp_state': {1: 'EMC_TASK_INTERP_IDLE', 2: 'EMC_TASK_INTERP_READING',
		3: 'EMC_TASK_INTERP_PAUSED', 4: 'EMC_TASK_INTERP_WAITING'},
	'interpreter_errcode': {0: 'INTERP_OK', 1: 'INTERP_EXIT',
		2: 'INTERP_EXECUTE_FINISH', 3: 'INTERP_ENDFILE', 4: 'INTERP_FILE_NOT_OPEN',
		5: 'INTERP_ERROR'},
	'kinematics_type': {1: 'KINEMATICS_IDENTITY', 2: 'KINEMATICS_FORWARD_ONLY',
		3: 'KINEMATICS_INVERSE_ONLY', 4: 'KINEMATICS_BOTH'},
	'motion_mode': {1: 'TRAJ_MODE_FREE', 2: 'TRAJ_MODE_COORD', 3: 'TRAJ_MODE_TELEOP'},
	'motion_type': {0: 'MOTION_TYPE_NONE', 1: 'MOTION_TYPE_TRAVERSE',
		2: 'MOTION_TYPE_FEED', 3: 'MOTION_TYPE_ARC', 4: 'MOTION_TYPE_TOOLCHANGE',
		5: 'MOTION_TYPE_PROBING', 6: 'MOTION_TYPE_INDEXROTARY'},
	'program_units': {1: 'CANON_UNITS_INCHES', 2: 'CANON_UNITS_MM', 3: 'CANON_UNITS_CM'},
	'state': {1: 'RCS_DONE', 2: 'RCS_EXEC', 3: 'RCS_ERROR'},
	'task_mode': {1: 'MODE_MANUAL', 2: 'MODE_AUTO', 3: 'MODE_MDI', },
	'task_state': {1: 'STATE_ESTOP', 2: 'STATE_ESTOP_RESET', 4: 'STATE_ON', },
	}

	for key, value in parent.status_labels.items(): # update all status labels
		# get the label and set the text to the status value of the key
		if key in stat_dict:
			stat_value = getattr(parent.status, f'{key}')
			if stat_value in stat_dict[key]:
				getattr(parent, f'{value}').setText(f'{stat_dict[key][stat_value]}')
		else:
			getattr(parent, f'{value}').setText(f'{getattr(parent.status, f"{key}")}')

	for key, value in parent.status_axes.items():
		if key == 'velocity':
			vel = abs(round(getattr(parent, 'status').axis[int(value[5])][key] * 60, 1))
			getattr(parent, f'{value}').setText(f'{vel}')
		else:
			getattr(parent, f'{value}').setText(f'{getattr(parent, "status").axis[int(value[-4])][key[0:-2]]}')

	if parent.findChild(QLabel, 'gcodes_lb'):
		g_codes = []
		for i in parent.status.gcodes[1:]:
			if i == -1: continue
			if i % 10 == 0:
				g_codes.append(f'G{(i/10):.0f}')
			else:
				g_codes.append(f'G{(i/10):.0f}.{i%10}')
		parent.gcodes_lb.setText(f'{" ".join(g_codes)}')


	if parent.findChild(QLabel, 'mcodes_lb'):
		m_codes = []
		for i in parent.status.mcodes[1:]:
			if i == -1: continue
			m_codes.append(f'M{i}')
		parent.mcodes_lb.setText(f'{" ".join(m_codes)}')

	# update gcode_pte
	if parent.gcode_pte_exists:
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

	# i/o s.ain[0] FIXME precision
	for key, value in parent.status_io.items(): # up to 64 items
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
	if parent.status.state == linuxcnc.STATE_ESTOP:
		pass

