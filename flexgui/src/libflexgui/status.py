
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

	# task_state STATE_ESTOP, STATE_ESTOP_RESET, STATE_ON, STATE_OFF
	if parent.task_state != parent.status.task_state:

		# e stop open
		if parent.status.task_state == emc.STATE_ESTOP:
			print('STATE_ESTOP')
			for key, value in parent.state_estop.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_estop_names.items():
				getattr(parent, key).setText(value)

		# e stop closed power off
		if parent.status.task_state == emc.STATE_ESTOP_RESET:
			print('STATE_ESTOP_RESET')
			for key, value in parent.state_estop_reset.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_estop_reset_names.items():
				getattr(parent, key).setText(value)

		# e stop closed power on
		if parent.status.task_state == emc.STATE_ON:
			print('STATE_ON')
			for key, value in parent.state_on.items():
				getattr(parent, key).setEnabled(value)
			for key, value in parent.state_on_names.items():
				getattr(parent, key).setText(value)

			if utilities.all_homed(parent):
				print('ALL HOMED')
				for item in parent.all_homed:
					getattr(parent, item).setEnabled(True)
				for item in parent.not_homed:
					getattr(parent, item).setEnabled(False)
			else:
				print('NOT HOMED')
				for item in parent.not_homed:
					getattr(parent, item).setEnabled(True)
				for item in parent.all_homed:
					getattr(parent, item).setEnabled(False)

			if parent.status.file:
				print('FILE LOADED')
				for item in parent.file_edit_items:
					getattr(parent, item).setEnabled(True)
			else:
				print('NO FILE LOADED')
				for item in parent.file_edit_items:
					getattr(parent, item).setEnabled(False)

		parent.task_state = parent.status.task_state

	# interp_state INTERP_IDLE, INTERP_READING, INTERP_PAUSED, INTERP_WAITING
	if parent.interp_state != parent.status.interp_state:
		if parent.status.task_mode == emc.MODE_AUTO:
			# program is running
			if parent.status.interp_state == emc.INTERP_WAITING:
				print('MODE_AUTO INTERP_WAITING')
				for key, value in parent.program_running.items():
					getattr(parent, key).setEnabled(value)

			# program is paused
			if parent.status.interp_state == emc.INTERP_PAUSED:
				print('MODE_AUTO INTERP_PAUSED')
				for key, value in parent.program_paused.items():
					getattr(parent, key).setEnabled(value)

		if parent.status.task_mode == emc.MODE_MDI:
			# mdi is running
			if parent.status.interp_state == emc.INTERP_READING:
				print('MODE_MDI INTERP_READING')

			# mdi is done
			if parent.status.interp_state == emc.INTERP_IDLE:
				print('MODE_MDI INTERP_IDLE')

		parent.interp_state = parent.status.interp_state

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

	# override items label : status item
	for label, stat in parent.overrides.items():
		getattr(parent, label).setText(f'{getattr(parent.status, f"{stat}") * 100:.0f}%')

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

	# spindle override
	for key, value in parent.status_spindle_overrides.items():
		key = key[0:-2]
		getattr(parent, f'{value}').setText(f'{getattr(parent, "status").spindle[int(value[-4])][key] * 100:.0f}%')

	# tool table s.tool_table[0].id
	for key, value in parent.tool_table.items():
		tool = int(key.split('_')[-1])
		key = key.split('_')[0] # get the status name from key xoffset_0
		tr = getattr(parent.status, 'tool_table')[tool]
		getattr(parent, f'{value}').setText(f'{getattr(tr, key)}')

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

