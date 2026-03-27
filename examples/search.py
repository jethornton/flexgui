#!/usr/bin/env python3

import re
	
def extract_button_names(file_path):
	"""
	Finds all lines in a file that contain 'widget class="QPushButton"' 
	and extracts the value of the 'name' attribute.

	Args:
		file_path (str): The path to the input file.

	Returns:
		list: A list of extracted 'name' attribute values.
	"""

	QLabels = ['acceleration_lb', 'active_queue_lb', 'actual_position_lb',
	'adaptive_feed_enabled_lb', 'ain_lb', 'angular_units_lb', 'aout_lb',
	'axis_lb', 'axis_mask_lb', 'block_delete_lb', 'call_level_lb', 'command_lb',
	'current_line_lb', 'current_vel_lb', 'cycle_time_lb', 'debug_lb',
	'delay_left_lb', 'din_lb', 'distance_to_go_lb', 'echo_serial_number_lb',
	'enabled_lb', 'estop_lb', 'exec_state_lb', 'feed_hold_enabled_lb',
	'feed_override_lb', 'file_lb', 'flood_lb', 'g5x_index_lb', 'g5x_offset_lb',
	'gcodes_lb', 'homed_lb', 'ini_filename_lb', 'inpos_lb', 'input_timeout_lb',
	'interp_state_lb', 'interpreter_errcode_lb', 'joint', 'joint_actual_position',
	'joint_position', 'joints_lb', 'kinematics_type_lb', 'limit',
	'linear_units_lb', 'lube_lb', 'lube_level_lb', 'machine_units_lb',
	'max_acceleration_lb', 'max_velocity_lb', 'min_jog_vel_lb', 'max_jog_vel_lb',
	'mcodes_lb', 'mist_lb', 'motion_line_lb', 'motion_mode_lb', 'motion_type_lb',
	'optional_stop_lb', 'paused_lb', 'pocket_prepped_lb', 'position_lb',
	'probe_tripped_lb', 'probe_val_lb', 'probed_position_lb', 'probing_lb',
	'program_units_lb', 'queue_lb', 'queue_full_lb', 'rapid_override_lb',
	'rapidrate_lb', 'read_line_lb', 'rotation_xy_lb', 'spindle_lb', 'spindles_lb',
	'state_lb', 'task_mode_lb', 'task_paused_lb', 'task_state_lb',
	'tool_in_spindle_lb', 'tool_from_pocket_lb', 'tool_offset_lb', 'tool_table_lb']

	QSliders = ['feed_override_sl', 'rapid_override_sl', 'spindle_override_sl',
	'jog_vel_sl']

	QActions = ['actionOpen', 'actionEdit', 'actionReload', 'actionSave_As',
		'actionEdit_Tool_Table', 'actionReload_Tool_Table', 'actionLadder_Editor',
		'actionQuit', 'actionE_Stop', 'actionPower', 'actionRun',
		'actionRun_From_Line', 'actionStep', 'actionPause', 'actionResume',
		'actionStop', 'actionClear_MDI_History', 'actionCopy_MDI_History',
		'actionShow_HAL', 'actionHAL_Meter', 'actionHAL_Scope', 'actionDRO',
		'actionLimits', 'actionExtents_Option', 'actionLive_Plot', 'actionVelocity',
		'actionMetric_Units', 'actionProgram', 'actionRapids', 'actionTool',
		'actionLathe_Radius', 'actionDTG', 'actionOffsets', 'actionOverlay',
		'actionClear_Live_Plot', 'actionAbout', 'actionQuick_Reference']

	QCheckBoxes = ['view_dro_cb', 'view_limits_cb', 'view_extents_option_cb',
	'view_live_plot_cb', 'view_velocity_cb', 'view_metric_units_cb',
	'view_program_cb', 'view_rapids_cb', 'view_tool_cb', 'view_lathe_radius_cb',
	'view_dtg_cb', 'view_offsets_cb', 'view_overlay_cb', 'keyboard_jog_cb',
	'override_limits_cb']
	
	QPushButtons = ['open_pb', 'edit_pb', 'reload_pb', 'edit_tool_table_pb',
	'edit_ladder_pb', 'reload_tool_table_pb', 'save_pb', 'save_as_pb', 'quit_pb',
	'estop_pb', 'power_pb', 'run_pb', 'run_from_line_pb', 'step_pb', 'pause_pb',
	'resume_pb', 'stop_pb', 'home_all_pb', 'home_pb_0', 'unhome_all_pb',
	'unhome_pb_0', 'clear_x', 'manual_mode_pb', 'probing_enable_pb', 'flood_pb',
	'mist_pb', 'optional_stop_pb', 'block_delete_pb', 'feed_override_pb',
	'clear_errors_pb', 'copy_errors_pb', 'clear_info_pb',
	'show_hal_pb', 'hal_meter_pb', 'hal_scope_pb', 'about_pb',
	'quick_reference_pb', 'clear_coord_0', 'clear_coord_1', 'clear_x_pb',
	'feed_percent_100', 'rapid_percent_100', 'spindle_percent_100',
	'jog_plus_pb_0', 'jog_minus_pb_0', 'run_mdi_pb', 'touchoff_pb_x',
	'copy_mdi_history_pb', 'save_mdi_history_pb', 'clear_mdi_history_pb',
	'tool_change_pb', 'tool_change_pb_1', 'tool_touchoff_selected_pb']

	found_buttons = []
	found_checkboxes = []
	found_actions = []
	found_sliders = []
	found_labels = []

	# Use a raw string for the regex pattern for correct backslash handling.
	# Pattern explanation:
	# r'...' - Raw string literal
	# .*? - Match any character non-greedily until the next part
	# widget class="QPushButton" - Match the literal target string
	# .*? - Match any character non-greedily until the name attribute
	# name=" - Match the literal 'name="' part
	# (.*?) - Capture group 1: capture any character non-greedily (the name value)
	# " - Match the closing quote
	button_pattern = re.compile(r'.*?class="QPushButton".*?name="(.*?)".*?')
	# <widget class="QPushButton" name="open_pb">
	checkbox_pattern = re.compile(r'.*?class="QCheckBox".*?name="(.*?)".*?')
	# <widget class="QCheckBox" name="checkBox">
	action_pattern = re.compile(r'.*?addaction .*?name="(.*?)".*?')
	# <addaction name="actionOpen"/>
	slider_pattern = re.compile(r'.*?class="QSlider".*?name="(.*?)".*?')
	# <widget class="QSlider" name="spindle_override_sl">
	label_pattern = re.compile(r'.*?class="QLabel".*?name="(.*?)".*?')
	# <widget class="QLabel" name="label_4">

	try:
		# Iterate over lines in the file efficiently without reading the whole file into memory.
		with open(file_path, 'r') as file:
			for line in file:
				# match QPushButton
				match = button_pattern.search(line)
				if match:
					# Extract the captured group (the value inside the quotes).
					if match.group(1) in QPushButtons:
						found_buttons.append(match.group(1))
				# match QCheckBox
				match = checkbox_pattern.search(line)
				if match:
					# Extract the captured group (the value inside the quotes).
					if match.group(1) in QCheckBoxes:
						found_checkboxes.append(match.group(1))
				# match QAction
				match = action_pattern.search(line)
				if match:
					# Extract the captured group (the value inside the quotes).
					if match.group(1) in QActions:
						found_actions.append(match.group(1))
				# match QSlider
				match = slider_pattern.search(line)
				if match:
					# Extract the captured group (the value inside the quotes).
					if match.group(1) in QSliders:
						found_sliders.append(match.group(1))
				# match QLabel
				match = label_pattern.search(line)
				if match:
					# Extract the captured group (the value inside the quotes).
					if match.group(1) in QLabels:
						found_labels.append(match.group(1))

	except FileNotFoundError:
		print(f"Error: The file '{file_path}' was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")

	# find missing widgets
	buttons = list(set(QPushButtons) - set(found_buttons))
	checkboxes = list(set(QCheckBoxes) - set(found_checkboxes))
	actions = list(set(QActions) - set(found_actions))
	sliders = list(set(QSliders) - set(found_sliders))
	labels = list(set(QLabels) - set(found_labels))

	return buttons, checkboxes, actions, sliders, labels

