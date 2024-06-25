import os, shutil
from functools import partial

from PyQt6.QtWidgets import QPushButton, QListWidget, QPlainTextEdit
from PyQt6.QtWidgets import QComboBox, QSlider, QMenu, QToolButton, QWidget
from PyQt6.QtWidgets import QVBoxLayout, QAbstractButton
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSettings
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import linuxcnc, hal

from libflexgui import actions
from libflexgui import commands
from libflexgui import dialogs
from libflexgui import utilities
from libflexgui import flexplot

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
			widget_name = f'flex_{action.objectName()[6:].replace(" ", "_")}'
			# make sure the action is in the tool bar
			if parent.toolBar.widgetForAction(action) is not None:
				parent.toolBar.widgetForAction(action).setObjectName(widget_name)
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
	parent.home_required = [] # different functions add to this
	# disable home all if home sequence is not found
	if 'home_all_pb' in parent.children:
		if not utilities.home_all_check(parent):
			parent.home_all_pb.setEnabled(False)

	# STATE_ESTOP
	parent.state_estop = {'power_pb': False, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': False, 'pause_pb': False,
		'resume_pb': False, 'home_all_pb': False, 'unhome_all_pb': False,
		'run_mdi_pb': False, 'spindle_start_pb': False, 'spindle_fwd_pb': False,
		'spindle_rev_pb': False, 'spindle_stop_pb': False, 'spindle_plus_pb': False,
		'spindle_minus_pb': False, 'flood_pb': False, 'mist_pb': False,
		'actionPower': False, 'actionRun': False, 'actionRun_From_Line': False,
		'actionStep': False, 'actionPause': False, 'tool_change_pb': False,
		'actionResume': False}

	for i in range(9):
		parent.state_estop[f'home_pb_{i}'] = False
		parent.state_estop[f'unhome_pb_{i}'] = False
		parent.state_estop[f'jog_plus_pb_{i}'] = False
		parent.state_estop[f'jog_minus_pb_{i}'] = False
	for item in AXES:
		parent.state_estop[f'touchoff_pb_{item}'] = False
		parent.state_estop[f'tool_touchoff_{item}'] = False
	for i in range(100):
		parent.state_estop[f'tool_change_pb_{i}'] = False
	for i in range(1, 10):
		parent.state_estop[f'change_cs_{i}'] = False

	# remove any items not found in the gui
	for item in list(parent.state_estop):
		if item not in parent.children:
			del parent.state_estop[item]

	parent.state_estop_names = {'estop_pb': 'E Stop\nOpen',
		'actionE_Stop': 'E Stop\nOpen', 'power_pb': 'Power\nOff',
		'actionPower': 'Power\nOff'}

	# remove any items not found in the gui
	for item in list(parent.state_estop_names):
		if item not in parent.children:
			del parent.state_estop_names[item]

	# STATE_ESTOP_RESET enable power
	parent.state_estop_reset = {'power_pb': True, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': False, 'pause_pb': False,
		'resume_pb': False, 'home_all_pb': False, 'unhome_all_pb': False,
		'run_mdi_pb': False, 'spindle_start_pb': False, 'spindle_fwd_pb': False,
		'spindle_rev_pb': False, 'spindle_stop_pb': False, 'spindle_plus_pb': False,
		'spindle_minus_pb': False, 'flood_pb': False, 'mist_pb': False,
		'actionPower': True, 'actionRun': False, 'actionRun_From_Line': False,
		'actionStep': False, 'actionPause': False, 'tool_change_pb': False,
		'actionResume': False}

	for i in range(9):
		parent.state_estop_reset[f'home_pb_{i}'] = False
		parent.state_estop_reset[f'unhome_pb_{i}'] = False
		parent.state_estop_reset[f'jog_plus_pb_{i}'] = False
		parent.state_estop_reset[f'jog_minus_pb_{i}'] = False
	for item in AXES:
		parent.state_estop_reset[f'touchoff_pb_{item}'] = False
		parent.state_estop_reset[f'tool_touchoff_{item}'] = False
	for i in range(100):
		parent.state_estop_reset[f'tool_change_pb_{i}'] = False
	for i in range(1, 10):
		parent.state_estop_reset[f'change_cs_{i}'] = False

	# remove any items not found in the gui
	for item in list(parent.state_estop_reset):
		if item not in parent.children:
			del parent.state_estop_reset[item]

	parent.state_estop_reset_names = {'estop_pb': 'E Stop\nClosed',
		'actionE_Stop': 'E Stop\nClosed', 'power_pb': 'Power\nOff',
		'actionPower': 'Power\nOff'}

	# remove any items not found in the gui
	for item in list(parent.state_estop_reset_names):
		if item not in parent.children:
			del parent.state_estop_reset_names[item]

	# STATE_ON home, jog, spindle
	parent.state_on = {'power_pb': True, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': False, 'pause_pb': False,
		'resume_pb': False, 'spindle_start_pb': True, 'spindle_fwd_pb': True,
		'spindle_rev_pb': True, 'spindle_stop_pb': True, 'spindle_plus_pb': True,
		'spindle_minus_pb': True, 'flood_pb': True, 'mist_pb': True,
		'actionPower': True, 'actionRun': False, 'actionRun_From_Line': False,
		'actionStep': False, 'actionPause': False, 'actionResume': False}

	for i in range(9):
		parent.state_on[f'jog_plus_pb_{i}'] = True
		parent.state_on[f'jog_minus_pb_{i}'] = True

	# remove any items not found in the gui
	for item in list(parent.state_on):
		if item not in parent.children:
			del parent.state_on[item]

	parent.state_on_names = {'estop_pb': 'E Stop\nClosed',
		'actionE_Stop': 'E Stop\nClosed', 'power_pb': 'Power\nOn',
		'actionPower': 'Power\nOn'}

	# remove any items not found in the gui
	for item in list(parent.state_on_names):
		if item not in parent.children:
			del parent.state_on_names[item]

	# run controls used to enable/disable when not running a program
	run_items = ['run_pb', 'run_from_line_pb', 'step_pb', 'run_mdi_pb',
	'reload_pb', 'actionReload', 'actionRun', 'actionRun_From_Line', 'actionStep',
	'tool_change_pb', 'flood_pb', 'mist_pb']
	for i in range(100):
		run_items.append(f'tool_change_pb_{i}')
	for item in AXES: # FIXME this needs to bo in tool setup as well well maybe not...
		run_items.append(f'tool_touchoff_{item}')
		run_items.append(f'touchoff_pb_{item}')
	parent.run_controls = []
	for item in run_items:
		if item in parent.children:
			parent.run_controls.append(item)

	home_items = ['home_all_pb']
	for i in range(9):
		home_items.append(f'home_pb_{i}')
	parent.home_controls = []
	for item in home_items:
		if item in parent.children:
			parent.home_controls.append(item)

	unhome_items = ['unhome_all_pb']
	for i in range(9):
		unhome_items.append(f'unhome_pb_{i}')
	parent.unhome_controls = []
	for item in unhome_items:
		if item in parent.children:
			parent.unhome_controls.append(item)

	parent.program_running = {'run_mdi_pb': False, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': False, 'pause_pb': True,
		'resume_pb': False, 'reload_pb': False, 'actionReload': False,
		'home_all_pb': False, 'actionRun': False, 'actionRun_From_Line': False,
		'actionStep': False, 'actionPause': True, 'actionResume': False,
		'unhome_all_pb': False, 'spindle_start_pb': False, 'spindle_fwd_pb': False,
		'spindle_rev_pb': False, 'spindle_stop_pb': False, 'spindle_plus_pb': False,
		'spindle_minus_pb': False, 'tool_change_pb': False, 'flood_pb': False,
		'mist_pb': False}

	for i in range(9):
		parent.program_running[f'jog_plus_pb_{i}'] = False
		parent.program_running[f'jog_minus_pb_{i}'] = False
		parent.program_running[f'home_pb_{i}'] = False
		parent.program_running[f'unhome_pb_{i}'] = False
	for i in range(100):
		parent.program_running[f'tool_change_pb_{i}'] = False
	for i in range(1, 10):
		parent.program_running[f'change_cs_{i}'] = False
	for item in AXES:
		parent.program_running[f'touchoff_pb_{item}'] = False
		parent.program_running[f'tool_touchoff_{item}'] = False

	# remove any items not found in the gui
	for item in list(parent.program_running):
		if item not in parent.children:
			del parent.program_running[item]

	parent.program_paused = {'run_mdi_pb': False, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': True, 'pause_pb': False,
		'resume_pb': True, 'home_all_pb': False, 'unhome_all_pb': False,
		'actionRun': False, 'actionRun_From_Line': False, 'actionStep': True,
		'actionPause': False, 'actionResume': True, 'flood_pb': True,
		'mist_pb': True}
	for i in range(9):
		parent.program_paused[f'home_pb_{i}'] = False
		parent.program_paused[f'unhome_pb_{i}'] = False

	# remove any items not found in the gui
	for item in list(parent.program_paused):
		if item not in parent.children:
			del parent.program_paused[item]

	# file items if not loaded disable
	file_items = ['edit_pb', 'reload_pb', 'save_as_pb', 'actionEdit',
		'actionReload', 'actionSave_As']

	parent.file_edit_items = []
	for item in file_items:
		if item in parent.children:
			parent.file_edit_items.append(item)

	if parent.status.file:
		text = open(parent.status.file).read()
		if 'gcode_pte' in parent.children:
			parent.gcode_pte.setPlainText(text)
	else:
		for item in parent.file_edit_items:
			getattr(parent, item).setEnabled(False)

	# FIXME this needs to be in mdi setup
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
	}

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

	# touch off coordinate system combo box
	if 'touchoff_system_cb' in parent.children:
		coordinate_systems = {'Current': 0, 'G54': 1, 'G55': 2, 'G56': 3, 'G57': 4,
			'G58': 5, 'G59': 6, 'G59.1': 7, 'G59.2': 8, 'G59.3': 9}
		for key, value in coordinate_systems.items():
			parent.touchoff_system_cb.addItem(key, value)

	# change coordinate system buttons
	for i in range(1, 10):
		item = f'change_cs_{i}'
		if item in parent.children:
			getattr(parent, item).clicked.connect(partial(commands.change_cs, parent))
			parent.home_required.append(item)

	checkable_buttons = {'flood_pb': 'flood_toggle', 'mist_pb': 'mist_toggle',
		'optional_stop_pb': 'optional_stop_toggle',
		'block_delete_pb': 'block_delete_toggle',
		'feed_override_pb': 'feed_override_toggle',
}
	for key, value in checkable_buttons.items():
		if key in parent.children: # make sure checkable is set to true
			if not getattr(parent, key).isCheckable():
				getattr(parent, key).setCheckable(True)
			getattr(parent, key).clicked.connect(partial(getattr(commands, value), parent))

	# set the button checked states
	parent.status.poll()
	if 'feed_override_pb' in parent.children:
		parent.feed_override_pb.setChecked(parent.status.feed_override_enabled)

