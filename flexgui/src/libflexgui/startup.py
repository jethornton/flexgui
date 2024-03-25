import os, shutil
from functools import partial

from PyQt6.QtWidgets import QLabel, QPushButton, QListWidget, QPlainTextEdit
from PyQt6.QtWidgets import QComboBox, QSlider, QMenu, QToolButton, QWidget
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSettings

import linuxcnc, hal

from libflexgui import actions
from libflexgui import commands
from libflexgui import dialogs
from libflexgui import utilities

AXES = ['x', 'y', 'z', 'a', 'b', 'c', 'u', 'v', 'w']

def find_children(parent): # get the object names of all widgets
	parent.children = []
	children = parent.findChildren(QWidget)
	for child in children:
		if child.objectName():
			parent.children.append(child.objectName())
	actions = parent.findChildren(QAction)
	for action in actions:
		if action.objectName():
			parent.children.append(action.objectName())
	menus = parent.findChildren(QMenu)
	for menu in menus:
		if menu.objectName():
			parent.children.append(menu.objectName())

def get_ini_values(parent):
	units = parent.inifile.find('TRAJ', 'LINEAR_UNITS') or False
	if units == 'inch':
		parent.units = 'in'
	else:
		parent.units = 'mm'

def setup_enables(parent):
	# these are always disabled at start up
	for item in ['actionPause', 'pause_pb', 'actionResume', 'resume_pb']:
		if item in parent.children:
			getattr(parent, item).setEnabled(False)

	# STATE_ESTOP items that should be disabled
	estop_open = ['power_pb', 'run_pb', 'run_from_line_pb', 'step_pb',
		'pause_pb', 'resume_pb', 'home_all_pb', 'unhome_all_pb', 'run_mdi_pb',
		'spindle_start_pb', 'spindle_fwd_pb', 'spindle_rev_pb', 'spindle_stop_pb',
		'spindle_plus_pb', 'spindle_minus_pb', 'flood_pb', 'mist_pb', 'actionPower',
		'actionRun', 'actionRun_From_Line', 'actionStep', 'actionPause',
		'actionResume']
	for item in ['home_pb_', 'unhome_pb_']:
		for i in range(9):
			estop_open.append(f'{item}{i}')
	for item in AXES:
		estop_open.append(f'jog_plus_pb_{item}')
		estop_open.append(f'jog_minus_pb_{item}')

	parent.state_estop_open = []
	for item in estop_open:
		if item in parent.children:
			parent.state_estop_open.append(item)

	# STATE_ESTOP_RESET enable power
	parent.state_estop_closed = []
	for item in ['power_pb', 'actionPower']:
		if item in parent.children:
			parent.state_estop_closed.append(item)

	# STATE_ON home, jog, spindle
	power_on = ['spindle_start_pb', 'spindle_fwd_pb', 'spindle_rev_pb',
	'spindle_stop_pb', 'spindle_plus_pb', 'spindle_minus_pb', 'flood_pb',
	'mist_pb']
	for i in range(9):
		power_on.append(f'home_pb_{i}')
	for item in AXES:
		power_on.append(f'jog_plus_pb_{item}')
		power_on.append(f'jog_minus_pb_{item}')

	parent.state_power_on = []
	for item in power_on:
		if item in parent.children:
			parent.state_power_on.append(item)

	# all homed
	all_homed = ['run_mdi_pb', 'unhome_all_pb']
	for i in range(9):
		all_homed.append(f'unhome_pb_{i}')
	parent.state_all_homed = []
	for item in  all_homed:
		if item in parent.children:
			parent.state_all_homed.append(item)

	# file loaded
	file_items = ['actionEdit', 'edit_pb', 'actionSave_As', 'save_as_pb',
		'actionReload', 'reload_pb']
	parent.file_loaded = []
	for item in file_items:
		if item in parent.children:
			parent.file_loaded.append(item)

	# run controls
	run = [ 'run_pb', 'run_from_line_pb', 'step_pb',
	'actionReload', 'actionRun', 'actionRun_From_Line', 'actionStep']
	parent.run_controls = []
	for item in run:
		if item in parent.children:
			parent.run_controls.append(item)

	# program running
	parent.program_running = []
	for item in ['pause_pb', 'actionPause']:
		if item in parent.children:
			parent.program_running.append(item)

	# program paused
	parent.program_paused = []
	for item in ['resume_pb', 'actionResume']:
		if item in parent.children:
			parent.program_paused.append(item)

	# unhome buttons
	unhome = ['unhome_all_pb']
	for i in range(9):
		unhome.append(f'unhome_pb_{i}')
	parent.unhome_controls = []
	for item in unhome:
		if item in parent.children:
			parent.unhome_controls.append(item)

	parent.status.poll()
	# STATE_ESTOP
	if parent.status.task_state == linuxcnc.STATE_ESTOP:
		for item in parent.state_estop_open:
			getattr(parent, item).setEnabled(False)
		# update button and action text
		for item in ['estop_pb', 'actionE_Stop']:
			if item in parent.children:
				getattr(parent, item).setText('E Stop\nOpen')
		for item in ['power_pb', 'actionPower']:
			if item in parent.children:
				getattr(parent, item).setText('Power\nOff')

	# STATE_ESTOP_RESET
	if parent.status.task_state == linuxcnc.STATE_ESTOP_RESET:
		for item in parent.state_estop_open:
			getattr(parent, item).setEnabled(False)
		for item in parent.state_estop_closed:
			getattr(parent, item).setEnabled(True)
		# update button and action text
		for item in ['estop_pb', 'actionE_Stop']:
			if item in parent.children:
				getattr(parent, item).setText('E Stop\nClosed')
		for item in ['power_pb', 'actionPower']:
			if item in parent.children:
				getattr(parent, item).setText('Power\nOff')

	# STATE_ON
	if parent.status.task_state == linuxcnc.STATE_ON:
		for item in parent.state_power_on:
			getattr(parent, item).setEnabled(True)

		# update button and action text
		for item in ['estop_pb', 'actionE_Stop']:
			if item in parent.children:
				getattr(parent, item).setText('E Stop\nClosed')
		for item in ['power_pb', 'actionPower']:
			if item in parent.children:
				getattr(parent, item).setText('Power\nOn')

			if utilities.all_homed(parent):
				for item in parent.state_all_homed:
					getattr(parent, item).setEnabled(True)
			else:
				for item in parent.unhome_controls:
					getattr(parent, item).setEnabled(False)
				for item in parent.run_controls:
					getattr(parent, item).setEnabled(False)

		# if a file is loaded and machine is homed enable run and step
			if parent.status.file and utilities.all_homed(parent):
				for item in parent.run_controls:
					getattr(parent, item).setEnabled(True)

		# home all push button
		if 'home_all_pb' in parent.children:
			if utilities.home_all_check(parent):
				parent.home_all_pb.setEnabled(True)
			else:
				parent.home_all_pb.setEnabled(False)

	# if a file is loaded
	if parent.status.file:
		text = open(parent.status.file).read()
		if 'gcode_pte' in parent.children:
			parent.gcode_pte.setPlainText(text)
		for item in parent.file_loaded:
			getattr(parent, item).setEnabled(True)
	else: # no file is loaded
		for item in parent.file_loaded:
			getattr(parent, item).setEnabled(False)

	# check for required items tool_touchoff_ touchoff_pb_
	to_missing = False
	tto_missing = False
	for item in AXES:
		if f'touchoff_pb_{item}' in parent.children:
			if 'touchoff_dsb' not in parent.children:
				getattr(parent, f'touchoff_pb_{item}').setEnabled(False)
				to_missing = True

		if f'tool_touchoff_{item}' in parent.children:
			if 'tool_touchoff_dsb' not in parent.children:
				getattr(parent, f'tool_touchoff_{item}').setEnabled(False)
				tto_missing = True

	if to_missing:
		msg = ('Touch Off Double Spin Box\n'
			'touchoff_dsb not found.\n'
			'Touch Off Buttons will be disabled')
		dialogs.warn_msg_ok(msg, 'Required Item Missing')

	if tto_missing:
		msg = ('Touch Off Double Spin Box\n'
			'tool_touchoff_dsb not found.\n'
			'Tool Touch Off Buttons will be disabled')
		dialogs.warn_msg_ok(msg, 'Required Item Missing')

	if 'run_mdi_pb' in parent.children:
		if 'mdi_command_le' not in parent.children:
			parent.run_mdi_pb.setEnabled(False)
			msg = ('Run MDI can not work without\n'
				'the Line Edit mdi_command_le.\n'
				'The Run MDI Button will be disabled')
			dialogs.warn_msg_ok(msg, 'Required Item Missing')

