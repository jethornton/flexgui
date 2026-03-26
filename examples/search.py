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

	<widget class="QPushButton" name="open_pb">
	<widget class="QCheckBox" name="checkBox">
	<addaction name="actionOpen"/>
	"""

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

	# Use a raw string for the regex pattern for correct backslash handling.
	# Pattern explanation:
	# r'...' - Raw string literal
	# .*? - Match any character non-greedily until the next part
	# widget class="QPushButton" - Match the literal target string
	# .*? - Match any character non-greedily until the name attribute
	# name=" - Match the literal 'name="' part
	# (.*?) - Capture group 1: capture any character non-greedily (the name value)
	# " - Match the closing quote
	button_pattern = re.compile(r'.*?widget class="QPushButton".*?name="(.*?)".*?')
	checkbox_pattern = re.compile(r'.*?widget class="QCheckBox".*?name="(.*?)".*?')
	action_pattern = re.compile(r'.*?addaction .*?name="(.*?)".*?')
	slider_pattern = re.compile(r'.*?widget class="QSlider".*?name="(.*?)".*?')

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

	except FileNotFoundError:
		print(f"Error: The file '{file_path}' was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")

	missing_buttons = list(set(QPushButtons) - set(found_buttons))
	missing_checkboxes = list(set(QCheckBoxes) - set(found_checkboxes))
	missing_actions = list(set(QActions) - set(found_actions))
	missing_sliders = list(set(QSliders) - set(found_sliders))

	return missing_buttons, missing_checkboxes, missing_actions, missing_sliders

# Example Usage:
# Assume your file is named 'ui_layout.txt' and contains lines like:
# <widget class="QPushButton" name="myButton1">
# <widget class="QCheckBox" name="myCheckBox">
# <widget class="QPushButton" name="anotherButton_ok">

# set the file path here
file_name = '/home/john/github/flexgui/examples/testgui/test.ui'
buttons, checkboxes, actions, sliders = extract_button_names(file_name)

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

