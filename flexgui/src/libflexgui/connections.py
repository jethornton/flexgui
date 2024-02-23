from functools import partial

from PyQt6.QtWidgets import QPushButton, QPlainTextEdit, QListWidget, QSlider
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QAction

from libflexgui import commands
from libflexgui import menus
from libflexgui import editor
from libflexgui import utilities

def connect_controls(parent):
	controls = {'abort_pb': 'abort',
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

	pushbuttons = []
	children = parent.findChildren(QPushButton)
	for child in children:
		pushbuttons.append(child.objectName())

	for pb in pushbuttons:
		if pb in controls:
			getattr(parent, pb).clicked.connect(partial(getattr(commands, controls[pb]), parent))

	jog_buttons = {
	'jog_plus_pb_0': 'jog',
	'jog_minus_pb_0': 'jog',
	'jog_plus_pb_1': 'jog',
	'jog_minus_pb_1': 'jog',
	'jog_plus_pb_2': 'jog',
	'jog_minus_pb_2': 'jog',
	}

	for pb in pushbuttons:
		if pb in jog_buttons:
			getattr(parent, pb).pressed.connect(partial(getattr(commands, jog_buttons[pb]), parent))
			getattr(parent, pb).released.connect(partial(getattr(commands, jog_buttons[pb]), parent))

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

	# Menu Items
	menu_actions = {'actionOpen': 'file_open',
	'actionReload': 'file_reload',
	'actionExit': 'app_close',
	'actionClear_MDI': 'clear_mdi',
	'actionShow_HAL': 'show_hal',
	'actionReload_Tooltable': 'load_tool_table'}

	action_list = []
	for action in parent.findChildren(QAction):
		if action.objectName():
			action_list.append(action.objectName())

	for action in action_list:
		if action in menu_actions:
			getattr(parent, action).triggered.connect(partial(getattr(menus, menu_actions[action]), parent))

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


	# plain text edits
	# ptes = {'gcode_pte': 'gcode_viewer'}
	#if isinstance(parent.findChild(QPlainTextEdit, 'gcode_pte'), QPlainTextEdit):
	#if parent.findChild(QPlainTextEdit, 'gcode_pte'):
	#./	parent.gcode_pte.cursorPositionChanged.connect(partial(editor.highlight_line, parent))