def setup_buttons(parent): # connect buttons to functions
	command_buttons = {
	'abort_pb': 'abort',
	'manual_mode_pb':'set_mode_manual',
	'home_all_pb': 'home_all',
	'home_pb_0': 'home',
	'home_pb_1': 'home',
	'home_pb_2': 'home',
	'unhome_all_pb': 'unhome_all',
	'unhome_pb_0': 'unhome',
	'unhome_pb_1': 'unhome',
	'unhome_pb_2': 'unhome',
	'run_mdi_pb': 'run_mdi',
	'tool_change_pb':  'tool_change',
	'spindle_fwd_pb': 'spindle',
	'spindle_rev_pb': 'spindle',
	'spindle_stop_pb': 'spindle',
	'spindle_plus_pb': 'spindle',
	'spindle_minus_pb': 'spindle',
	'flood_pb': 'flood_toggle',
	'mist_pb': 'mist_toggle',
	}

	for item in AXES:
		command_buttons[f'touchoff_pb_{item}'] = 'touchoff'
		command_buttons[f'tool_touchoff_{item}'] = 'tool_touchoff'
	for key, value in command_buttons.items():
		if key in parent.children:
			getattr(parent, key).clicked.connect(partial(getattr(commands, value), parent))

	action_buttons = {
	'estop_pb': 'action_estop',
	'power_pb': 'action_power',
	'run_pb': 'action_run',
	'run_from_line_pb': 'action_run_from_line',
	'step_pb': 'action_step',
	'pause_pb': 'action_pause',
	'resume_pb': 'action_resume',
	'stop_pb': 'action_stop',
	'open_pb': 'action_open',
	'edit_pb': 'action_edit',
	'reload_pb': 'action_reload',
	'save_as_pb': 'action_save_as',
	'quit_pb': 'action_quit',
	'copy_mdi_history_pb': 'action_copy_mdi',
	'clear_mdi_history_pb': 'action_clear_mdi'
	}
	for key, value in action_buttons.items():
		if key in parent.children:
			getattr(parent, key).clicked.connect(partial(getattr(actions, value), parent))

	if 'clear_error_history_pb' in parent.children:
		if 'errors_pte' in parent.children:
			parent.clear_error_history_pb.clicked.connect(partial(utilities.clear_errors, parent))
	

