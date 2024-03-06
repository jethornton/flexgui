import os
from functools import partial

from PyQt6.QtWidgets import QLabel, QPushButton, QListWidget, QPlainTextEdit
from PyQt6.QtWidgets import QComboBox, QSlider, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import QSettings

import hal

from libflexgui import actions
from libflexgui import commands

def load_postgui(parent): # load post gui hal and tcl files if found
	postgui_halfiles = parent.inifile.findall("HAL", "POSTGUI_HALFILE") or None
	if postgui_halfiles is not None:
		for f in postgui_halfiles:
			if f.lower().endswith('.tcl'):
				res = os.spawnvp(os.P_WAIT, "haltcl", ["haltcl", "-i", parent.ini_path, f])
			else:
				res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i", parent.ini_path, "-f", f])
			if res: raise SystemExit(res)

def setup_actions(parent): # setup menu actions
	actions_dict = {'actionOpen': 'action_open', 'actionRecent': 'action_recent',
		'actionEdit': 'action_edit', 'actionReload': 'action_reload',
		'actionSave_As': 'action_save_as',
		'actionEdit_Tool_Table': 'action_edit_tool_table',
		'actionReload_Tool_Table': 'action_reload_tool_table',
		'actionLadder_Editor': 'action_ladder_editor', 'actionQuit': 'action_quit',
		'actionClear_MDI': 'action_clear_mdi', 'actionCopy_MDI': 'action_copy_mdi',
		'actionShow_HAL': 'action_show_hal', 'actionHAL_Meter': 'action_hal_meter',
		'actionHAL_Scope': 'action_hal_scope', 'actionAbout': 'action_about',
		'actionQuick_Reference': 'action_quick_reference'}

	# if an action is found connect it to the function
	for key, value in actions_dict.items():
		if parent.findChild(QAction, f'{key}'):
			getattr(parent, f'{key}').triggered.connect(partial(getattr(actions, f'{value}'), parent))

	# special check for the classicladder editor
	if parent.findChild(QAction, 'actionLadder_Editor'):
		if not hal.component_exists("classicladder_rt"):
			parent.actionLadder_Editor.setEnabled(False)


def setup_recent_files(parent):
	# add the Recent menu FIXME look for file open then add before next action
	actions_found = parent.findChildren(QAction)
	for action in actions_found:
		if action.objectName() == 'actionEdit':
			parent.menuRecent = QMenu('Recent', parent)
			parent.menuFile.insertMenu(action, parent.menuRecent)
			#print(type(parent.menuRecent))

	# if any files have been opened add them
	keys = parent.settings.allKeys()
	for key in keys:
		if key.startswith('recent_files'):
			path = parent.settings.value(key)
			name = os.path.basename(path)
			a = parent.menuRecent.addAction(name)
			a.triggered.connect(partial(getattr(actions, 'load_file'), parent, path))
			#a.triggered.connect(actions.action_test)

def setup_enables(parent):
	# just disable all controls except estop at startup
	control_list = ['power_pb', 'run_pb', 'step_pb', 'pause_pb', 'resume_pb',
		'stop_pb', 'home_all_pb', 'unhome_all_pb', 'run_mdi_pb', 'start_spindle_pb',
		'stop_spindle_pb', 'spindle_plus_pb', 'spindle_minus_pb', 'flood_pb',
		'mist_pb']
	home_items = ['home_pb_', 'unhome_pb_']
	for item in home_items:
		for i in range(9):
			control_list.append(f'{item}{i}')
	for item in control_list:
		if parent.findChild(QPushButton, item):
			getattr(parent, item).setEnabled(False)

	parent.status.poll()
	estop = ['power_pb']
	parent.estop_enables = []
	for control in estop:
		if parent.findChild(QPushButton, control):
			parent.estop_enables.append(control)

	#file_name = parent.status.file
	run_buttons = ['run_pb', 'step_pb', 'pause_pb', 'resume_pb',]
	parent.run_enables = []
	for button in run_buttons:
		if parent.findChild(QPushButton, button):
			parent.run_enables.append(button)

	power = ['start_spindle_pb', 'flood_pb', 'mist_pb',]
	parent.power_enables = []
	for control in power:
		if parent.findChild(QPushButton, control):
			parent.power_enables.append(control)

	home = []
	for i in range(9):
		home.append(f'home_pb_{i}')
	parent.home_enables = []
	for button in home:
		if parent.findChild(QPushButton, button):
			parent.home_enables.append(button)

	unhome = ['unhome_all_pb']
	for i in range(9):
		unhome.append(f'unhome_pb_{i}')
	parent.unhome_enables = []
	for control in unhome:
		if parent.findChild(QPushButton, control):
			parent.unhome_enables.append(control)

	parent.home_all_ok = False
	home_all = False
	for i in range(parent.status.joints): # enable/disable home all
		if parent.inifile.find(f'JOINT_{i}', "HOME_SEQUENCE"):
			home_all = True
		else:
			home_all = False
			break
	if parent.findChild(QPushButton, 'home_all_pb'):
		parent.home_all_pb.setEnabled(False)
		parent.home_all_ok = home_all

	if parent.findChild(QPushButton, 'run_mdi_pb'):
		parent.run_mdi_pb.setEnabled(False)

