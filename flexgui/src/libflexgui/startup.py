import os, sys, shutil, re, importlib
from functools import partial

from PyQt6.QtWidgets import QPushButton, QListWidget, QPlainTextEdit, QLineEdit
from PyQt6.QtWidgets import QComboBox, QSlider, QMenu, QToolButton, QWidget
from PyQt6.QtWidgets import QVBoxLayout, QAbstractButton, QAbstractSpinBox
from PyQt6.QtWidgets import QLabel, QLCDNumber, QDoubleSpinBox
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSettings
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import linuxcnc, hal

from libflexgui import actions
from libflexgui import commands
from libflexgui import dialogs
from libflexgui import utilities
from libflexgui import flexplot
from libflexgui import view
from libflexgui import probe

AXES = ['x', 'y', 'z', 'a', 'b', 'c', 'u', 'v', 'w']

def set_screen(parent):
	try:
		parent.resize(parent.settings.value('GUI/window_size'))
		parent.move(parent.settings.value('GUI/window_position'))
		parent.no_check_firmware_cb.setChecked(True if parent.settings.value('NAGS/firmware') == "true" else False)
	except:
		pass

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
			if 'toolBar' in parent.children:
				widget_name = f'flex_{action.objectName()[6:].replace(" ", "_")}'
				# make sure the action is in the tool bar
				if parent.toolBar.widgetForAction(action) is not None:
					parent.toolBar.widgetForAction(action).setObjectName(widget_name)
					setattr(parent, widget_name, parent.toolBar.widgetForAction(action))
					parent.children.append(widget_name)
	menus = parent.findChildren(QMenu)
	for menu in menus:
		if menu.objectName():
			parent.children.append(menu.objectName())

def update_check(parent):
	if 'feedrate_lb' in parent.children:
		msg = ('The Feed Override Percent Label object name\n'
		'feedrate_lb has been changed to feed_override_lb.\n'
		'Change the name in the ui file.\n'
		'The label will be disabled and will not function.')
		dialogs.critical_msg_ok(msg, 'Object Name Changed')
		parent.feedrate_lb.setEnabled(False)

def setup_enables(parent):
	parent.home_required = [] # different functions add to this
	# disable home all if home sequence is not found
	if 'home_all_pb' in parent.children:
		if not utilities.home_all_check(parent):
			parent.home_all_pb.setEnabled(False)

	# STATE_ESTOP
	parent.state_estop = {
		'power_pb': False, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': False,
		'pause_pb': False, 'resume_pb': False,
		'home_all_pb': False, 'unhome_all_pb': False,
		'run_mdi_pb': False, 'mdi_s_pb': False,
		'spindle_start_pb': False, 'spindle_fwd_pb': False,
		'spindle_rev_pb': False, 'spindle_stop_pb': False,
		'spindle_plus_pb': False, 'spindle_minus_pb': False,
		'flood_pb': False, 'mist_pb': False,
		'actionPower': False, 'actionRun': False,
		'actionRun_From_Line': False, 'actionStep': False,
		'actionPause': False, 'tool_change_pb': False,
		'actionResume': False
		}

	for i in range(9):
		parent.state_estop[f'home_pb_{i}'] = False
		parent.state_estop[f'unhome_pb_{i}'] = False
	for axis in AXES:
		parent.state_estop[f'touchoff_pb_{axis}'] = False
		parent.state_estop[f'tool_touchoff_{axis}'] = False
		parent.state_estop[f'zero_{axis}_pb'] =  False
	for i in range(100):
		parent.state_estop[f'tool_change_pb_{i}'] = False
	for i in range(1, 10):
		parent.state_estop[f'change_cs_{i}'] = False

	# remove any items not found in the gui
	for item in list(parent.state_estop):
		if item not in parent.children:
			del parent.state_estop[item]

	parent.state_estop_names = {'estop_pb': 'E Stop Open',
		'actionE_Stop': 'E Stop Open', 'power_pb': 'Power Off',
		'actionPower': 'Power Off'}

	# remove any items not found in the gui
	for item in list(parent.state_estop_names):
		if item not in parent.children:
			del parent.state_estop_names[item]

	# STATE_ESTOP_RESET enable power
	parent.state_estop_reset = {
		'power_pb': True, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': False,
		'pause_pb': False, 'resume_pb': False,
		'home_all_pb': False, 'unhome_all_pb': False,
		'run_mdi_pb': False, 'spindle_start_pb': False,
		'spindle_fwd_pb': False, 'spindle_rev_pb': False,
		'spindle_stop_pb': False, 'spindle_plus_pb': False,
		'spindle_minus_pb': False, 'flood_pb': False,
		'mist_pb': False, 'actionPower': True,
		'actionRun': False, 'actionRun_From_Line': False,
		'actionStep': False, 'actionPause': False,
		'tool_change_pb': False, 'actionResume': False
		}

	for i in range(9):
		parent.state_estop_reset[f'home_pb_{i}'] = False
		parent.state_estop_reset[f'unhome_pb_{i}'] = False
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

	parent.state_estop_reset_names = {
		'estop_pb': 'E Stop Closed', 'actionE_Stop': 'E Stop Closed',
		'power_pb': 'Power Off', 'actionPower': 'Power Off'
		}

	# remove any items not found in the gui
	for item in list(parent.state_estop_reset_names):
		if item not in parent.children:
			del parent.state_estop_reset_names[item]

	# STATE_ON home, jog, spindle
	parent.state_on = {
		'power_pb': True, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': False,
		'pause_pb': False, 'resume_pb': False,
		'spindle_start_pb': True, 'spindle_fwd_pb': True,
		'spindle_rev_pb': True, 'spindle_stop_pb': True,
		'spindle_plus_pb': True, 'spindle_minus_pb': True,
		'flood_pb': True, 'mist_pb': True,
		'actionPower': True, 'actionRun': False,
		'actionRun_From_Line': False, 'actionStep': False,
		'actionPause': False, 'actionResume': False
		}

	# remove any items not found in the gui
	for item in list(parent.state_on):
		if item not in parent.children:
			del parent.state_on[item]

	parent.state_on_names = {'estop_pb': 'E Stop Closed',
		'actionE_Stop': 'E Stop Closed', 'power_pb': 'Power On',
		'actionPower': 'Power On'}

	# remove any items not found in the gui
	for item in list(parent.state_on_names):
		if item not in parent.children:
			del parent.state_on_names[item]

	# run controls used to enable/disable when not running a program
	run_items = ['open_pb', 'run_pb', 'run_from_line_pb', 'step_pb', 'run_mdi_pb',
	'reload_pb', 'actionOpen', 'menuRecent', 'actionReload', 'actionRun',
	'actionRun_From_Line', 'actionStep', 'tool_change_pb', 'flood_pb', 'mist_pb']
	for i in range(100):
		run_items.append(f'tool_change_pb_{i}')
	for item in AXES:
		run_items.append(f'tool_touchoff_{item}')
		run_items.append(f'touchoff_pb_{item}')
	parent.run_controls = []
	for item in run_items:
		if item in parent.children:
			parent.run_controls.append(item)

	home_items = []
	if utilities.home_all_check(parent):
		home_items.append('home_all_pb')
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

	parent.program_running = {
			'open_pb': False, 'reload_pb': False,
			'run_pb': False, 'run_from_line_pb': False,
			'step_pb': False, 'pause_pb': True,
			'resume_pb': False, 'run_mdi_pb': False,
			'home_all_pb': False,'actionRun': False,
			'actionOpen': False, 'menuRecent': False, 'actionReload': False,
			'actionRun_From_Line': False, 'actionStep': False,
			'actionPause': True, 'actionResume': False,
			'unhome_all_pb': False, 'spindle_start_pb': False,
			'spindle_fwd_pb': False, 'spindle_rev_pb': False,
			'spindle_stop_pb': False, 'spindle_plus_pb': False,
			'spindle_minus_pb': False, 'tool_change_pb': False,
			'flood_pb': False, 'mist_pb': False
			}

	for i in range(9):
		parent.program_running[f'home_pb_{i}'] = False
		parent.program_running[f'unhome_pb_{i}'] = False

	for i in range(100):
		parent.program_running[f'tool_change_pb_{i}'] = False

	for i in range(1, 10):
		parent.program_running[f'change_cs_{i}'] = False

	for item in AXES:
		parent.program_running[f'touchoff_pb_{item}'] = False
		parent.program_running[f'tool_touchoff_{item}'] = False

	parent.program_running['mdi_s_pb'] = False

	# remove any items not found in the gui
	for item in list(parent.program_running):
		if item not in parent.children:
			del parent.program_running[item]

	parent.program_paused = {
		'run_mdi_pb': False, 'run_pb': False,
		'run_from_line_pb': False, 'step_pb': True,
		'pause_pb': False, 'resume_pb': True,
		'home_all_pb': False, 'unhome_all_pb': False,
		'actionRun': False, 'actionRun_From_Line': False,
		'actionStep': True, 'actionPause': False,
		'actionResume': True, 'flood_pb': True,
		'mist_pb': True
		}

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