def setup_touchoff(parent):
	# check for required items tool_touchoff_ touchoff_pb_
	# FIXME add touchoff_le and tool_touchoff_le for touch screens
	# self.lineEdit_passwort.mousePressEvent = self.on_lineEdit_passwort_clicked
	# def on_lineEdit_passwort_clicked(self, *arg, **kwargs):
	# 	print("lineEdit_passwort clicked!")
	if 'touchoff_le' in parent.children:
		parent.touchoff_le.installEventFilter(parent)
		#parent.touchoff_le.mousePressEvent = test.test_it(parent)
	to_missing = False
	tto_missing = False
	touchoff = ['touchoff_le', 'touchoff_dsb']
	for item in AXES:
		if f'touchoff_pb_{item}' in parent.children:
			#print(bool(set(touchoff) & set(parent.children)))
			if bool(set(touchoff) & set(parent.children)):
				break
			else:
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
	if 'mdi_history_lw' in parent.children:
		if 'actionClear_MDI_History' in parent.children:
			parent.actionClear_MDI_History.setEnabled(False)
		if 'actionCopy_MDI_History' in parent.children:
			parent.actionCopy_MDI_History.setEnabled(False)

def setup_status_labels(parent):
	units = parent.inifile.find('TRAJ', 'LINEAR_UNITS') or False # mm or inch
	if units.lower() == 'inch':
		default_precision = 4
	elif units.lower() == 'mm':
		default_precision = 3

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

	# FIXME move linear_units and set precision
	status_items = ['acceleration', 'active_queue', 
	'adaptive_feed_enabled', 'angular_units', 'axes', 'axis',
	'axis_mask', 'block_delete', 'call_level', 'command', 'current_line',
	'current_vel', 'cycle_time', 'debug', 'delay_left', 'distance_to_go',
	'echo_serial_number', 'enabled', 'estop', 'exec_state',
	'feed_override_enabled', 'flood', 'g5x_index', 'ini_filename', 'inpos',
	'input_timeout', 'interp_state', 'interpreter_errcode', 'joint', 'joints',
	'kinematics_type', 'linear_units', 'lube', 'lube_level', 'max_acceleration',
	'max_velocity', 'mist', 'motion_line', 'motion_mode', 'motion_type',
	'optional_stop', 'paused', 'pocket_prepped', 'probe_tripped', 'probe_val',
	'probed_position', 'probing', 'program_units', 'queue', 'queue_full',
	'read_line', 'rotation_xy', 'settings', 'spindle', 'spindles', 'state',
	'task_mode', 'task_paused', 'task_state', 'tool_in_spindle',
	'tool_from_pocket', 'tool_offset', 'tool_table']

	# check for status labels in the ui key is label and value is status item
	parent.status_labels = {} # create an empty dictionary
	for item in status_items: # iterate the status items list
		if f'{item}_lb' in parent.children: # if the label is found
			parent.status_labels[f'{item}_lb'] = item # add the status and label

	parent.status_position = {} # create an empty dictionary
	for i, axis in enumerate(AXES):
		label = f'actual_lb_{axis}'
		if label in parent.children:
			p = getattr(parent, label).property('precision')
			p = p if p is not None else default_precision
			parent.status_position[f'{label}'] = [i, p] # label , joint & precision

	parent.status_dro = {} # create an empty dictionary
	for i, axis in enumerate(AXES):
		label = f'dro_lb_{axis}'
		if label in parent.children:
			p = getattr(parent, label).property('precision')
			p = p if p is not None else default_precision
			parent.status_dro[f'{label}'] = [i, p] # add the label, tuple position & precision

	parent.status_g5x = {} # create an empty dictionary
	for i, axis in enumerate(AXES):
		label = f'g5x_lb_{axis}'
		if label in parent.children:
			p = getattr(parent, label).property('precision')
			p = p if p is not None else default_precision
			parent.status_g5x[f'{label}'] = [i, p] # add the label, tuple position & precision

	parent.status_g92 = {} # create an empty dictionary
	for i, axis in enumerate(AXES):
		label = f'g92_lb_{axis}'
		if label in parent.children:
			p = getattr(parent, label).property('precision')
			p = p if p is not None else default_precision
			parent.status_g92[f'{label}'] = [i, p] # add the label, tuple position & precision

	# check for axis labels in the ui
	# this return a tuple of dictionaries syntax parent.status.axis[0]['velocity']
	# label axis_n_velocity_lb
	parent.status.poll()
	axes = parent.status.axis_mask.bit_count()

	parent.status_axes = {} # create an empty dictionary
	for i in range(axes):
		for item in ['max_position_limit', 'min_position_limit', 'velocity']:
			label = f'axis_{i}_{item}_lb'
			if label in parent.children:
				p = getattr(parent, label).property('precision')
				p = p if p is not None else default_precision
				parent.status_axes[label] = [i, item, p] # axis, status item, precision

	parent.status_axes_vel_min = {}
	for i in range(axes):
		label = f'axis_{i}_vel_per_min_lb'
		if label in parent.children:
			p = getattr(parent, label).property('precision')
			p = p if p is not None else default_precision
			parent.status_axes_vel_min[label] = [i, 'velocity', p] # axis, item, precision

	# two joint velocity
	parent.two_vel = {}
	if 'two_vel_lb' in parent.children:
		joint_0 = parent.two_vel_lb.property('joint_0')
		joint_1 = parent.two_vel_lb.property('joint_1')
		p = getattr(parent, f'two_vel_lb').property('precision')
		p = p if p is not None else default_precision
		if None not in (joint_0, joint_1): # check for None or False
			parent.two_vel['two_vel_lb'] = [joint_0, joint_1, p]

	# three joint velocity
	parent.three_vel = {}
	if 'three_vel_lb' in parent.children:
		joint_0 = parent.three_vel_lb.property('joint_0')
		joint_1 = parent.three_vel_lb.property('joint_1')
		joint_2 = parent.three_vel_lb.property('joint_2')
		p = getattr(parent, f'three_vel_lb').property('precision')
		p = p if p is not None else default_precision
		if None not in (joint_0, joint_1, joint_2): # check for None or False
			parent.three_vel['three_vel_lb'] = [joint_0, joint_1, joint_2, p]

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

	# joint velocity joint_velocity_n_lb parent.status.joint[0]['velocity']
	parent.status.poll()
	parent.joint_vel_sec = {}
	for i in range(parent.status.joints):
		if f'joint_vel_sec_{i}_lb' in parent.children: # if the label is found
			p = getattr(parent, f'joint_vel_sec_{i}_lb').property('precision')
			p = p if p is not None else default_precision
			parent.joint_vel_sec[f'joint_vel_sec_{i}_lb'] = [i, p] # add the label, tuple position & precision

	parent.joint_vel_min = {}
	for i in range(parent.status.joints):
		if f'joint_vel_min_{i}_lb' in parent.children: # if the label is found
			p = getattr(parent, f'joint_vel_min_{i}_lb').property('precision')
			p = p if p is not None else default_precision
			parent.joint_vel_min[f'joint_vel_min_{i}_lb'] = [i, p] # add the label, tuple position & precision

	joint_number_items = ['units', 'velocity']
	parent.status_joint_prec = {}
	for i in range(16):
		for item in joint_number_items:
			if f'joint_{item}_{i}_lb' in parent.children: # if the label is found
				p = getattr(parent, f'joint_{item}_{i}_lb').property('precision')
				p = p if p is not None else default_precision
				parent.status_joint_prec[f'{item}_{i}'] = [i, p] # add the label, tuple position & precision

	#override_items = ['feedrate',  'rapidrate',]
	override_items = {'feedrate_lb': 'feedrate' , 'rapidrate_lb': 'rapidrate',
		'rapid_override_lb': 'max_velocity'}
	# label : status item rapid_override_lb
	parent.overrides = {}
	for label, stat in override_items.items():
		if label in parent.children:
			parent.overrides[label] = stat

	# dio din_0_lb dout_0_lb
	parent.status_dio = {}
	for i in range(64):
		for item in ['din', 'dout']:
			label = f'{item}_{i}_lb'
			if label in parent.children:
				parent.status_dio[label] = [item, i] # add label and stat
				parent.stat_dict[f'{item}[{i}]'] = {0: False, 1: True}

	# aio ain_0_lb aout_0_lb aio[0] aout[0]
	parent.status_aio = {}
	for i in range(64):
		for item in ['ain', 'aout']:
			label = f'{item}_{i}_lb'
			if label in parent.children:
				p = getattr(parent, f'{item}_{i}_lb').property('precision')
				p = p if p is not None else default_precision
				parent.status_aio[label] = [item, i, p] # add label, stat and precision

	# check for tool table labels in the ui , 'comment'
	tool_table_items = ['id', 'xoffset', 'yoffset', 'zoffset', 'aoffset',
		'boffset', 'coffset', 'uoffset', 'voffset', 'woffset', 'diameter',
		'frontangle', 'backangle', 'orientation']
	parent.current_tool = {}
	for item in tool_table_items:
		if f'tool_{item}_lb' in parent.children:
			parent.current_tool[f'tool_{item}_lb'] = item

	if 'file_lb' in parent.children:
		parent.status.poll()
		gcode_file = parent.status.file or False
		if gcode_file:
			parent.file_lb.setText(os.path.basename(gcode_file))
		else:
			parent.file_lb.setText('No G code file loaded')

	parent.home_status = []
	for i in range(9):
		if f'home_lb_{i}' in parent.children:
			parent.home_status.append(f'home_lb_{i}')

	for item in parent.home_status:
		if parent.status.homed[int(item[-1])]:
			getattr(parent, item).setText('*')
		else:
			getattr(parent, item).setText('')