def setup_status_labels(parent):
	status_items = ['acceleration', 'active_queue', 
	'adaptive_feed_enabled', 'angular_units', 'axes', 'axis',
	'axis_mask', 'block_delete', 'call_level', 'command', 'current_line',
	'current_vel', 'cycle_time', 'debug', 'delay_left', 'distance_to_go',
	'echo_serial_number', 'enabled', 'estop', 'exec_state',
	'feed_hold_enabled', 'feed_override_enabled', 'feedrate', 'file', 'flood',
	'g5x_index',
	'ini_filename', 'inpos', 'input_timeout', 'interp_state',
	'interpreter_errcode', 'joint',
	'joints', 'kinematics_type', 'linear_units', 'lube', 'lube_level',
	'max_acceleration', 'max_velocity', 'mcodes', 'mist', 'motion_line',
	'motion_mode', 'motion_type', 'optional_stop', 'paused', 'pocket_prepped',
	'probe_tripped', 'probe_val', 'probed_position', 'probing',
	'program_units', 'queue', 'queue_full', 'rapidrate', 'read_line',
	'rotation_xy', 'settings', 'spindle', 'spindles', 'state', 'task_mode',
	'task_paused', 'task_state', 'tool_in_spindle', 'tool_from_pocket',
	'tool_offset', 'tool_table', 'velocity']

	# check for status labels in the ui
	parent.status_labels = {} # create an empty dictionary
	for item in status_items: # iterate the status items list
		if parent.findChild(QLabel, f'{item}_lb'): # if the label is found
			# parent.status_labels['acceleration'] = 'acceleration_lb'
			parent.status_labels[item] = f'{item}_lb' # add the status and label

	dro_items = ['dro_lb_x', 'dro_lb_y', 'dro_lb_z', 'dro_lb_a', 'dro_lb_b',
		'dro_lb_c', 'dro_lb_u', 'dro_lb_v', 'dro_lb_w']
	parent.status_dro = {} # create an empty dictionary
	# check for dro labels in the ui
	for i, item in enumerate(dro_items):
		if parent.findChild(QLabel, f'{item}'): # if the label is found
			p = getattr(parent, item).property('precision')
			p = p if p is not None else 3
			parent.status_dro[f'{item}'] = [i, p] # add the label, tuple position & precision

	g5x_items = ['g5x_lb_x', 'g5x_lb_y', 'g5x_lb_z', 'g5x_lb_a', 'g5x_lb_b',
		'g5x_lb_c', 'g5x_lb_u', 'g5x_lb_v', 'g5x_lb_w']
	parent.status_g5x = {} # create an empty dictionary
	# check for g5x offset labels in the ui
	for i, item in enumerate(g5x_items):
		if parent.findChild(QLabel, f'{item}'): # if the label is found
			p = getattr(parent, item).property('precision')
			p = p if p is not None else 3
			parent.status_g5x[f'{item}'] = [i, p] # add the label, tuple position & precision

	g92_items = ['g92_lb_x', 'g92_lb_y', 'g92_lb_z', 'g92_lb_a', 'g92_lb_b',
		'g92_lb_c', 'g92_lb_u', 'g92_lb_v', 'g92_lb_w']
	parent.status_g92 = {} # create an empty dictionary
	# check for g5x offset labels in the ui
	for i, item in enumerate(g92_items):
		if parent.findChild(QLabel, f'{item}'): # if the label is found
			p = getattr(parent, item).property('precision')
			p = p if p is not None else 3
			parent.status_g92[f'{item}'] = [i, p] # add the label, tuple position & precision

	# check for axis labels in the ui FIXME precision velocity
	# these return tuples of xyzabcuvw axes
	axis_items = ['max_position_limit', 'min_position_limit', 'velocity']
	parent.status_axes = {} # create an empty dictionary
	parent.status.poll()
	for i in range(parent.status.axis_mask.bit_count()): # only check for axes that exist
		for item in axis_items:
			if parent.findChild(QLabel, f'axis_{item}_{i}_lb'): # if the label is found
				parent.status_axes[f'{item}_{i}'] = f'axis_{item}_{i}_lb' # add the status and label

	# check for joint labels in ui
	# these return 16 joints
	joint_items = ['backlash', 'enabled', 'fault', 'ferror_current',
	'ferror_highmark', 'homed', 'homing', 'inpos', 'input', 'jointType',
	'max_ferror', 'max_hard_limit', 'max_position_limit', 'max_soft_limit',
	'min_ferror', 'min_hard_limit', 'min_position_limit', 'min_soft_limit',
	'output', 'override_limits', 'units', 'velocity']
	parent.status_joints = {} # create an empty dictionary
	for i in range(9):
		for item in joint_items:
			if parent.findChild(QLabel, f'joint_{item}_{i}_lb'):
				parent.status_joints[f'{item}_{i}'] = f'joint_{item}_{i}_lb'

	# check for analog and digital labels in ui
	# these return 64 items each
	io_items = ['ain', 'aout', 'din', 'dout']
	parent.status_io = {}
	for i in range(64):
		for item in io_items:
			if parent.findChild(QLabel, f'{item}_{i}_lb'):
				parent.status_io[f'{item}_{i}'] = f'{item}_{i}_lb'

	# check for spindle labels in ui
	spindle_items = ['brake', 'direction', 'enabled', 'homed',
	'orient_fault', 'orient_state', 'override', 'override_enabled', 'speed']
	parent.status_spindles = {}
	parent.status.poll()
	 # only look for the num of spindles configured
	for i in range(parent.status.spindles):
		for item in spindle_items:
			if parent.findChild(QLabel, f'spindle_{item}_{i}_lb'):
				parent.status_spindles[f'{item}_{i}'] = f'spindle_{item}_{i}_lb'

	tool_table_items = ['id', 'xoffset', 'yoffset', 'zoffset', 'aoffset',
		'boffset', 'coffset', 'uoffset', 'voffset', 'woffset', 'diameter',
		'frontangle', 'backangle', 'orientation']
	parent.tool_table = {}
	parent.status.poll()
	for i in range(len(parent.status.tool_table)):
		for item in tool_table_items:
			if parent.findChild(QLabel, f'tool_table_{item}_{i}_lb'):
				parent.tool_table[f'{item}_{i}'] = f'tool_table_{item}_{i}_lb'