def setup_buttons(parent): # connect buttons to functions
	command_buttons = {
	'abort_pb': 'abort', 'manual_mode_pb':'set_mode_manual',
	'home_all_pb': 'home_all', 'home_pb_0': 'home',
	'home_pb_1': 'home', 'home_pb_2': 'home',
	'unhome_all_pb': 'unhome_all', 'unhome_pb_0': 'unhome',
	'unhome_pb_1': 'unhome', 'unhome_pb_2': 'unhome',
	'run_mdi_pb': 'run_mdi',
	}

	for i in range(11):
		command_buttons[f'clear_coord_{i}'] = 'clear_cs'

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
	'edit_tool_table_pb': 'action_edit_tool_table',
	'edit_ladder_pb': 'action_ladder_editor',
	'reload_tool_table_pb': 'action_reload_tool_table',
	'quit_pb': 'action_quit',
	'clear_mdi_history_pb': 'action_clear_mdi',
	'copy_mdi_history_pb': 'action_copy_mdi',
	'save_mdi_history_pb': 'action_save_mdi',
	'show_hal_pb': 'action_show_hal',
	'hal_meter_pb': 'action_hal_meter',
	'hal_scope_pb': 'action_hal_scope'
	}

	for key, value in action_buttons.items():
		if key in parent.children:
			getattr(parent, key).clicked.connect(partial(getattr(actions, value), parent))

	if 'errors_pte' in parent.children:
		if 'clear_errors_pb' in parent.children:
			parent.clear_errors_pb.clicked.connect(partial(utilities.clear_errors, parent))

		if 'copy_errors_pb' in parent.children:
			parent.copy_errors_pb.clicked.connect(partial(utilities.copy_errors, parent))

	if 'clear_info_pb' in parent.children:
		if 'info_pte' in parent.children:
			parent.clear_info_pb.clicked.connect(partial(utilities.clear_info, parent))

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

	# zero axis button setup
	for axis in AXES:
		name = f'zero_{axis}_pb'
		if name in parent.children:
			button = getattr(parent, name)
			button.clicked.connect(partial(commands.zero_axis, parent, axis.upper()))
			parent.home_required.append(name)

def setup_menus(parent):
	menus = parent.findChildren(QMenu)
	parent.shortcuts = []
	for menu in menus:
		menu_list = menu.actions()
		for index, action in enumerate(menu_list):
			if action.objectName() == 'actionOpen':
				if index + 1 < len(menu_list):
					parent.menuRecent = QMenu('Recent', parent)
					parent.menuRecent.setObjectName('menuRecent')
					parent.children.append('menuRecent')
					parent.menuFile.insertMenu(menu_list[index + 1], parent.menuRecent)
					# if any files have been opened add them
					keys = parent.settings.allKeys()
					for key in keys:
						if key.startswith('recent_files'):
							path = parent.settings.value(key)
							name = os.path.basename(path)
							a = parent.menuRecent.addAction(name)
							a.triggered.connect(partial(getattr(actions, 'load_file'), parent, path))
			if action.objectName() == 'actionHoming': # add homing actions
				action.setMenu(QMenu('Homing', parent))

				# add Home All if the home sequence is set for all axes
				if utilities.home_all_check(parent):
					setattr(parent, 'actionHome_All', QAction('Home All', parent))
					getattr(parent, 'actionHome_All').setObjectName('actionHome_all')
					action.menu().addAction(getattr(parent, 'actionHome_All'))
					getattr(parent,'actionHome_All').triggered.connect(partial(commands.home_all, parent))
					parent.home_controls.append('actionHome_All')
					parent.state_estop['actionHome_All'] = False
					parent.state_estop_reset['actionHome_All'] = False
					parent.state_on['actionHome_All'] = True
					parent.program_running['actionHome_All'] = False
					parent.program_paused['actionHome_All'] = False

				# add Home menu item for each axis
				for i, axis in enumerate(parent.axis_letters):
					setattr(parent, f'actionHome_{i}', QAction(f'Home {axis}', parent))
					getattr(parent, f'actionHome_{i}').setObjectName(f'actionHome_{i}')
					action.menu().addAction(getattr(parent, f'actionHome_{i}'))
					getattr(parent, f'actionHome_{i}').triggered.connect(partial(commands.home, parent))
					parent.home_controls.append(f'actionHome_{i}')
					parent.state_estop[f'actionHome_{i}'] = False
					parent.state_estop_reset[f'actionHome_{i}'] = False
					parent.state_on[f'actionHome_{i}'] = True
					parent.program_running[f'actionHome_{i}'] = False
					parent.program_paused[f'actionHome_{i}'] = False

			elif action.objectName() == 'actionUnhoming':
				action.setMenu(QMenu('Unhoming', parent))
				setattr(parent, 'actionUnhome_All', QAction('Unome All', parent))
				getattr(parent, 'actionUnhome_All').setObjectName('actionUnhome_All')
				action.menu().addAction(getattr(parent, 'actionUnhome_All'))
				getattr(parent,'actionUnhome_All').triggered.connect(partial(commands.unhome_all, parent))
				parent.unhome_controls.append('actionUnhome_All')
				parent.state_estop['actionUnhome_All'] = False
				parent.state_estop_reset['actionUnhome_All'] = False
				parent.state_on['actionUnhome_All'] = True
				parent.program_running['actionUnhome_All'] = False
				parent.program_paused['actionUnhome_All'] = False

				for i, axis in enumerate(parent.axis_letters):
					setattr(parent, f'actionUnhome_{i}', QAction(f'Unhome {axis}', parent))
					getattr(parent, f'actionUnhome_{i}').setObjectName(f'actionUnhome_{i}')
					action.menu().addAction(getattr(parent, f'actionUnhome_{i}'))
					getattr(parent, f'actionUnhome_{i}').triggered.connect(partial(commands.unhome, parent))
					parent.unhome_controls.append(f'actionUnhome_{i}')
					parent.state_estop[f'actionUnhome_{i}'] = False
					parent.state_estop_reset[f'actionUnhome_{i}'] = False
					parent.state_on[f'actionUnhome_{i}'] = True
					parent.program_running[f'actionUnhome_{i}'] = False
					parent.program_paused[f'actionUnhome_{i}'] = False
			elif action.objectName() == 'actionClear_Offsets':
				action.setMenu(QMenu('Clear Offsets', parent))
				cs = ['Current', 'G54', 'G55', 'G56', 'G57', 'G58', 'G59', 'G59.1', 'G59.2', 'G59.3', 'G92']
				for i, item in enumerate(cs):
					setattr(parent, f'actionClear_{i}', QAction(f'Clear {item}', parent))
					getattr(parent, f'actionClear_{i}').setObjectName(f'actionClear_{i}')
					action.menu().addAction(getattr(parent, f'actionClear_{i}'))
					getattr(parent, f'actionClear_{i}').triggered.connect(partial(commands.clear_cs, parent))

			if len(action.shortcut().toString()) > 0: # collect shortcuts for quick reference
				parent.shortcuts.append(f'{action.text()}\t{action.shortcut().toString()}')
	'''
	# special check for Homing, Unhoming and Clear Offsets in the menu
	menus = parent.findChildren(QMenu)
	for menu in menus: # menus is the top most menu like File Machine etc.
		menu_list = menu.actions()
		for index, action in enumerate(menu_list):
	'''