def setup_plain_text_edits(parent):
	# for gcode_pte update
	if 'gcode_pte' in parent.children:
		parent.gcode_pte.setCenterOnScroll(True)
		parent.gcode_pte.ensureCursorVisible()
		parent.gcode_pte.viewport().installEventFilter(parent)
		parent.gcode_pte.cursorPositionChanged.connect(partial(utilities.update_qcode_pte, parent))

		parent.status.poll()
		parent.last_line = parent.status.motion_line

def setup_check_boxes(parent):
	if 'print_states_cb' in parent.children:
		parent.print_states_cb.stateChanged.connect(partial(utilities.print_states, parent))
		parent.print_states = parent.print_states_cb.isChecked()
	else:
		parent.print_states = False

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
	# mdi_command_le and run_mdi_pb are required to run mdi commands
	# mdi_history_lw is optional
	# determine if mdi is possible from the gui
	# parent.mdi_command is tested in status.py so it much exist
	parent.mdi_command = ''
	if 'mdi_command_le' in parent.children and 'run_mdi_pb' in parent.children:
		if parent.mdi_command_le.property('mode') == 'touch':
			parent.mdi_command_le.installEventFilter(parent)
		else:
			parent.mdi_command_le.returnPressed.connect(partial(commands.run_mdi, parent))
		parent.home_required.append('run_mdi_pb')
		if 'mdi_history_lw' in parent.children:
			path = os.path.dirname(parent.status.ini_filename)
			mdi_file = os.path.join(path, 'mdi_history.txt')
			if os.path.exists(mdi_file): # load mdi history
				with open(mdi_file, 'r') as f:
					history_list = f.readlines()
					for item in history_list:
						parent.mdi_history_lw.addItem(item.strip())
			parent.mdi_history_lw.itemSelectionChanged.connect(partial(utilities.add_mdi, parent))

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
	required_jog_items = ['jog_vel_sl', 'jog_modes_cb']
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

		min_vel = parent.inifile.find('DISPLAY', 'MIN_LINEAR_VELOCITY') or False
		if min_vel:
			parent.jog_vel_sl.setMinimum(int(float(min_vel) * 60))

		max_vel = parent.inifile.find('DISPLAY', 'MAX_LINEAR_VELOCITY') or False
		if max_vel:
			parent.jog_vel_sl.setMaximum(int(float(max_vel) * 60))

		default_vel = parent.inifile.find('DISPLAY', 'DEFAULT_LINEAR_VELOCITY') or False
		if default_vel:
			parent.jog_vel_sl.setValue(int(float(default_vel) * 60))

		if 'jog_vel_lb' in parent.children:
			parent.jog_vel_sl.valueChanged.connect(partial(utilities.update_jog_lb, parent))
			parent.jog_vel_lb.setText(f'{parent.jog_vel_sl.value()}')
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
	# spindle defaults
	default_rpm = parent.inifile.find('DISPLAY', 'DEFAULT_SPINDLE_SPEED') or False
	if default_rpm:
		parent.spindle_speed = int(default_rpm)
	else:
		parent.spindle_speed = 100
	if 'spindle_speed_lb' in parent.children:
		parent.spindle_speed_lb.setText(f'{parent.spindle_speed}')
	parent.increment = 100
	parent.min_rpm = 0

	spindle_buttons = {
	'spindle_fwd_pb': 'spindle',
	'spindle_rev_pb': 'spindle',
	'spindle_stop_pb': 'spindle',
	'spindle_plus_pb': 'spindle',
	'spindle_minus_pb': 'spindle',
	}
	for key, value in spindle_buttons.items():
		if key in parent.children:
			getattr(parent, key).clicked.connect(partial(getattr(commands, value), parent))
			if key in ['spindle_fwd_pb', 'spindle_rev_pb']:
				getattr(parent, key).setCheckable(True)

	increment = parent.inifile.find('SPINDLE_0', 'INCREMENT') or False
	if not increment:
		increment = parent.inifile.find('DISPLAY', 'SPINDLE_INCREMENT') or False
	#elif not parent.increment:
	#	parent.increment = 100
	parent.increment = int(increment) if increment else 100

	if 'spindle_speed_sb' in parent.children:
		parent.spindle_speed_sb.valueChanged.connect(partial(commands.spindle, parent))
		parent.min_rpm = parent.inifile.find('SPINDLE_0', 'MIN_FORWARD_VELOCITY') or False 
		parent.min_rpm = int(parent.min_rpm) if parent.min_rpm else 0
		max_rpm = parent.inifile.find('SPINDLE_0', 'MAX_FORWARD_VELOCITY') or False
		max_rpm = int(max_rpm) if max_rpm else 1000
		parent.spindle_speed_sb.setMinimum(parent.min_rpm)
		parent.spindle_speed_sb.setMaximum(max_rpm)
		parent.spindle_speed_sb.setValue(parent.spindle_speed)
		parent.spindle_speed_sb.setSingleStep(parent.increment)

	if 'spindle_override_sl' in parent.children:
		parent.spindle_override_sl.valueChanged.connect(partial(utilities.spindle_override, parent))
		max_spindle_override = parent.inifile.find('DISPLAY', 'MAX_SPINDLE_OVERRIDE') or False
		if not max_spindle_override: max_spindle_override = 1.0
		max_spindle_override = int(float(max_spindle_override) * 100)
		parent.spindle_override_sl.setMaximum(max_spindle_override)
		if max_spindle_override >= 100:
			parent.spindle_override_sl.setValue(100)

	# check for spindle labels in the ui
	spindle_items = ['brake', 'direction', 'enabled', 'homed',
	'orient_fault', 'orient_state', 'override', 'override_enabled']
	parent.status_spindles = {}
	parent.status_spindle_overrides = {}
	parent.status_spindle_lcd = {}
	parent.status.poll()
	 # only look for the num of spindles configured
	for i in range(parent.status.spindles):
		for item in spindle_items:
			if f'spindle_{item}_{i}_lb' in parent.children:
				parent.status_spindles[f'spindle_{item}_{i}_lb'] = item

		if f'spindle_override_{i}_lb' in parent.children:
			parent.status_spindle_overrides[f'spindle_override_{i}_lb'] = i
			#parent.status_spindle_overrides[f'override_{i}'] = f'spindle_override_{i}_lb'

	# might think about this a bit...
	parent.status_spindle_dir = {}
	if 'spindle_direction_0_lb' in parent.children: 
		parent.status_spindle_dir['spindle_direction_0_lb'] = ['direction']

	parent.status_spindle_speed = {}
	if 'spindle_speed_0_lb' in parent.children:
		parent.status_spindle_speed['spindle_speed_0_lb'] = 'speed'

	if 'spindle_speed_0_lcd' in parent.children:
		parent.status_spindle_lcd['spindle_speed_0_lcd'] = 'speed'
		#parent.spindle_speed_0_lcd.display(123.5)

	# special spindle labels
	parent.spindle_actual_speed = []
	spindle_actual_speed = ['spindle_actual_speed_lb', 'spindle_override_0_lb']
	if all(x in parent.children for x in spindle_actual_speed):
		parent.spindle_actual_speed.append('spindle_actual_speed_lb')