def setup_actions(parent): # setup menu actions
	actions_dict = {'actionOpen': 'action_open', 'actionEdit': 'action_edit',
		'actionReload': 'action_reload', 'actionSave_As': 'action_save_as',
		'actionEdit_Tool_Table': 'action_edit_tool_table',
		'actionReload_Tool_Table': 'action_reload_tool_table',
		'actionLadder_Editor': 'action_ladder_editor', 'actionQuit': 'action_quit',
		'actionE_Stop': 'action_estop', 'actionPower': 'action_power',
		'actionRun': 'action_run', 
		'actionRun_From_Line': 'action_run_from_line', 'actionStep': 'action_step',
		'actionPause': 'action_pause', 'actionResume': 'action_resume',
		'actionStop': 'action_stop', 'actionClear_MDI_History': 'action_clear_mdi',
		'actionCopy_MDI_History': 'action_copy_mdi',
		'actionShow_HAL': 'action_show_hal', 'actionHAL_Meter': 'action_hal_meter',
		'actionHAL_Scope': 'action_hal_scope', 'actionAbout': 'action_about',
		'actionQuick_Reference': 'action_quick_reference'}

	# if an action is found connect it to the function
	for key, value in actions_dict.items():
		if parent.findChild(QAction, f'{key}'):
			if key == 'action_Power':
				print('etc')
			getattr(parent, f'{key}').triggered.connect(partial(getattr(actions, f'{value}'), parent))

	# special check for the classicladder editor
	if parent.findChild(QAction, 'actionLadder_Editor'):
		if not hal.component_exists("classicladder_rt"):
			parent.actionLadder_Editor.setEnabled(False)

	# special check for MDI
	if parent.findChild(QListWidget, 'mdi_history_lw') is None:
		if parent.findChild(QAction, 'actionClear_MDI_History'):
			parent.actionClear_MDI_History.setEnabled(False)
		if parent.findChild(QAction, 'actionCopy_MDI_History'):
			parent.actionCopy_MDI_History.setEnabled(False)