def setup_actions(parent): # setup menu actions
	actions_dict = {
		'actionOpen': 'action_open',
		'actionEdit': 'action_edit',
		'actionReload': 'action_reload',
		'actionSave_As': 'action_save_as',
		'actionEdit_Tool_Table': 'action_edit_tool_table',
		'actionReload_Tool_Table': 'action_reload_tool_table',
		'actionLadder_Editor': 'action_ladder_editor',
		'actionQuit': 'action_quit',
		'actionE_Stop': 'action_estop',
		'actionPower': 'action_power',
		'actionRun': 'action_run',
		'actionRun_From_Line': 'action_run_from_line',
		'actionStep': 'action_step',
		'actionPause': 'action_pause',
		'actionResume': 'action_resume',
		'actionStop': 'action_stop',
		'actionClear_MDI_History': 'action_clear_mdi',
		'actionCopy_MDI_History': 'action_copy_mdi',
		'actionOverlay': 'action_toggle_overlay',
		'actionShow_HAL': 'action_show_hal',
		'actionHAL_Meter': 'action_hal_meter',
		'actionHAL_Scope': 'action_hal_scope',
		'actionAbout': 'action_about',
		'actionQuick_Reference': 'action_quick_reference'}

	# if an action is found connect it to the function
	for key, value in actions_dict.items():
		if key in parent.children:
			getattr(parent, f'{key}').triggered.connect(partial(getattr(actions, f'{value}'), parent))

	# special check for the classicladder editor
	if not hal.component_exists("classicladder_rt"):
		if 'actionLadder_Editor' in parent.children:
			parent.actionLadder_Editor.setEnabled(False)
		if 'edit_ladder_pb' in parent.children:
			parent.edit_ladder_pb.setEnabled(False)

	# special check for MDI
	if 'mdi_history_lw' in parent.children:
		if 'actionClear_MDI_History' in parent.children:
			parent.actionClear_MDI_History.setEnabled(False)
		if 'actionCopy_MDI_History' in parent.children:
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
	'echo_serial_number', 'enabled', 'estop', 'exec_state', 'feed_hold_enabled',
	'feed_override_enabled', 'flood', 'g5x_index', 'ini_filename', 'inpos',
	'input_timeout', 'interp_state', 'interpreter_errcode', 'joint', 'joints',
	'kinematics_type', 'lube', 'lube_level', 'max_acceleration',
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
			p = p if p is not None else parent.default_precision
			parent.status_position[f'{label}'] = [i, p] # label , joint & precision

	parent.status_dro = {} # create an empty dictionary
	for i, axis in enumerate(AXES):
		label = f'dro_lb_{axis}'
		if label in parent.children:
			p = getattr(parent, label).property('precision')
			p = p if p is not None else parent.default_precision
			parent.status_dro[f'{label}'] = [i, p] # add the label, tuple position & precision

	parent.status_g5x_offset = {} # create an empty dictionary
	for i, axis in enumerate(AXES):
		label = f'g5x_lb_{axis}'
		if label in parent.children:
			p = getattr(parent, label).property('precision')
			p = p if p is not None else parent.default_precision
			parent.status_g5x_offset[f'{label}'] = [i, p] # add the label, tuple position & precision

	parent.status_g92 = {} # create an empty dictionary
	for i, axis in enumerate(AXES):
		label = f'g92_lb_{axis}'
		if label in parent.children:
			p = getattr(parent, label).property('precision')
			p = p if p is not None else parent.default_precision
			parent.status_g92[f'{label}'] = [i, p] # add the label, tuple position & precision

	# check for axis labels in the ui
	# this return a tuple of dictionaries syntax parent.status.axis[0]['velocity']
	# label axis_n_velocity_lb
	parent.status.poll()

	parent.status_axes = {} # create an empty dictionary
	for i in range(parent.axis_count):
		for item in ['max_position_limit', 'min_position_limit', 'velocity']:
			label = f'axis_{i}_{item}_lb'
			if label in parent.children:
				p = getattr(parent, label).property('precision')
				p = p if p is not None else parent.default_precision
				parent.status_axes[label] = [i, item, p] # axis, status item, precision

	# two joint velocity
	parent.two_vel = {}
	if 'two_vel_lb' in parent.children:
		joint_0 = parent.two_vel_lb.property('joint_0')
		joint_1 = parent.two_vel_lb.property('joint_1')
		p = getattr(parent, f'two_vel_lb').property('precision')
		p = p if p is not None else parent.default_precision
		if None not in (joint_0, joint_1): # check for None or False
			parent.two_vel['two_vel_lb'] = [joint_0, joint_1, p]

	# three joint velocity
	parent.three_vel = {}
	if 'three_vel_lb' in parent.children:
		joint_0 = parent.three_vel_lb.property('joint_0')
		joint_1 = parent.three_vel_lb.property('joint_1')
		joint_2 = parent.three_vel_lb.property('joint_2')
		p = getattr(parent, f'three_vel_lb').property('precision')
		p = p if p is not None else parent.default_precision
		if None not in (joint_0, joint_1, joint_2): # check for None or False
			parent.three_vel['three_vel_lb'] = [joint_0, joint_1, joint_2, p]

	parent.status_units = {}
	if 'linear_units_lb' in parent.children:
		p = parent.linear_units_lb.property('precision') or parent.default_precision
		parent.status_units['linear_units_lb'] = ['linear_units', p]

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
			p = p if p is not None else parent.default_precision
			parent.joint_vel_sec[f'joint_vel_sec_{i}_lb'] = [i, p] # add the label, tuple position & precision

	parent.joint_vel_min = {}
	for i in range(parent.status.joints):
		if f'joint_vel_min_{i}_lb' in parent.children: # if the label is found
			p = getattr(parent, f'joint_vel_min_{i}_lb').property('precision')
			p = p if p is not None else parent.default_precision
			parent.joint_vel_min[f'joint_vel_min_{i}_lb'] = [i, p] # add the label, tuple position & precision

	joint_number_items = ['units', 'velocity']
	parent.status_joint_prec = {}
	for i in range(16):
		for item in joint_number_items:
			if f'joint_{item}_{i}_lb' in parent.children: # if the label is found
				p = getattr(parent, f'joint_{item}_{i}_lb').property('precision')
				p = p if p is not None else parent.default_precision
				parent.status_joint_prec[f'{item}_{i}'] = [i, p] # add the label, tuple position & precision

	override_items = {'feed_override_lb': 'feedrate' , 'rapid_override_lb': 'rapidrate'}

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
				p = p if p is not None else parent.default_precision
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
			if 'start_line_lb' in parent.children:
				parent.start_line_lb.setText('0')
		else:
			parent.file_lb.setText('N/A')
			if 'start_line_lb' in parent.children:
				parent.start_line_lb.setText('n/a')

	parent.home_status = []
	for i in range(9):
		if f'home_lb_{i}' in parent.children:
			parent.home_status.append(f'home_lb_{i}')

	for item in parent.home_status:
		if parent.status.homed[int(item[-1])]:
			getattr(parent, item).setText('*')
		else:
			getattr(parent, item).setText('')

	if 'settings_speed_lb' in parent.children:
		parent.status_settings = {'settings_speed_lb': 2}
		parent.settings_speed_lb.setText(f'S{parent.status.settings[2]}')

	if 'mdi_s_pb' in parent.children:
		parent.mdi_s_pb.clicked.connect(partial(commands.spindle, parent))
		parent.home_required.append('mdi_s_pb')

def setup_list_widgets(parent):
	if 'file_lw' in parent.children:
		if os.path.exists(parent.nc_code_dir):
			utilities.read_dir(parent) # this is called from actions as well
		parent.file_lw.itemClicked.connect(partial(actions.file_selector, parent))