def setup_tools(parent):
	# tool change using a combo box
	if 'tool_change_cb' in parent.children:
		tool_len = len(parent.status.tool_table)
		parent.tool_change_cb.addItem('Tool 0', 0)
		for i in range(1, tool_len):
			tool_id = parent.status.tool_table[i][0]
			parent.tool_change_cb.addItem(f'Tool {tool_id}', tool_id)
		if 'tool_change_pb' in parent.children:
			parent.tool_change_pb.clicked.connect(partial(commands.tool_change, parent))
			parent.home_required.append('tool_change_pb')
		else:
			msg = ('Tool change Push Button\n'
				'requires the next_tool_sb spin box.')
			dialogs.warn_msg_ok(msg, 'Required Item Missing')

	# home required touch off buttons
	# tool change is a MDI command so power on and all homed
	for i in range(100):
		item = f'tool_change_pb_{i}'
		if item in parent.children:
			getattr(parent, item).clicked.connect(partial(commands.tool_change, parent))
			parent.home_required.append(item)
	for axis in AXES:
		item = f'touchoff_pb_{axis}'
		if item in parent.children:
			getattr(parent, item).clicked.connect(partial(getattr(commands, 'touchoff'), parent))
			parent.home_required.append(item)
		item = f'tool_touchoff_{axis}'
		if item in parent.children:
			getattr(parent, item).clicked.connect(partial(getattr(commands, 'tool_touchoff'), parent))
			parent.home_required.append(item)