def setup_status_labels(parent):
	parent.stat_dict = {'adaptive_feed_enabled': {0: False, 1: True},
	'motion_mode': {1: 'TRAJ_MODE_FREE', 2: 'TRAJ_MODE_COORD', 3: 'TRAJ_MODE_TELEOP'},
	'exec_state': {1: 'EXEC_ERROR', 2: 'EXEC_DONE', 3: 'EXEC_WAITING_FOR_MOTION',
		4: 'EXEC_WAITING_FOR_MOTION_QUEUE', 5: 'EXEC_WAITING_FOR_IO',
		7: 'EXEC_WAITING_FOR_MOTION_AND_IO', 8: 'EXEC_WAITING_FOR_DELAY',
		9: 'EXEC_WAITING_FOR_SYSTEM_CMD', 10: 'EXEC_WAITING_FOR_SPINDLE_ORIENTED',},
	'estop': {0: False, 1: True},
	'flood': {0: 'FLOOD_OFF', 1: 'FLOOD_ON'},
	'g5x_index': {1: 'G54', 2: 'G55', 3: 'G56', 4: 'G57', 5: 'G58', 6: 'G59',
		7: 'G59.1', 8: 'G59.2', 9: 'G59.3'},
	'interp_state': {1: 'INTERP_IDLE', 2: 'INTERP_READING',
		3: 'INTERP_PAUSED', 4: 'INTERP_WAITING'},
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

	status_items = ['acceleration', 'active_queue', 
	'adaptive_feed_enabled', 'angular_units', 'axes', 'axis',
	'axis_mask', 'block_delete', 'call_level', 'command', 'current_line',
	'current_vel', 'cycle_time', 'debug', 'delay_left', 'distance_to_go',
	'echo_serial_number', 'enabled', 'estop', 'exec_state',
	'feed_hold_enabled', 'feed_override_enabled', 'feedrate', 'flood',
	'g5x_index', 'ini_filename', 'inpos', 'input_timeout', 'interp_state',
	'interpreter_errcode', 'joint', 'joints', 'kinematics_type', 'linear_units',
	'lube', 'lube_level', 'max_acceleration', 'max_velocity', 'mist',
	'motion_line', 'motion_mode', 'motion_type', 'optional_stop', 'paused',
	'pocket_prepped', 'probe_tripped', 'probe_val', 'probed_position', 'probing',
	'program_units', 'queue', 'queue_full', 'rapidrate', 'read_line',
	'rotation_xy', 'settings', 'spindle', 'spindles', 'state', 'task_mode',
	'task_paused', 'task_state', 'tool_in_spindle', 'tool_from_pocket',
	'tool_offset', 'tool_table', 'velocity']

	# check for status labels in the ui
	parent.status_labels = {} # create an empty dictionary
	for item in status_items: # iterate the status items list
		if f'{item}_lb' in parent.children: # if the label is found
			parent.status_labels[item] = f'{item}_lb' # add the status and label

	position_items = ['actual_lb_x', 'actual_lb_y', 'actual_lb_z', 'actual_lb_a',
		'actual_lb_b', 'actual_lb_c', 'actual_lb_u', 'actual_lb_v', 'actual_lb_w']
	parent.status_position = {} # create an empty dictionary
	# check for position labels in the ui
	for i, item in enumerate(position_items):
		if item in parent.children: # if the label is found
			p = getattr(parent, item).property('precision')
			p = p if p is not None else 3
			parent.status_position[f'{item}'] = [i, p] # add the label, tuple position & precision

	dro_items = ['dro_lb_x', 'dro_lb_y', 'dro_lb_z', 'dro_lb_a', 'dro_lb_b',
		'dro_lb_c', 'dro_lb_u', 'dro_lb_v', 'dro_lb_w']
	parent.status_dro = {} # create an empty dictionary
	# check for dro labels in the ui
	for i, item in enumerate(dro_items):
		if item in parent.children: # if the label is found
			p = getattr(parent, item).property('precision')
			p = p if p is not None else 3
			parent.status_dro[f'{item}'] = [i, p] # add the label, tuple position & precision

	g5x_items = ['g5x_lb_x', 'g5x_lb_y', 'g5x_lb_z', 'g5x_lb_a', 'g5x_lb_b',
		'g5x_lb_c', 'g5x_lb_u', 'g5x_lb_v', 'g5x_lb_w']
	parent.status_g5x = {} # create an empty dictionary
	# check for g5x offset labels in the ui
	for i, item in enumerate(g5x_items):
		if item in parent.children: # if the label is found
			p = getattr(parent, item).property('precision')
			p = p if p is not None else 3
			parent.status_g5x[f'{item}'] = [i, p] # add the label, tuple position & precision

	g92_items = ['g92_lb_x', 'g92_lb_y', 'g92_lb_z', 'g92_lb_a', 'g92_lb_b',
		'g92_lb_c', 'g92_lb_u', 'g92_lb_v', 'g92_lb_w']
	parent.status_g92 = {} # create an empty dictionary
	# check for g5x offset labels in the ui
	for i, item in enumerate(g92_items):
		if item in parent.children: # if the label is found
			p = getattr(parent, item).property('precision')
			p = p if p is not None else 3
			parent.status_g92[f'{item}'] = [i, p] # add the label, tuple position & precision

	tool_offset_items = ['tool_offset_lb_0', 'tool_offset_lb_1',
		'tool_offset_lb_2', 'tool_offset_lb_3', 'tool_offset_lb_4',
		'tool_offset_lb_5', 'tool_offset_lb_6', 'tool_offset_lb_7',
		'tool_offset_lb_8']
	parent.status_tool_offset = {} # create an empty dictionary
	# check for tool offset labels in the ui
	for i, item in enumerate(tool_offset_items):
		if item in parent.children: # if the label is found
			p = getattr(parent, item).property('precision')
			p = p if p is not None else 3
			parent.status_tool_offset[f'{item}'] = [i, p] # add the label, tuple position & precision

	# check for axis labels in the ui FIXME precision velocity
	# these return tuples of xyzabcuvw axes
	axis_items = ['max_position_limit', 'min_position_limit', 'velocity']
	parent.status_axes = {} # create an empty dictionary
	parent.status.poll()
	for i in range(parent.status.axis_mask.bit_count()): # only check for axes that exist
		for item in axis_items:
			if f'axis_{item}_{i}_lb' in parent.children: # if the label is found
				parent.status_axes[f'{item}_{i}'] = f'axis_{item}_{i}_lb' # add the status and label

	# check for joint labels in ui
	# these return 16 joints
	joint_items = ['backlash', 'enabled', 'fault', 'ferror_current',
	'ferror_highmark', 'homed', 'homing', 'inpos', 'input', 'jointType',
	'max_ferror', 'max_hard_limit', 'max_position_limit', 'max_soft_limit',
	'min_ferror', 'min_hard_limit', 'min_position_limit', 'min_soft_limit',
	'output', 'override_limits']
	parent.status_joints = {} # create an empty dictionary
	for i in range(16):
		for item in joint_items:
			if f'joint_{item}_{i}_lb' in parent.children:
				parent.status_joints[f'{item}_{i}'] = f'joint_{item}_{i}_lb'

	joint_number_items = ['units', 'velocity']
	parent.status_joint_prec = {}
	for i in range(16):
		for item in joint_number_items:
			if f'joint_{item}_{i}_lb' in parent.children: # if the label is found
				p = getattr(parent, f'joint_{item}_{i}_lb').property('precision')
				p = p if p is not None else 3
				parent.status_joint_prec[f'{item}_{i}'] = [i, p] # add the label, tuple position & precision

	# check for analog and digital labels in ui
	# these return 64 items each
	io_items = ['ain', 'aout', 'din', 'dout']
	parent.status_io = {}
	for i in range(64):
		for item in io_items:
			if f'{item}_{i}_lb' in parent.children:
				parent.status_io[f'{item}_{i}'] = f'{item}_{i}_lb'

	# check for spindle labels in the ui
	spindle_items = ['brake', 'direction', 'enabled', 'homed',
	'orient_fault', 'orient_state', 'override', 'override_enabled', 'speed']
	parent.status_spindles = {}
	parent.status.poll()
	 # only look for the num of spindles configured
	for i in range(parent.status.spindles):
		for item in spindle_items:
			if f'spindle_{item}_{i}_lb' in parent.children:
				parent.status_spindles[f'{item}_{i}'] = f'spindle_{item}_{i}_lb'

	# check for tool table labels in the ui
	tool_table_items = ['id', 'xoffset', 'yoffset', 'zoffset', 'aoffset',
		'boffset', 'coffset', 'uoffset', 'voffset', 'woffset', 'diameter',
		'frontangle', 'backangle', 'orientation']
	parent.tool_table = {}
	parent.status.poll()
	for i in range(len(parent.status.tool_table)):
		for item in tool_table_items:
			if f'tool_table_{item}_{i}_lb' in parent.children:
				parent.tool_table[f'{item}_{i}'] = f'tool_table_{item}_{i}_lb'

	if 'file_lb' in parent.children:
		parent.status.poll()
		gcode_file = parent.status.file or False
		if gcode_file:
			parent.file_lb.setText(os.path.basename(gcode_file))
		else:
			parent.file_lb.setText('No G code file loaded')

def setup_spin_boxes(parent):
	if 'spindle_speed_sb' in parent.children:
		parent.spindle_speed_sb.valueChanged.connect(partial(utilities.spindle_speed, parent))
		parent.spindle_speed_sb.setValue(parent.spindle_speed)

def setup_plain_text_edits(parent):
	# for gcode_pte update
	if 'gcode_pte' in parent.children:
		parent.status.poll()
		parent.last_line = parent.status.motion_line

def setup_list_widgets(parent):
	list_widgets = ['mdi_history_lw']
	for item in list_widgets:
		if parent.findChild(QListWidget, item) is not None:
			setattr(parent, f'{item}_exists', True)
		else:
			setattr(parent, f'{item}_exists', False)

def load_postgui(parent): # load post gui hal and tcl files if found
	postgui_halfiles = parent.inifile.findall("HAL", "POSTGUI_HALFILE") or None
	if postgui_halfiles is not None:
		for f in postgui_halfiles:
			if f.lower().endswith('.tcl'):
				res = os.spawnvp(os.P_WAIT, "haltcl", ["haltcl", "-i", parent.ini_path, f])
			else:
				res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", parent.ini_path, "-f", f])
			if res: raise SystemExit(res)

def setup_mdi(parent):
	if 'mdi_history_lw' in parent.children:
		path = os.path.dirname(parent.status.ini_filename)
		mdi_file = os.path.join(path, 'mdi_history.txt')
		if os.path.exists(mdi_file): # load mdi history
			with open(mdi_file, 'r') as f:
				history_list = f.readlines()
				for item in history_list:
					parent.mdi_history_lw.addItem(item.strip())
		parent.mdi_history_lw.itemSelectionChanged.connect(partial(utilities.add_mdi, parent))
		if 'mdi_command_le' in parent.children:
			parent.mdi_command_le.returnPressed.connect(partial(commands.run_mdi, parent))

def setup_recent_files(parent):
	parent.menuRecent = QMenu('Recent', parent)
	# add the Recent menu FIXME look for file open then add before next action
	action = parent.findChild(QAction, 'actionEdit') or False
	if action:
		parent.menuFile.insertMenu(action, parent.menuRecent)

		# if any files have been opened add them
		keys = parent.settings.allKeys()
		for key in keys:
			if key.startswith('recent_files'):
				path = parent.settings.value(key)
				name = os.path.basename(path)
				a = parent.menuRecent.addAction(name)
				a.triggered.connect(partial(getattr(actions, 'load_file'), parent, path))

def setup_jog(parent):
	jog_buttons = {}
	required_jog_items = ['jog_vel_s', 'jog_modes_cb']
	jog_buttons = []
	for i in range(16):
		jog_buttons.append(f'jog_plus_pb_{i}')
		jog_buttons.append(f'jog_minus_pb_{i}')
	jog_items_found = []
	for item in jog_buttons:
		if item in parent.children: # check for jog required items before connecting
			jog_items_found.append(item)
	if len(jog_items_found) > 0:
		for item in required_jog_items:
			# don't make the connection if all required widgets are not present
			if item not in parent.children:
				msg = (f'{item} is required to jog\n but was not found.\n'
					'Jog Buttons will be disabled.')
				dialogs.warn_msg_ok(msg, 'Missing Item')
				for item in jog_items_found:
					getattr(parent, item).setEnabled(False)
				return
		# ok to connect if we get this far
		for item in jog_items_found: # connect jog buttons
			getattr(parent, item).pressed.connect(partial(getattr(commands, 'jog'), parent))
			getattr(parent, item).released.connect(partial(getattr(commands, 'jog'), parent))

		max_vel = parent.inifile.find('DISPLAY', 'MAX_LINEAR_VELOCITY') or False
		if max_vel:
			parent.jog_vel_s.setMaximum(int(float(max_vel) * 60))

		default_vel = parent.inifile.find('DISPLAY', 'DEFAULT_LINEAR_VELOCITY') or False
		if default_vel:
			parent.jog_vel_s.setValue(int(float(default_vel) * 60))

		if 'jog_vel_lb' in parent.children:
			parent.jog_vel_s.valueChanged.connect(partial(utilities.update_jog_lb, parent))
			parent.jog_vel_lb.setText(f'{parent.jog_vel_s.value()}')
			utilities.update_jog_lb(parent)

		parent.jog_modes_cb.addItem('Continuous', False)
		increments = parent.inifile.find('DISPLAY', 'INCREMENTS') or False
		# INCREMENTS = 1 in, 0.1 in, 10 mil, 1 mil, 1mm, .1mm, 1/8000 in
		if increments:
			for item in increments.split():
				data = ''
				for char in item:
					if char.isdigit() or char == '.':
						data += char
				parent.jog_modes_cb.addItem(item, float(data))

def setup_spindle(parent):
	parent.spindle_speed = 100

	if 'spindle_speed_sb' in parent.children:
		min_rpm = int(parent.inifile.find('SPINDLE_0', 'MIN_FORWARD_VELOCITY')) or 0
		max_rpm = int(parent.inifile.find('SPINDLE_0', 'MAX_FORWARD_VELOCITY')) or 1000
		increment = int(parent.inifile.find('SPINDLE_0', 'INCREMENT')) or False
		if not increment:
			increment = int(parent.inifile.find('DISPLAY', 'SPINDLE_INCREMENT')) or 100
		parent.spindle_speed_sb.setMinimum(min_rpm)
		parent.spindle_speed_sb.setMaximum(max_rpm)
		parent.spindle_speed_sb.setSingleStep(increment)

# FIXME Everything from here down needs to be looked at

def setup_hal_buttons(parent):
	for button in parent.findChildren(QPushButton):
		if button.property('function') == 'hal_pin':
			props = button.dynamicPropertyNames()
			for prop in props:
				prop = str(prop, 'utf-8')
				if prop.startswith('pin_'):
					pin_settings = button.property(prop).split(',')
					name = button.objectName()
					pin_name = pin_settings[0]
					pin_type = getattr(hal, f'{pin_settings[1].upper().strip()}')
					pin_dir = getattr(hal, f'{pin_settings[2].upper().strip()}')
					parent.halcomp = hal.component('jet')
					setattr(parent, f'{prop}', parent.halcomp.newpin(pin_name, pin_type, pin_dir))
					getattr(parent, f'{name}').toggled.connect(lambda:
						getattr(parent, f'{prop}').set(getattr(parent, f'{name}').isChecked()))

def copy_examples(parent, title=None):
	if parent.settings.contains('nags/copy_examples'):
		if parent.settings.value('nags/copy_examples') == 'no':
			return True
	if title is None:
		title = 'Example Files'
	configs_dir = os.path.join(os.path.expanduser('~'), 'linuxcnc', 'configs', 'flex_examples')
	if not os.path.isdir(configs_dir):
		msg = ('The example configuration directory\n'
			'was not found. Do you want to copy them to\n'
			f'{configs_dir}')
		response, check = dialogs.question_msg_yes_no_check(title, msg, 'Never Ask Again')
		if check:
			parent.settings.beginGroup("nags");
			parent.settings.setValue("copy_examples", 'no')
			parent.settings.endGroup()

		if response:
			source_dir = '/usr/lib/libflexgui/examples'
			dest_dir = os.path.join(os.path.expanduser('~'), 'linuxcnc', 'configs', 'flex_examples')
			if os.path.isdir(source_dir):
				shutil.copytree(source_dir, dest_dir)
	return True