def setup_plain_text_edits(parent):
	# for gcode_pte update
	if 'gcode_pte' in parent.children:
		parent.gcode_pte.setCenterOnScroll(True)
		parent.gcode_pte.ensureCursorVisible()
		parent.gcode_pte.viewport().installEventFilter(parent)
		parent.gcode_pte.cursorPositionChanged.connect(partial(utilities.update_qcode_pte, parent))
		parent.status.poll()
		parent.last_line = parent.status.motion_line

def setup_line_edits(parent):
	parent.number_le = []
	parent.nccode_le = []
	parent.keyboard_le = []
	for child in parent.findChildren(QLineEdit):
		if child.property('input') == 'number': # enable the number pad
			parent.number_le.append(child.objectName())
			child.installEventFilter(parent)
		elif child.property('input') == 'nccode': # enable the nc code pad
			parent.nccode_le.append(child.objectName())
			child.installEventFilter(parent)
		elif child.property('input') == 'keyboard': # enable the keyboard pad
			parent.keyboard_le.append(child.objectName())
			child.installEventFilter(parent)

def setup_spin_boxes(parent):
	parent.touch_sb = []
	for child in parent.findChildren(QAbstractSpinBox):
		if child.property('input') == 'number': # enable the number pad
			sb_child = child.findChild(QLineEdit)
			sb_child.setObjectName(f'{child.objectName()}_child')
			parent.touch_sb.append(sb_child.objectName())
			sb_child.installEventFilter(parent)
			#le.installEventFilter(parent)

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
	# parent.mdi_command is tested in status.py so it must exist
	parent.mdi_command = ''

	if 'run_mdi_pb' in parent.children:
		if 'mdi_command_le' in parent.children: # we are good to go
			if parent.mdi_command_le.property('input') == 'nccode':
			 parent.gcode_le.append('mdi_command_le')
			 parent.mdi_command_le.installEventFilter(parent)
			elif parent.mdi_command_le.property('input') == 'keyboard':
			 parent.keyboard_le.append('mdi_command_le')
			 parent.mdi_command_le.installEventFilter(parent)
			else: # keyboard and mouse
				parent.mdi_command_le.returnPressed.connect(partial(commands.run_mdi, parent))
			parent.home_required.append('run_mdi_pb')
		else: # missing mdi_command_le
			parent.run_mdi_pb.setEnabled(False)

	if 'mdi_history_lw' in parent.children:
		path = os.path.dirname(parent.status.ini_filename)
		mdi_file = os.path.join(path, 'mdi_history.txt')
		if os.path.exists(mdi_file): # load mdi history
			with open(mdi_file, 'r') as f:
				history_list = f.readlines()
				for item in history_list:
					parent.mdi_history_lw.addItem(item.strip())
		parent.mdi_history_lw.itemSelectionChanged.connect(partial(utilities.add_mdi, parent))

def setup_jog(parent):
	jog_buttons = {}
	required_jog_items = ['jog_vel_sl', 'jog_modes_cb']
	jog_buttons = []
	for i in range(16):
		if f'jog_plus_pb_{i}' in parent.children:
			jog_buttons.append(f'jog_plus_pb_{i}')
		if f'jog_minus_pb_{i}' in parent.children:
			jog_buttons.append(f'jog_minus_pb_{i}')

	if len(jog_buttons) > 0:
		for item in required_jog_items:
			# don't make the connection if all required widgets are not present
			if item not in parent.children:
				msg = (f'{item} is required to jog\n but was not found.\n'
					'Jog Buttons will be disabled.')
				dialogs.warn_msg_ok(msg, 'Missing Item')
				for item in jog_buttons:
					getattr(parent, item).setEnabled(False)
				return

		# ok to connect if we get this far
		for item in jog_buttons: # connect jog buttons
			getattr(parent, item).pressed.connect(partial(getattr(commands, 'jog'), parent))
			getattr(parent, item).released.connect(partial(getattr(commands, 'jog'), parent))
			parent.state_estop[item] = False
			parent.state_estop_reset[item] = False
			parent.state_on[item] = True
			parent.program_running[item] = False

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

		# machine units are inch
		# do not convert in or inch
		# convert mil to inch mil * 0.001 = inch
		# convert cm to inch divide the value by 2.54
		# convert mm to inch divide the value by 25.4
		# convert um to inch divide the value by 25400

		# machine units are mm
		# convert inches to mm multiply the value by 25.4
		# convert mil to mm mil * 0.001 = inch multiply the value by 25.4
		# convert cm to mm multiply the length value by 10
		# no conversion for mm
		# convert um to mm divide the length value by 1000

		parent.jog_modes_cb.addItem('Continuous', False)
		machine_units = parent.inifile.find('TRAJ', 'LINEAR_UNITS') or False
		units = ['mm', 'cm', 'um', 'in', 'inch', 'mil']
		increments = parent.inifile.find('DISPLAY', 'INCREMENTS') or False

		if increments:
			incr_list = []
			values = increments.split(',')
			for item in values:
				item = item.strip()
				if item[-1].isdigit():
					distance = conv_to_decimal(item) # if it's a fraction convert to decimal
					incr_list.append([item, distance])
					parent.jog_modes_cb.addItem(item, distance)
				else:
					for suffix in units:
						if item.endswith(suffix):
							distance = item.removesuffix(suffix).strip()
							if utilities.is_float(distance):
								converted_distance = conv_units(distance, suffix, machine_units)
								incr_list.append([item, converted_distance])
								parent.jog_modes_cb.addItem(item, converted_distance)
								break
							else:
								msg = ('Malformed INCREMENTS value\n'
									f'{distance}\n'
									'may be missing comma seperators?')
								dialogs.warn_msg_ok(msg, 'Error')
					else:
						msg = ('INI section DISPLAY value INCREMENTS\n'
							f'{item} is not a valid jog increment\n'
							'and will not be added to the jog options.')
						dialogs.warn_msg_ok(msg, 'Configuration Error')

def conv_units(value, suffix, machine_units):
	if machine_units == 'inch':
		if suffix == 'in' or suffix == 'inch':
			return float(value)
		elif suffix == 'mil':
			return float(value) * 0.001
		elif suffix == 'cm':
			return float(value) / 2.54
		elif suffix == 'mm':
			return float(value) / 25.4
		elif suffix == 'um':
			return float(value) / 25400

	elif machine_units == 'mm':
		if suffix == 'in' or suffix == 'inch':
			return float(value) * 25.4
		elif suffix == 'mil':
			return float(value) * 0.0254
		elif suffix == 'cm':
			return float(value) * 10
		elif suffix == 'mm':
			return float(value)
		elif suffix == 'um':
			return float(value) / 1000

def conv_to_decimal(data):
	if "/" in data:
		p, q = data.split("/")
		return (float(p) / float(q))
	else:
		return float(data)

def setup_spindle(parent):
	# spindle defaults
	default_rpm = parent.inifile.find('DISPLAY', 'DEFAULT_SPINDLE_SPEED') or False
	if default_rpm:
		parent.spindle_speed = int(default_rpm)
	else:
		parent.spindle_speed = 0
	if 'spindle_speed_lb' in parent.children:
		parent.spindle_speed_lb.setText(f'{parent.spindle_speed}')
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
	parent.increment = int(increment) if increment else 10

	if 'spindle_speed_sb' in parent.children:
		parent.spindle_speed_sb.valueChanged.connect(partial(commands.spindle, parent))

		parent.min_rpm = parent.inifile.find('SPINDLE_0', 'MIN_FORWARD_VELOCITY') or False
		if parent.min_rpm and utilities.is_int(parent.min_rpm): # found in the ini and a valid int
			parent.min_rpm = int(parent.min_rpm)
		elif parent.min_rpm and utilities.is_float(parent.min_rpm): # see if it's a float if so convert to int
			parent.min_rpm = utilities.string_to_int(parent.min_rpm)
		else:
			parent.min_rpm = 0
		parent.spindle_speed_sb.setMinimum(parent.min_rpm)

		max_rpm = parent.inifile.find('SPINDLE_0', 'MAX_FORWARD_VELOCITY') or False
		if max_rpm and utilities.is_int(max_rpm): # found in the ini and a valid int
			parent.max_rpm = int(max_rpm)
			parent.spindle_speed_sb.setMaximum(parent.max_rpm)
		elif max_rpm and utilities.is_float(max_rpm): # see if it's a float if so convert to int
			parent.max_rpm = utilities.string_to_int(max_rpm)
			parent.spindle_speed_sb.setMaximum(parent.max_rpm)
		else:
			parent.max_rpm = 1000
			parent.spindle_speed_sb.setMaximum(parent.max_rpm)

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

	# special spindle labels
	parent.spindle_actual_speed = []
	# only add the actual speed if the override slider is there
	spindle_actual_speed = ['spindle_actual_speed_lb', 'spindle_override_sl']
	if all(x in parent.children for x in spindle_actual_speed):
		parent.spindle_actual_speed.append('spindle_actual_speed_lb')