def setup_sliders(parent):
	if 'feed_override_sl' in parent.children:
		parent.feed_override_sl.valueChanged.connect(partial(utilities.feed_override, parent))
		max_feed_override = parent.inifile.find('DISPLAY', 'MAX_FEED_OVERRIDE') or False
		if not max_feed_override: max_feed_override = 1.0
		parent.feed_override_sl.setMaximum(int(float(max_feed_override) * 100))
		parent.feed_override_sl.setValue(100)

	if 'rapid_override_sl' in parent.children:
		parent.rapid_override_sl.valueChanged.connect(partial(utilities.rapid_override, parent))
		parent.rapid_override_sl.setMaximum(100)
		parent.rapid_override_sl.setValue(100)

def setup_defaults(parent):
	if 'optional_stop_pb' in parent.children:
		if parent.optional_stop_pb.isChecked():
			parent.command.set_optional_stop(True)
		else:
			parent.command.set_optional_stop(False)

def setup_mdi_buttons(parent):
	for button in parent.findChildren(QAbstractButton):
		if button.property('function') == 'mdi':
			if button.property('command'):
				button.clicked.connect(partial(commands.mdi_button, parent, button))
				parent.home_required.append(button.objectName())
				parent.state_estop[button.objectName()] = False
			else:
				msg = (f'MDI Button {button.text()}\n'
				'Does not have a command\n'
				f'{button.text()} will not be functional.')
				dialogs.warn_msg_ok(msg, 'Configuration Error')
				button.setEnabled(False)

