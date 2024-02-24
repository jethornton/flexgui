import os
from functools import partial

from PyQt6.QtWidgets import QLabel, QPushButton, QListWidget, QPlainTextEdit
from PyQt6.QtWidgets import QComboBox, QSlider
from PyQt6.QtGui import QAction

from libflexgui import actions

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
	'actionEdit_Tools': 'action_edit_tools', 'actionReload_Tools': 'action_reload_tools',
	'actionQuit': 'action_quit', 'actionClear_MDI': 'action_clear_mdi',
	'actionShow_HAL': 'action_show_hal', 'actionHal_Meter': 'action_hal_meter',
	'actionHal_Scope': 'action_hal_scope'}

	# if an action is found connect it to the function
	for key, value in actions_dict.items():
		if parent.findChild(QAction, f'{key}'):
			getattr(parent, f'{key}').triggered.connect(partial(getattr(actions, f'{value}'), parent))

def setup_enables(parent):
	parent.status.poll()
	estop = ['power_pb']
	parent.estop_enables = []
	for control in estop:
		if parent.findChild(QPushButton, control):
			parent.estop_enables.append(control)
	for item in parent.estop_enables:
		getattr(parent, item).setEnabled(False)

	#file_name = parent.status.file
	run_buttons = ['run_pb', 'step_pb', 'pause_pb', 'resume_pb',]
	parent.run_enables = []
	for button in run_buttons:
		if parent.findChild(QPushButton, button):
			parent.run_enables.append(button)
	for item in parent.run_enables:
		getattr(parent, item).setEnabled(False)

	power = ['run_mdi_pb', 'start_spindle_pb', 'flood_pb', 'mist_pb',]
	parent.power_enables = []
	for control in power:
		if parent.findChild(QPushButton, control):
			parent.power_enables.append(control)
	for item in parent.power_enables:
		getattr(parent, item).setEnabled(False)

	home = []
	for i in range(9):
		home.append(f'home_pb_{i}')
	parent.home_enables = []
	for button in home:
		if parent.findChild(QPushButton, button):
			parent.home_enables.append(button)
	for item in parent.home_enables:
		getattr(parent, item).setEnabled(False)

	unhome = ['unhome_all_pb']
	for i in range(9):
		unhome.append(f'unhome_pb_{i}')
	parent.unhome_enables = []
	for control in unhome:
		if parent.findChild(QPushButton, control):
			parent.unhome_enables.append(control)
	for item in parent.unhome_enables:
		getattr(parent, item).setEnabled(False)

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

	# check for status labels in ui
	parent.status_labels = {} # create an empty dictionary
	for item in status_items: # iterate the status items list
		if parent.findChild(QLabel, f'{item}_lb'): # if the label is found
			# parent.status_labels['acceleration'] = 'acceleration_lb'
			parent.status_labels[item] = f'{item}_lb' # add the status and label

	# check for axis labels in ui
	# these return tuples of xyzabcuvw axes
	axis_items = ['max_position_limit', 'min_position_limit', 'velocity']
	parent.status_axes = {}
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
	parent.status_joints = {}
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