def setup_touchoff(parent):
	# check for required items tool_touchoff_ touchoff_pb_
	if 'touchoff_le' in parent.children:
		parent.touchoff_le.setText('0')
		if parent.touchoff_le.property('input') == 'number': # enable the number pad
			parent.touchoff_le.installEventFilter(parent)
			parent.number_le.append('touchoff_le')

	if 'tool_touchoff_le' in parent.children:
		parent.tool_touchoff_le.setText('0')
		if parent.tool_touchoff_le.property('input') == 'number': # enable the number pad
			parent.tool_touchoff_le.installEventFilter(parent)
			parent.number_le.append('tool_touchoff_le')

	# setup touch off buttons
	for axis in AXES:
		item = f'touchoff_pb_{axis}'
		if item in parent.children:
			getattr(parent, item).clicked.connect(partial(getattr(commands, 'touchoff'), parent))
			parent.home_required.append(item)

def setup_tools(parent):
	# tool change using a combo box
	tool_change_required = ['tool_change_pb', 'tool_change_cb']
	# test to see if any tool change items are in the ui
	if set(tool_change_required) & set(parent.children):
		# test to make sure all items required are in the ui
		if not all(item in parent.children for item in tool_change_required):
			missing_items = list(sorted(set(tool_change_required) - set(parent.children)))
			missing = ' '.join(missing_items)
			msg = ('Tool change requires both\n'
				'the tool_change_cb combo box\n'
				'and the tool_change_pb push button.\n'
				f'{missing} was not found.')
			dialogs.warn_msg_ok(msg, 'Required Item Missing')
			return
		tool_len = len(parent.status.tool_table)
		parent.tool_change_cb.addItem('Tool 0', 0)
		for i in range(1, tool_len):
			tool_id = parent.status.tool_table[i][0]
			parent.tool_change_cb.addItem(f'Tool {tool_id}', tool_id)
		parent.tool_change_pb.clicked.connect(partial(commands.tool_change, parent))
		parent.home_required.append('tool_change_pb')
	# tool change push buttons is a MDI command so power on and all homed
	for i in range(100):
		item = f'tool_change_pb_{i}'
		if item in parent.children:
			getattr(parent, item).clicked.connect(partial(commands.tool_change, parent))
			parent.home_required.append(item)

	# tool touch off
	# home required for tool touch off buttons
	# check to see if any tool touch off buttons are in the ui
	for axis in AXES:
		item = f'tool_touchoff_{axis}'
		if item in parent.children:
			if 'tool_touchoff_le' in parent.children:
				getattr(parent, item).clicked.connect(partial(getattr(commands, 'tool_touchoff'), parent))
				parent.home_required.append(item)
			else:
				getattr(parent, item).setEnabled(False)
				msg = ('Tool Touchoff Button requires\n'
				'the Tool Offset Line Edit tool_touchoff_le')
				dialogs.warn_msg_ok(msg, 'Required Item Missing')

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

def setup_overrides(parent):
	if 'override_limits_cb' in parent.children:
		parent.override_limits_cb.setEnabled(False)

def setup_defaults(parent):
	if 'optional_stop_pb' in parent.children:
		if parent.optional_stop_pb.isChecked():
			parent.command.set_optional_stop(True)
		else:
			parent.command.set_optional_stop(False)

def setup_probing(parent):
	# any object name that starts with probe_ is disabled
	parent.probing = False
	parent.probe_controls = []
	for child in parent.children:
		if child.startswith('probe_') and not isinstance(child, QLabel):
			if not isinstance(parent.findChild(QWidget, child), QLabel):
				getattr(parent, child).setEnabled(False)
				parent.probe_controls.append(child)
	if len(parent.probe_controls) > 0: # make sure the probe enable is present
		if 'probing_enable_pb' in parent.children:
			parent.state_estop[f'probing_enable_pb'] = False
			parent.probing_enable_pb.setCheckable(True)
			parent.home_required.append('probing_enable_pb')
			parent.probing_enable_pb.toggled.connect(partial(probe.toggle, parent))
		else:
			msg = ('The Probing Enable Push Button\n'
				'was not found, all probe controls\n'
				'will be disabled. Did you name it\n'
				'probing_enable_pb?')
			dialogs.warn_msg_ok(msg, 'Object Not Found!')

def setup_mdi_buttons(parent):
	for button in parent.findChildren(QAbstractButton):
		if button.property('function') == 'mdi':
			if button.property('command'):
				button_name = button.objectName()
				button.clicked.connect(partial(commands.mdi_button, parent, button))
				# probe buttons are taken care of in setup_probe function
				if button_name.startswith('probe_'):
					parent.probe_controls.append(button_name)
				else:
					parent.program_running[button_name] = False
					parent.state_estop[button_name] = False
					parent.home_required.append(button_name)
			else:
				msg = (f'MDI Button {button.text()}\n'
				'Does not have a command\n'
				f'{button.text()} will not be functional.')
				dialogs.warn_msg_ok(msg, 'Configuration Error')
				button.setEnabled(False)

def setup_get_var(parent):
	# variables are floats so only put them in a QDoubleSpinBox
	var_file = os.path.join(parent.ini_path, parent.var_file)
	with open(var_file, 'r') as f:
		var_list = f.readlines()

	for item in parent.findChildren(QDoubleSpinBox):
		if item.property('function') == 'get_var':
			var = item.property('variable')
			found = False
			for line in var_list:
				if line.startswith(var):
					item.setValue(float(line.split()[1]))
					found = True
					break
			if not found:
				msg = (f'The variable {var} was not found\n'
				f'in the variables file {parent.var_file}\n'
				f'the QDoubleSpinBox {item.objectName()}\n'
				'will not contain any value.')
				dialogs.warn_msg_ok(msg, 'Error')