# Example Usage:
# Assume your file is named 'ui_layout.txt' and contains lines like:
# <widget class="QPushButton" name="myButton1">
# <widget class="QCheckBox" name="myCheckBox">
# <widget class="QPushButton" name="anotherButton_ok">

# set the file path here
file_name = '/home/john/github/flexgui/examples/features/status/status.ui'
#file_name = '/home/john/github/flexgui/examples/testgui/test.ui'
buttons, checkboxes, actions, sliders, labels = extract_button_names(file_name)

print(f'Searching {file_name}')

if buttons:
	print(f'Missing names for QPushButton widgets in "{file_name}":')
	for name in buttons:
		print(f'{name}')
else:
	print('No missing QPushButton widgets')

if checkboxes:
	print(f'Missing names for QCheckBox widgets in "{file_name}":')
	for name in checkboxes:
		print(f'{name}')
else:
	print('No missing QCheckBox widgets')

if actions:
	print(f'Missing names for QAction widgets in "{file_name}":')
	for name in actions:
		print(f'{name}')
else:
	print('No missing QAction widgets')

if sliders:
	print(f'Missing names for QSlider widgets in "{file_name}":')
	for name in sliders:
		print(f'{name}')
else:
	print('No missing QSlider widgets')

if labels:
	print(f'Missing names for QLabel widgets in "{file_name}":')
	for name in labels:
		print(f'{name}')
else:
	print('No missing QLabel widgets')