def setup_list_widgets(parent):
	list_widgets = ['mdi_history_lw']
	for item in list_widgets:
		if parent.findChild(QListWidget, item) is not None:
			setattr(parent, f'{item}_exists', True)
		else:
			setattr(parent, f'{item}_exists', False)

def setup_plain_text_edits(parent):
	plain_text_edits = ['gcode_pte', 'errors_pte']
	for item in plain_text_edits:
		if parent.findChild(QPlainTextEdit, item) is not None:
			setattr(parent, f'{item}_exists', True)
		else:
			setattr(parent, f'{item}_exists', False)

def setup_combo_boxes(parent):
	combo_boxes = ['jog_modes_cb']
	for item in combo_boxes:
		if parent.findChild(QComboBox, item) is not None:
			setattr(parent, f'{item}_exists', True)
		else:
			setattr(parent, f'{item}_exists', False)

def setup_sliders(parent):
	sliders = ['jog_vel_s']
	for item in sliders:
		if parent.findChild(QSlider, item) is not None:
			setattr(parent, f'{item}_exists', True)
		else:
			setattr(parent, f'{item}_exists', False)

def setup_buttons(parent):
	control_buttons = {'abort_pb': 'abort',
	'estop_pb': 'estop_toggle',
	'power_pb': 'power_toggle',
	'run_pb': 'run',
	'manual_mode_pb':'set_mode_manual',
	'step_pb': 'step',
	'pause_pb': 'pause',
	'resume_pb': 'resume',
	'stop_pb': 'stop',
	'home_all_pb': 'home_all',
	'home_pb_0': 'home',
	'home_pb_1': 'home',
	'home_pb_2': 'home',
	'unhome_all_pb': 'unhome_all',
	'unhome_pb_0': 'unhome',
	'unhome_pb_1': 'unhome',
	'unhome_pb_2': 'unhome',
	'run_mdi_pb': 'run_mdi',
	'touchoff_pb_x': 'touchoff',
	'touchoff_pb_y': 'touchoff',
	'touchoff_pb_z': 'touchoff',
	'x_tool_touchoff_pb': 'tool_touchoff',
	'y_tool_touchoff_pb': 'tool_touchoff',
	'z_tool_touchoff_pb': 'tool_touchoff',
	'tool_change_pb':  'tool_change',
	'start_spindle_pb': 'spindle',
	'stop_spindle_pb': 'spindle',
	'spindle_plus_pb': 'spindle',
	'spindle_minus_pb': 'spindle',
	'flood_pb': 'flood_toggle',
	'mist_pb': 'mist_toggle',
	}

	for i in range(16):
		control_buttons[f'jog_plus_pb_{i}'] = 'jog'
		control_buttons[f'jog_minus_pb_{i}'] = 'jog'

	for key, value in control_buttons.items():
		if parent.findChild(QPushButton, key):
			getattr(parent, key).clicked.connect(partial(getattr(commands, value), parent))

	return

	special_buttons = {
	'numberpad_pb_0': 'number_pad',
	'numberpad_pb_1': 'number_pad',
	'numberpad_pb_2': 'number_pad',
	'gcode_pad_pb': 'gcode_pad',
	}
	for pb in pushbuttons:
		if pb in special_buttons:
			getattr(parent, pb).clicked.connect(getattr(parent, special_buttons[pb]))

	if 'exit_pb' in pushbuttons:
		#parent.exit_pb.setVisible(False)
		parent.exit_pb.setFlat(True)
		parent.exit_pb.pressed.connect(parent.close)