def setup_hal(parent):
	hal_labels = []
	hal_buttons = []
	hal_spinboxes = []
	hal_sliders = []
	hal_lcd = []
	parent.hal_io = {}
	parent.hal_readers = {}
	parent.hal_floats = {}
	children = parent.findChildren(QWidget)

	for child in children:
		if child.property('function') == 'hal_io':
			print(child.objectName())
			child_name = child.objectName()
			pin_name = child.property('pin_name')
			hal_type = child.property('hal_type')
			hal_dir = child.property('hal_dir')
			hal_type = getattr(hal, f'{hal_type}')
			hal_dir = getattr(hal, f'{hal_dir}')
			setattr(parent, f'{pin_name}', parent.halcomp.newpin(pin_name, hal_type, hal_dir))
			child.valueChanged.connect(partial(utilities.update_hal_io, parent))
			parent.hal_io[child_name] = pin_name

	for child in children:
		if child.property('function') == 'hal_pin':
			if isinstance(child, QAbstractButton):
				hal_buttons.append(child)
			elif isinstance(child, QAbstractSpinBox):
				hal_spinboxes.append(child)
			elif isinstance(child, QSlider):
				hal_sliders.append(child)
			elif isinstance(child, QLabel):
				hal_labels.append(child)
			elif isinstance(child, QLCDNumber):
				hal_lcd.append(child)

	if len(hal_lcd) > 0: # setup hal labels
		valid_types = ['HAL_FLOAT', 'HAL_S32', 'HAL_U32']
		for lcd in hal_lcd:
			lcd_name = lcd.objectName()
			pin_name = lcd.property('pin_name')
			if pin_name in dir(parent):
				msg = (f'HAL LCD {lcd_name}\n'
				f'pin name {pin_name}\n'
				'is already used in Flex GUI\n'
				'The HAL pin can not be created.')
				dialogs.critical_msg_ok(msg, 'Configuration Error')
				continue

			hal_type = lcd.property('hal_type')
			if hal_type not in valid_types:
				lcd.setEnabled(False)
				msg = (f'{hal_type} is not valid\n'
				'for a HAL LCD, only\n'
				'HAL_FLOAT or HAL_S32 or HAL_U32\n'
				f'can be used. The {lcd_name} will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			hal_dir = lcd.property('hal_dir')
			if hal_dir != 'HAL_IN':
				lcd.setEnabled(False)
				msg = (f'{hal_dir} is not a valid\n'
				'hal_dir for a HAL LCD Display,\n'
				'only HAL_IN can be used for hal_dir.\n'
				f'The {lcd_name} LCD will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			if lcd_name == pin_name:
				lcd.setEnabled(False)
				msg = (f'The object name {lcd_name}\n'
					'can not be the same as the\n'
					f'pin name {pin_name}.\n'
					'The HAL object will not be created\n'
					'and the LCD will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			if None not in [pin_name, hal_type, hal_dir]:
				hal_type = getattr(hal, f'{hal_type}')
				hal_dir = getattr(hal, f'{hal_dir}')
				setattr(parent, f'{pin_name}', parent.halcomp.newpin(pin_name, hal_type, hal_dir))
				pin = getattr(parent, f'{pin_name}')
				# if hal type is float add it to hal_float with precision
				if hal_type == 2: # HAL_FLOAT
					p = lcd.property('precision')
					p = p if p is not None else parent.default_precision
					parent.hal_floats[f'{lcd_name}'] = [pin_name, p] # lcd ,status item, precision
				else:
					parent.hal_readers[lcd_name] = pin_name

	if len(hal_labels) > 0: # setup hal labels
		valid_types = ['HAL_BIT', 'HAL_FLOAT', 'HAL_S32', 'HAL_U32']
		for label in hal_labels:
			label_name = label.objectName()
			pin_name = label.property('pin_name')
			if pin_name in dir(parent):
				msg = (f'HAL Label {label_name}\n'
				f'pin name {pin_name}\n'
				'is already used in Flex GUI\n'
				'The HAL pin can not be created.')
				dialogs.critical_msg_ok(msg, 'Configuration Error')
				continue

			hal_type = label.property('hal_type')
			if hal_type not in valid_types:
				label.setEnabled(False)
				msg = (f'{hal_type} is not valid for a HAL Label\n'
				', only HAL_BIT, HAL_FLOAT, HAL_S32 or HAL_U32\n'
				f'can be used. The {label_name} label will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			hal_dir = label.property('hal_dir')
			if hal_dir != 'HAL_IN':
				label.setEnabled(False)
				msg = (f'{hal_dir} is not a valid\n'
				'hal_dir for a HAL Lable,\n'
				'only HAL_IN can be used for hal_dir.\n'
				f'The {label_name} Label will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			if label_name == pin_name:
				label.setEnabled(False)
				msg = (f'The object name {label_name}\n'
					'can not be the same as the\n'
					f'pin name {pin_name}.\n'
					'The HAL object will not be created\n'
					'and the label will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			if None not in [pin_name, hal_type, hal_dir]:
				hal_type = getattr(hal, f'{hal_type}')
				hal_dir = getattr(hal, f'{hal_dir}')
				setattr(parent, f'{pin_name}', parent.halcomp.newpin(pin_name, hal_type, hal_dir))
				pin = getattr(parent, f'{pin_name}')
				# if hal type is float add it to hal_float with precision
				if hal_type == 2: # HAL_FLOAT
					p = label.property('precision')
					p = p if p is not None else parent.default_precision
					parent.hal_floats[f'{label_name}'] = [pin_name, p] # label ,status item, precision
				else:
					parent.hal_readers[label_name] = pin_name

	'''
	HAL_BIT = 1
	HAL_FLOAT = 2
	HAL_S32 = 3
	HAL_U32 = 4
	HAL_IN = 16
	HAL_OUT = 32
	HAL_IO = 48
	HAL_RO = 64
	HAL_RW = 192
	'''

	if len(hal_buttons) > 0: # setup hal buttons and checkboxes
		for button in hal_buttons:
			button_name = button.objectName()
			pin_name = button.property('pin_name')
			if pin_name in dir(parent):
				button.setEnabled(False)
				msg = (f'HAL Button {button_name}\n'
				f'pin name {pin_name}\n'
				'is already used in Flex GUI\n'
				'The HAL pin can not be created.'
				f'The {button_name} button will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error')
				continue

			if button_name == pin_name:
				button.setEnabled(False)
				msg = (f'The object name {button_name}\n'
					'can not be the same as the\n'
					f'pin name {pin_name}.\n'
					'The HAL object will not be created\n'
					f'The {button_name} button will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			hal_type = button.property('hal_type')
			if hal_type != 'HAL_BIT':
				button.setEnabled(False)
				msg = (f'{hal_type} is not a valid\n'
				'hal_type for a HAL Button,\n'
				'only HAL_BIT can be used for hal_type.\n'
				f'The {button_name} button will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			hal_dir = button.property('hal_dir')
			if hal_dir != 'HAL_OUT':
				button.setEnabled(False)
				msg = (f'{hal_dir} is not a valid\n'
				'hal_dir for a HAL Button,\n'
				'only HAL_OUT can be used for hal_dir.\n'
				f'The {button_name} button will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			if None not in [pin_name, hal_type, hal_dir]:
				hal_type = getattr(hal, f'{hal_type}')
				hal_dir = getattr(hal, f'{hal_dir}')
				setattr(parent, f'{pin_name}', parent.halcomp.newpin(pin_name, hal_type, hal_dir))
				pin = getattr(parent, f'{pin_name}')

				if button.isCheckable():
					button.toggled.connect(lambda checked, pin=pin: (pin.set(checked)))
					# set the hal pin default
					setattr(parent.halcomp, pin_name, button.isChecked())
				else:
					button.pressed.connect(lambda pin=pin: (pin.set(True)))
					button.released.connect(lambda pin=pin: (pin.set(False)))

				parent.state_estop[button_name] = False
				parent.state_estop_reset[button_name] = False

				if button.property('required') == 'homed':
					parent.home_required.append(button_name)
				else:
					parent.state_on[button_name] = True

	if len(hal_spinboxes) > 0: # setup hal spinboxes
		valid_types = ['HAL_FLOAT', 'HAL_S32', 'HAL_U32']
		for spinbox in hal_spinboxes:
			spinbox_name = spinbox.objectName()
			pin_name = spinbox.property('pin_name')
			if pin_name in dir(parent):
				spinbox.setEnabled(False)
				msg = (f'HAL Spinbox {spinbox_name}\n'
				f'pin name {pin_name}\n'
				'is already used in Flex GUI\n'
				'The HAL pin can not be created.'
				f'The {spinbox_name} spinbox will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error')
				continue

			if spinbox_name == pin_name:
				spinbox.setEnabled(False)
				msg = (f'The object name {spinbox_name}\n'
					'can not be the same as the\n'
					f'pin name {pin_name}.\n'
					'The HAL object will not be created\n'
					f'The {spinbox_name} spinbox will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			hal_type = spinbox.property('hal_type')
			if hal_type not in valid_types:
				spinbox.setEnabled(False)
				msg = (f'{hal_type} is not valid\n'
				'for a HAL spinbox, only\n'
				'HAL_FLOAT or HAL_S32 or HAL_U32\n'
				f'The {spinbox_name} spinbox will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			hal_dir = spinbox.property('hal_dir')
			if hal_dir != 'HAL_OUT':
				spinbox.setEnabled(False)
				msg = (f'{hal_dir} is not a valid\n'
				'hal_dir for a HAL Spinbox,\n'
				'only HAL_OUT can be used for hal_dir.\n'
				f'The {spinbox_name} spinbox will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			if None not in [pin_name, hal_type, hal_dir]:
				hal_type = getattr(hal, f'{hal_type}')
				hal_dir = getattr(hal, f'{hal_dir}')
				parent.halcomp.newpin(pin_name, hal_type, hal_dir)
				# set the default value of the spin box to the hal pin
				setattr(parent.halcomp, pin_name, spinbox.value())
				spinbox.valueChanged.connect(partial(utilities.update_hal_spinbox, parent))
				parent.state_estop[spinbox_name] = False
				parent.state_estop_reset[spinbox_name] = False
				if parent.probe_controls: # make sure the probing_enable_pb is there
					if spinbox_name.startswith('probe_'): # don't enable it when power is on
						parent.probe_controls.append(spinbox_name)
				elif spinbox.property('required') == 'homed':
					parent.home_required.append(spinbox_name)
				else:
					parent.state_on[spinbox_name] = True

	if len(hal_sliders) > 0: # setup hal sliders
		valid_types = ['HAL_S32', 'HAL_U32']
		for slider in hal_sliders:
			slider_name = slider.objectName()
			pin_name = slider.property('pin_name')
			if pin_name in dir(parent):
				slider.setEnabled(False)
				msg = (f'HAL Slider {slider_name}\n'
				f'pin name {pin_name}\n'
				'is already used in Flex GUI\n'
				'The HAL pin can not be created.')
				f'The {slider_name} slider will be disabled.'
				dialogs.critical_msg_ok(msg, 'Configuration Error')
				continue

			if slider_name == pin_name:
				slider.setEnabled(False)
				msg = (f'The object name {slider_name}\n'
					'can not be the same as the\n'
					f'pin name {pin_name}.\n'
					'The HAL object will not be created\n'
					f'The {slider_name} slider will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			hal_type = slider.property('hal_type')
			if hal_type not in valid_types:
				slider.setEnabled(False)
				msg = (f'{hal_type} is not valid\n'
				'for a HAL slider, only\n'
				'HAL_S32 or HAL_U32 are valid\n'
				f'The {slider_name} slider will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			hal_dir = slider.property('hal_dir')
			if hal_dir != 'HAL_OUT':
				slider.setEnabled(False)
				msg = (f'{hal_dir} is not a valid\n'
				'hal_dir for a HAL Slider,\n'
				'only HAL_OUT can be used for hal_dir.\n'
				f'The {slider_name} slider will be disabled.')
				dialogs.critical_msg_ok(msg, 'Configuration Error!')
				continue

			if None not in [pin_name, hal_type, hal_dir]:
				hal_type = getattr(hal, f'{hal_type}')
				hal_dir = getattr(hal, f'{hal_dir}')
				parent.halcomp.newpin(pin_name, hal_type, hal_dir)
				# set the default value of the spin box to the hal pin
				setattr(parent.halcomp, pin_name, slider.value())
				slider.valueChanged.connect(partial(utilities.update_hal_slider, parent))
				parent.state_estop[slider_name] = False
				parent.state_estop_reset[slider_name] = False
				if parent.probe_controls: # make sure the probing_enable_pb is there
					if slider_name.startswith('probe_'): # don't enable it when power is on
						parent.probe_controls.append(slider_name)
				elif slider.property('required') == 'homed':
					parent.home_required.append(slider_name)
				else:
					parent.state_on[slider_name] = True

	parent.halcomp.ready()
	if 'hal_comp_name_lb' in parent.children:
		parent.hal_comp_name_lb.setText(f'{parent.halcomp}')

def setup_plot(parent):
	if 'plot_widget' in parent.children:
		# add the plotter to the container
		from libflexgui import flexplot
		parent.plotter = flexplot.emc_plot(parent)
		layout = QVBoxLayout(parent.plot_widget)
		layout.addWidget(parent.plotter)

		dro_font = parent.inifile.find('DISPLAY', 'DRO_FONT_SIZE') or '12'
		parent.plotter._font = f'monospace bold {dro_font}'

		#key object name, value[0] function, value[1] plot function
		plot_actions = {
		'actionDRO': ['action_toggle_dro', 'enable_dro'],
		'actionLimits': ['action_toggle_limits', 'show_limits'],
		'actionExtents_Option': ['action_toggle_extents_option', 'show_extents_option'],
		'actionLive_Plot': ['action_toggle_live_plot', 'show_live_plot'],
		'actionVelocity': ['action_toggle_velocity', 'show_velocity'],
		'actionMetric_Units': ['action_toggle_metric_units', 'metric_units'],
		'actionProgram': ['action_toggle_program', 'show_program'],
		'actionRapids': ['action_toggle_rapids', 'show_rapids'],
		'actionTool': ['action_toggle_tool', 'show_tool'],
		'actionLathe_Radius': ['action_toggle_lathe_radius', 'show_lathe_radius'],
		'actionDTG': ['action_toggle_dtg', 'show_dtg'],
		'actionOffsets': ['action_toggle_offsets', 'show_offsets'],
		'actionOverlay': ['action_toggle_overlay', 'show_overlay']
		}

		for key, value in plot_actions.items():
			if key in parent.children:
				getattr(parent, f'{key}').triggered.connect(partial(getattr(actions, f'{value[0]}'), parent))
				getattr(parent, key).setCheckable(True)
				if parent.settings.contains(f'PLOT/{key}'):
					state = True if parent.settings.value(f'PLOT/{key}') == 'true' else False
				else: # add it and set to default
					state = getattr(parent.plotter, value[1])
					parent.settings.beginGroup('PLOT')
					parent.settings.setValue(key, state)
					parent.settings.endGroup()
				getattr(parent, key).setChecked(state)
				setattr(parent.plotter, value[1], state)

		view_checkboxes = {
			'view_dro_cb': ['action_toggle_dro', 'enable_dro'],
			'view_limits_cb': ['action_toggle_limits', 'show_limits'],
			'view_extents_option_cb': ['action_toggle_extents_option', 'show_extents_option'],
			'view_live_plot_cb': ['action_toggle_live_plot', 'show_live_plot'],
			'view_velocity_cb': ['action_toggle_velocity', 'show_velocity'],
			'view_metric_units_cb': ['action_toggle_metric_units', 'metric_units'],
			'view_program_cb': ['action_toggle_program', 'show_program'],
			'view_rapids_cb': ['action_toggle_rapids', 'show_rapids'],
			'view_tool_cb': ['action_toggle_tool', 'show_tool'],
			'view_lathe_radius_cb': ['action_toggle_lathe_radius', 'show_lathe_radius'],
			'view_dtg_cb': ['action_toggle_dtg', 'show_dtg'],
			'view_offsets_cb': ['action_toggle_offsets', 'show_offsets'],
			'view_overlay_cb': ['action_toggle_overlay', 'show_overlay']
		}

		# if a checkbox is found connect it to the function
		for key, value in view_checkboxes.items():
			if key in parent.children:
				getattr(parent, f'{key}').clicked.connect(partial(getattr(actions, f'{value[0]}'), parent))
				if parent.settings.contains(f'PLOT/{key}'):
					state = True if parent.settings.value(f'PLOT/{key}') == 'true' else False
				else: # add it and set to default
					state = getattr(parent.plotter, value[1])
					parent.settings.beginGroup('PLOT')
					parent.settings.setValue(key, state)
					parent.settings.endGroup()
				getattr(parent, key).setChecked(state)
				setattr(parent.plotter, value[1], state)

		parent.plotter.update()

		view_controls = {
			'view_rotate_up_pb': ('rotateView', 0, -5),
			'view_rotate_down_pb': ('rotateView', 0, 5),
			'view_rotate_left_pb': ('rotateView', 5, 0),
			'view_rotate_right_pb': ('rotateView', -5, 0),
			'view_pan_up_pb': ('panView', 0, -5),
			'view_pan_down_pb': ('panView', 0, 5),
			'view_pan_left_pb': ('panView', -5, 0),
			'view_pan_right_pb': ('panView', 5, 0),
			'view_zoom_in_pb': ('zoomin',),
			'view_zoom_out_pb': ('zoomout',),
			'view_clear_pb': ('clear_live_plotter',)
		}

		for key, value in view_controls.items():
			if key in parent.children:
				button = getattr(parent, key)
				if len(value) == 3:
					method, vertical, horizontal = value
					button.clicked.connect(lambda _, m=method, v=vertical, h=horizontal: (
						getattr(parent.plotter, m)(vertical=v, horizontal=h)
					))
				elif len(value) == 1:
					method = value[0]
					button.clicked.connect(lambda _, m=method: (
						getattr(parent.plotter, m)()
					))

		views = {
			'view_p_pb': 'p',
			'view_x_pb': 'x',
			'view_y_pb': 'y',
			'view_y2_pb': 'y2',
			'view_z_pb': 'z',
			'view_z2_pb': 'z2'
		}

		for key, value in views.items():
			if key in parent.children:
				button = getattr(parent, key)
				button.clicked.connect(lambda _, v=value: (
					parent.plotter.makeCurrent(),
					setattr(parent.plotter, 'current_view', v),
					parent.plotter.set_current_view()
				))

def setup_fsc(parent): # mill feed and speed calculator
	if 'fsc_container' in parent.children:
		from libflexgui import fsc
		parent.fsc_calc = fsc.fs_calc()
		layout = QVBoxLayout(parent.fsc_container)
		layout.addWidget(parent.fsc_calc)
		if parent.fsc_container.property('input') == 'number':
			fsc_items = ['fsc_diameter_le', 'fsc_rpm_le', 'fsc_flutes_le', 'fsc_feed_le', 'fsc_chip_load_le']
			for item in fsc_items:
				getattr(parent.fsc_calc, f'{item}').installEventFilter(parent)
				parent.number_le.append(item)

def setup_dsf(parent): # drill speed and feed calculator
	if 'dsf_container' in parent.children:
		from libflexgui import dsf
		parent.dsf_calc = dsf.dsf_calc()
		layout = QVBoxLayout(parent.dsf_container)
		layout.addWidget(parent.dsf_calc)
		if parent.dsf_container.property('input') == 'number':
			dsf_items = ['dfs_diameter_le', 'dfs_surface_speed_le']
			for item in dsf_items:
				getattr(parent.dsf_calc, f'{item}').installEventFilter(parent)
				parent.number_le.append(item)

def setup_import(parent):
	module_name = parent.inifile.find('FLEX', 'IMPORT') or False
	if module_name: # import the module
		try:
			sys.path.append(parent.ini_path)
			module = importlib.import_module(module_name)
			module.startup(parent)
		except:
			msg = (f'The file {module_name} was\n'
				'not found, check for file name\n'
				'or there was an error in the imported\n'
				'module code.')
			dialogs.warn_msg_ok(msg, 'Import Failed')

def set_status(parent): # this is only used if running from a terminal
	parent.status.poll()
	if parent.status.task_state == linuxcnc.STATE_ESTOP:
		for key, value in parent.state_estop.items():
			getattr(parent, key).setEnabled(value)
		for key, value in parent.state_estop_names.items():
			getattr(parent, key).setText(value)
		if parent.estop_open_color: # if False just don't bother
			if 'estop_pb' in parent.children:
				open_color = f'QPushButton{{background-color: {parent.estop_open_color};}}'
				parent.estop_pb.setStyleSheet(open_color)
			if 'flex_E_Stop' in parent.children:
				open_color = f'QToolButton{{background-color: {parent.estop_open_color};}}'
				parent.flex_E_Stop.setStyleSheet(open_color)
		if parent.power_off_color: # if False just don't bother
			if 'power_pb' in parent.children:
				off_color = f'QPushButton{{background-color: {parent.power_off_color};}}'
				parent.power_pb.setStyleSheet(off_color)
			if 'flex_Power' in parent.children:
				off_color = f'QToolButton{{background-color: {parent.power_off_color};}}'
				parent.flex_Power.setStyleSheet(off_color)

	# this state can only happen when runnning with a sim
	if parent.status.task_state == linuxcnc.STATE_ESTOP_RESET:
		for key, value in parent.state_estop_reset.items():
			getattr(parent, key).setEnabled(value)
		for key, value in parent.state_estop_reset_names.items():
			getattr(parent, key).setText(value)
		if parent.estop_closed_color: # if False just don't bother
			if 'estop_pb' in parent.children:
				closed_color = f'QPushButton{{background-color: {parent.estop_closed_color};}}'
				parent.estop_pb.setStyleSheet(closed_color)
			if 'flex_E_Stop' in parent.children:
				closed_color = f'QToolButton{{background-color: {parent.estop_closed_color};}}'
				parent.flex_E_Stop.setStyleSheet(closed_color)
		if parent.power_off_color: # if False just don't bother
			if 'power_pb' in parent.children:
				off_color = f'QPushButton{{background-color: {parent.power_off_color};}}'
				parent.power_pb.setStyleSheet(off_color)
			if 'flex_Power' in parent.children:
				off_color = f'QToolButton{{background-color: {parent.power_off_color};}}'
				parent.flex_Power.setStyleSheet(off_color)

	if parent.status.task_state == linuxcnc.STATE_ON:
		for key, value in parent.state_on.items():
			getattr(parent, key).setEnabled(value)
		for key, value in parent.state_on_names.items():
			getattr(parent, key).setText(value)
		if utilities.all_homed and parent.status.file:
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(True)
		if parent.estop_closed_color: # if False just don't bother
			if 'estop_pb' in parent.children:
				closed_color = f'QPushButton{{background-color: {parent.estop_closed_color};}}'
				parent.estop_pb.setStyleSheet(closed_color)
			if 'flex_E_Stop' in parent.children:
				closed_color = f'QToolButton{{background-color: {parent.estop_closed_color};}}'
				parent.flex_E_Stop.setStyleSheet(closed_color)
		if parent.power_on_color: # if False just don't bother
			if 'power_pb' in parent.children:
				on_color = f'QPushButton{{background-color: {parent.power_on_color};}}'
				parent.power_pb.setStyleSheet(on_color)
			if 'flex_Power' in parent.children:
				on_color = f'QToolButton{{background-color: {parent.power_on_color};}}'
				parent.flex_Power.setStyleSheet(on_color)
		if utilities.all_homed(parent):
			for item in parent.unhome_controls:
				getattr(parent, item).setEnabled(True)
			for item in parent.home_controls:
				getattr(parent, item).setEnabled(False)
		elif utilities.all_unhomed(parent):
			for item in parent.unhome_controls:
				getattr(parent, item).setEnabled(False)
		else:
			for item in parent.home_required:
				getattr(parent, item).setEnabled(False)
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(False)
			for item in parent.home_controls: # enable/disable by joint
				if item[-1].isnumeric():
					joint = int(item[-1])
					if parent.status.homed[joint] == 0: # not homed
						getattr(parent, item).setEnabled(True)
					elif parent.status.homed[joint] == 1: # homed
						getattr(parent, item).setEnabled(False)
			for item in parent.unhome_controls:
				if item[-1].isnumeric():
					joint = int(item[-1])
					if parent.status.homed[joint] == 0: # not homed
						getattr(parent, item).setEnabled(False)
					elif parent.status.homed[joint] == 1: # homed
						getattr(parent, item).setEnabled(True)

	open_file = parent.inifile.find('DISPLAY', 'OPEN_FILE') or False
	if open_file and open_file != '""':
		if open_file.startswith('./'):
			open_file = os.path.join(parent.ini_path, open_file.lstrip('./'))
		elif open_file.startswith('~'):
			open_file = open_file.replace('~', parent.home_dir)
		else: # full path
			open_file = open_file
		if os.path.exists(open_file):
			actions.load_file(parent, open_file)
		else:
			msg = (f'The G code file\n{open_file}\n'
				'was not found.\n'
				'Check the [DISPLAY] OPEN_FILE\n'
				'setting in the ini file.')

			dialogs.warn_msg_ok(msg, 'File Not Found')