def setup_hal_buttons(parent):
	hal_buttons = []
	for button in parent.findChildren(QAbstractButton):
		if button.property('function') == 'hal_pin':
			hal_buttons.append(button)
			if button.property('required') == 'homed':
				parent.home_required.append(button.objectName())
				parent.state_estop[button.objectName()] = False
	for n, button in enumerate(hal_buttons):
		props = button.dynamicPropertyNames()
		for prop in props:
			prop = str(prop, 'utf-8')
			if prop.startswith('pin_'): # we have a hal button
				pin_settings = button.property(prop).split(',')
				name = button.objectName()
				pin_name = pin_settings[0]
				pin_type = getattr(hal, f'{pin_settings[1].upper().strip()}')
				pin_dir = getattr(hal, f'{pin_settings[2].upper().strip()}')
				setattr(parent, f'{prop}', parent.halcomp.newpin(pin_name, pin_type, pin_dir))
				pin = getattr(parent, f'{prop}')
				if button.isCheckable():
					button.toggled.connect(lambda checked, pin=pin: (pin.set(checked)))
				else:
					button.pressed.connect(lambda pin=pin: (pin.set(True)))
					button.released.connect(lambda pin=pin: (pin.set(False)))
				parent.state_estop[button.objectName()] = False
				parent.state_estop_reset[button.objectName()] = False
				parent.state_on[button.objectName()] = True
	parent.halcomp.ready()