def setup_misc(parent):
	list_widgets = {'mdi_history_lw': 'add_mdi'}
	list_widgets_list = []
	for list_widget in parent.findChildren(QListWidget):
		if list_widget.objectName():
			list_widgets_list.append(list_widget.objectName())

	for item in list_widgets_list:
		if item in list_widgets:
			getattr(parent, item).itemSelectionChanged.connect(partial(getattr(utilities, list_widgets[item]), parent))

	sliders = {
	'jog_vel_s': 'jog_slider'}

	slider_list = []
	for slider in parent.findChildren(QSlider):
		if slider.objectName():
			slider_list.append(slider.objectName())

	for item in slider_list:
		if item in sliders:
			getattr(parent, item).valueChanged.connect(partial(getattr(utilities, sliders[item]), parent))

	line_edit_list = []
	for line_edit in parent.findChildren(QLineEdit):
		if line_edit.objectName():
			line_edit_list.append(line_edit.objectName())

	line_edits = {'touchoff_le': '', 'mdi_command_le': 'run_mdi'}

	for item in line_edit_list:
		if item in line_edits:
			getattr(parent, item).returnPressed.connect(partial(getattr(commands, line_edits[item]), parent))

	utility_list = {'clear_mdi_history_pb': 'clear_mdi_history'}

	for item in utility_list:
		if item in pushbuttons:
			getattr(parent, item).clicked.connect(partial(getattr(utilities, utility_list[item]), parent))

	# combo boxes
	combo_dict = {'jog_mode_cb': 'load_jog_modes'}


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


