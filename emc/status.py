import math, statistics

from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor, QAction
from PyQt6.QtWidgets import QLCDNumber, QAbstractSpinBox, QCheckBox, QSlider

import linuxcnc as emc
import hal

from libflexgui import utilities
from libflexgui import dialogs

EXEC_STATES = {1: 'EXEC_ERROR', 2: 'EXEC_DONE', 3: 'EXEC_WAITING_FOR_MOTION',
	4: 'EXEC_WAITING_FOR_MOTION_QUEUE', 5: 'EXEC_WAITING_FOR_IO',
	7: 'EXEC_WAITING_FOR_MOTION_AND_IO', 8: 'EXEC_WAITING_FOR_DELAY',
	9: 'EXEC_WAITING_FOR_SYSTEM_CMD', 10: 'EXEC_WAITING_FOR_SPINDLE_ORIENTED', }

INTERP_STATES = {1: 'INTERP_IDLE', 2: 'INTERP_READING', 3: 'INTERP_PAUSED',
	4: 'INTERP_WAITING'}

INTERPRETER_ERRCODES = {0: 'INTERP_OK', 1: 'INTERP_EXIT',
	2: 'INTERP_EXECUTE_FINISH', 3 :'INTERP_ENDFILE', 4 :'INTERP_FILE_NOT_OPEN',
	5 :'INTERP_ERROR'}

MOTION_MODES = {1: 'TRAJ_MODE_FREE', 2: 'TRAJ_MODE_COORD', 3: 'TRAJ_MODE_TELEOP'}

MOTION_TYPES = {0: 'MOTION_TYPE_NONE', 1: 'MOTION_TYPE_TRAVERSE',
	2: 'MOTION_TYPE_FEED', 3: 'MOTION_TYPE_ARC', 4: 'MOTION_TYPE_TOOLCHANGE',
	5: 'MOTION_TYPE_PROBING', 6: 'MOTION_TYPE_INDEXROTARY'}

STATES = {1: 'RCS_DONE', 2: 'RCS_EXEC', 3: 'RCS_ERROR'}

TASK_MODES = {1: 'MODE_MANUAL', 2: 'MODE_AUTO', 3: 'MODE_MDI'}

TASK_STATES = {1: 'STATE_ESTOP', 2: 'STATE_ESTOP_RESET', 3: 'STATE_OFF',
	4: 'STATE_ON'}

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
	changed = False
	# **** EXEC STATE ****
	# exec_state EXEC_ERROR, EXEC_DONE, EXEC_WAITING_FOR_MOTION,
	# EXEC_WAITING_FOR_MOTION_QUEUE, EXEC_WAITING_FOR_IO,
	# EXEC_WAITING_FOR_MOTION_AND_IO, EXEC_WAITING_FOR_DELAY,
	# EXEC_WAITING_FOR_SYSTEM_CMD, EXEC_WAITING_FOR_SPINDLE_ORIENTED.
	if parent.exec_state != parent.status.exec_state:
		print(f'EXEC STATE: {EXEC_STATES[parent.status.exec_state]}')
		changed = True
		if 'exec_state_lb' in parent.child_names: # update the label
			parent.exec_state_lb.setText(EXEC_STATES[parent.status.exec_state])

		parent.exec_state = parent.status.exec_state

	# **** INTERP STATE ****
	# interp_state INTERP_IDLE, INTERP_READING, INTERP_PAUSED, INTERP_WAITING
	if parent.interp_state != parent.status.interp_state:
		print(f'INTERP STATE: {INTERP_STATES[parent.status.interp_state]}')
		changed = True
		if 'interp_state_lb' in parent.child_names: # update the label
			parent.interp_state_lb.setText(INTERP_STATES[parent.status.interp_state])

		parent.interp_state = parent.status.interp_state

	# **** INTERPRETER ERRCODE ****
	# interpreter_errcode INTERP_OK INTERP_EXIT INTERP_EXECUTE_FINISH
	# INTERP_ENDFILE INTERP_FILE_NOT_OPEN INTERP_ERROR
	if parent.interpreter_errcode != parent.status.interpreter_errcode:
		print(f'INTERPRETER ERRCODE: {INTERPRETER_ERRCODES[parent.status.interpreter_errcode]}')
		changed = True
		if 'interpreter_errcode_lb' in parent.child_names: # update the label
			parent.interpreter_errcode_lb.setText(INTERPRETER_ERRCODES[parent.status.interpreter_errcode])

		parent.interpreter_errcode = parent.status.interpreter_errcode

	# **** MOTION MODE ****
	# motion_mode TRAJ_MODE_COORD, TRAJ_MODE_FREE, TRAJ_MODE_TELEOP
	if parent.motion_mode != parent.status.motion_mode:
		print(f'MOTION MODE: {MOTION_MODES[parent.status.motion_mode]}')
		changed = True
		if 'motion_mode_lb' in parent.child_names: # update the label
			parent.motion_mode_lb.setText(MOTION_MODES[parent.status.motion_mode])

		parent.motion_mode = parent.status.motion_mode

	# **** MOTION TYPE ****
	if parent.motion_type != parent.status.motion_type:
		print(f'MOTION TYPE: {MOTION_TYPES[parent.status.motion_type]}')
		changed = True
		if 'motion_type_lb' in parent.child_names: # update the label
			parent.motion_type_lb.setText(MOTION_TYPES[parent.status.motion_type])

		parent.motion_type = parent.status.motion_type

	# **** STATE ****
	# state RCS_DONE, RCS_EXEC, RCS_ERROR
	if parent.state != parent.status.state:
		print(f'STATE: {STATES[parent.status.state]}')
		changed = True
		if 'state_lb' in parent.child_names: # update the label
			parent.state_lb.setText(STATES[parent.status.state])

		parent.state = parent.status.state

	# **** TASK MODE ****
	# task_mode MODE_MDI, MODE_AUTO, MODE_MANUAL
	if parent.task_mode != parent.status.task_mode:
		print(f'TASK MODE: {TASK_MODES[parent.status.task_mode]}')
		changed = True
		if 'task_mode_lb' in parent.child_names: # update the label
			parent.task_mode_lb.setText(TASK_MODES[parent.status.task_mode])

		parent.task_mode = parent.status.task_mode


	# **** TASK STATE ****
	# task_state STATE_ESTOP, STATE_ESTOP_RESET, STATE_ON, STATE_OFF
	if parent.task_state != parent.status.task_state:
		print(f'TASK STATE: {TASK_STATES[parent.status.task_state]}')
		changed = True
		if 'task_state_lb' in parent.child_names: # update the label
			parent.task_state_lb.setText(TASK_STATES[parent.status.task_state])

		parent.task_state = parent.status.task_state

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
		elif error_type == 'Error':
			if 'errors_pte' in parent.child_names:
				parent.errors_pte.appendPlainText(error_type)
				parent.errors_pte.appendPlainText(text)
				parent.errors_pte.setFocus()
				if 'statusbar' in parent.child_names:
					parent.statusbar.showMessage('Error', 10000)
			if parent.status.task_mode ==  emc.MODE_MDI:
				utilities.update_mdi(parent)

	if changed:
		print('End of changes\n')
		changed = False