def setup_plot(parent):
	if 'plot_widget' in parent.children:
		from libflexgui import flexplot
		plotter = flexplot.graphics(parent)
		layout = QVBoxLayout(parent.plot_widget)
		layout.addWidget(plotter)

def set_status(parent): # FIXME look close at this to make sure it catches all
	parent.status.poll()
	if parent.status.task_state == linuxcnc.STATE_ESTOP:
		for key, value in parent.state_estop.items():
			getattr(parent, key).setEnabled(value)
		for key, value in parent.state_estop_names.items():
			getattr(parent, key).setText(value)

	if parent.status.task_state == linuxcnc.STATE_ESTOP_RESET:
		#print('STATE_ESTOP_RESET')
		for key, value in parent.state_estop_reset.items():
			getattr(parent, key).setEnabled(value)
		for key, value in parent.state_estop_reset_names.items():
			getattr(parent, key).setText(value)

	if parent.status.task_state == linuxcnc.STATE_ON:
		for key, value in parent.state_on.items():
			getattr(parent, key).setEnabled(value)
		for key, value in parent.state_on_names.items():
			getattr(parent, key).setText(value)
		if utilities.all_homed and parent.status.file:
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(True)
		if utilities.all_homed(parent):
			for item in parent.unhome_controls:
				getattr(parent, item).setEnabled(True)
			for item in parent.home_controls:
				getattr(parent, item).setEnabled(False)
		else:
			for item in parent.home_required:
				getattr(parent, item).setEnabled(False)
			for item in parent.unhome_controls:
				getattr(parent, item).setEnabled(False)
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(False)


