import os, shutil, re, sys
from string import digits
from fractions import Fraction
from functools import partial

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor, QPalette
from PyQt6.QtGui import QAction, QTextFormat
from PyQt6.QtWidgets import QApplication, QTextEdit, QFileDialog, QMenu
from PyQt6.QtWidgets import QRadioButton, QGroupBox

import linuxcnc as emc

from libflexgui import dialogs
from libflexgui import commands

def to_bool(parent, ini_item, string):
	string = string.strip().lower() # Handle leading/trailing spaces and case variations
	if string == 'true':
		return True
	elif string == 'false':
		return False
	else:
		msg = (f'The INI key {ini_item} value "{string}"\n'
		'did not evaluate to a True or False Boolean')
		dialogs.error_msg_ok(parent, msg, 'title')
		return False

def to_int(string):
	try:
		number = int(string)
		return number
	except ValueError:
		return False

def is_float(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def is_number(string):
	try:
		int(string)
		return True
	except ValueError:
		try:
			float(string)
			return True
		except ValueError:
			return False

def is_fraction(item):
	try:
		Fraction(s)
		return True
	except ValueError:
		return False

def convert_fraction(item):
	# strip trailing non digits
	for i in range(len(item) - 1, -1, -1):
		if item[i].isdigit():
			fraction_string = item[:i+1]
			break
	suffix = item[i+1:].strip() if len(item[i+1:].strip()) > 0 else False

	if len(fraction_string.split('/')) == 2: # might be a good number
		match = re.match(r'(\d+)?\s*(\d+)/(\d+)', fraction_string)
		if match:
			whole_number = int(match.group(1)) if match.group(1) else 0
			numerator = int(match.group(2))
			denominator = int(match.group(3))
			# return the decimal number plus suffix
			return whole_number + (numerator / denominator), suffix
	else:
		return False, False

'''
In Python, a function can return multiple values by separating them with commas
in the return statement. When you return multiple values this way, Python
implicitly packages them into a single tuple.

Unpack the tuple into multiple variables: This is the most common and Pythonic
way. List the variable names on the left side of the assignment operator,
separated by commas, corresponding to the order of the returned values.
'''

def is_valid_increment(parent, item): # need to return text ,data and suffix
	if is_number(item): # there is no suffix and it's a valid number
		return f'{item} {parent.units.lower()}', item, parent.units

	if '/' in item: # it might be a fraction
		#for character in item:
		fraction, suffix = convert_fraction(item)
		if fraction and suffix:
			return f'{item}', fraction, 'inch'
		elif fraction and not suffix:
			return f'{item} inch', fraction, 'inch'
		else:
			return False, False, False

	units = ['mm', 'cm', 'um', 'in', 'inch', 'mil']
	if item.endswith(tuple(units)): # test to see if it matches any units
		for suffix in units:
			if item.endswith(suffix):
				increment = item.removesuffix(suffix).strip()
				if is_number(increment):
					return item, increment, suffix
				else:
					return False, False, False
	else: # not a valid increment
		return False, False, False

def string_to_int(string):
	if '.' in string:
		string, digits = string.split('.')
	return int(string)

def string_to_float(string):
	try:
		number = float(string)
		return number
	except ValueError:
		return False

def valid_color_string(string, key):
	for item in string.split(','):
		if not item.strip().isdigit():
			msg = (f'The [FLEXGUI] key {key}\n'
				f'{string}\n'
				'is not a valid color\n'
				'See the INI section of the\n'
				'documents for proper usage.')
			dialogs.warn_msg_ok(parent, msg, 'Invalid INI Entry')
			return False
		else:
			return True

def string_to_rgba(parent, string, key):
	if string.startswith('#') and len(string) == 7: # hex color
		return string
	if valid_color_string(string, key):
		if string.count(',') == 2: # rgb
			return f'rgb({string})'
		elif string.count(',') == 3: # rgba
			return f'rgba({string})'

def string_to_qcolor(parent, string, key):
	if valid_color_string(string, key):
		colors = [int(s) for s in string.split(',')]
		if len(colors) == 3:
			r, g, b = colors
			a = 255
		elif len(colors) == 4:
			r, g, b, a = colors
		else:
			return False
		return QColor(r,g,b,a)
	elif string.startswith('#'):
		color = string.lstrip('#')
		if len(color) != 6:
			return False
		try:
			r = int(color[0:2], 16)
			g = int(color[2:4], 16)
			b = int(color[4:6], 16)
			return QColor(r, g, b)
		except ValueError:
			return False

	else: # unknown color value
		msg = (f'The [FLEXGUI] key {key}\n'
			f'{string}\n'
			'is not a valid color\n'
			'See the INI section of the\n'
			'documents for proper usage.')
		dialogs.warn_msg_ok(parent, msg, 'Invalid INI Entry')
		return False

def file_chooser(parent, caption, dialog_type, nc_code_dir=None):
	if nc_code_dir is None:
		nc_code_dir = parent.nc_code_dir
	options = QFileDialog.Option.DontUseNativeDialog
	file_path = False
	file_dialog = QFileDialog()
	file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
	file_dialog.setOptions(QFileDialog.Option.DontUseNativeDialog)
	file_dialog.setWindowTitle('Open File')
	file_dialog.setStyleSheet('') # this does  nothing
	file_dialog.setGeometry(10, 10, 800, 600) # this does  nothing
	if dialog_type == 'open':
		file_path, file_type = file_dialog.getOpenFileName(None,
		caption=caption, directory=parent.nc_code_dir,
		filter=parent.ext_filter, options=options)
	elif dialog_type == 'save':
		file_path, file_type = file_dialog.getSaveFileName(None,
		caption=caption, directory=parent.nc_code_dir,
		filter=parent.ext_filter, options=options)
	if file_path:
		return file_path
	else:
		return False

def all_homed(parent):
	parent.status.poll()
	return parent.status.homed.count(1) == parent.status.joints

def all_unhomed(parent):
	parent.status.poll()
	num_joints = parent.status.joints
	home_status = parent.status.homed[:num_joints]
	test_list = []
	for i in range(num_joints):
		test_list.append(0)
	test_tuple = tuple(test_list)
	return home_status == test_tuple

def home_all_check(parent):
	parent.status.poll()
	for i in range(parent.status.joints):
		if parent.inifile.find(f'JOINT_{i}', 'HOME_SEQUENCE') is None:
			return False
	return True

def set_hal_enables(parent, obj):
	obj_name = obj.objectName()
	always_on = obj.property('always_on')
	state_on = obj.property('state_on')
	all_homed = obj.property('all_homed')

	if always_on:
		return

	# FIXME parent.state_estop_disabled needs to be removed
	special_buttons = ['probing_enable_pb', 'tool_changed_pb']
	# all HAL objects are disabled when state estop unless always_on is true
	parent.state_estop_disabled.append(obj_name)
	if state_on and not all_homed:
		#parent.state_estop_reset[obj_name] = False
		parent.state_on_enabled.append(obj_name)
	elif not state_on and all_homed:
		parent.homed_enabled.append(obj_name)
	elif state_on and all_homed:
		#parent.state_estop_reset[obj_name] = False
		parent.homed_enabled.append(obj_name)
		#parent.state_on_unhomed[obj_name] = False
	elif obj_name not in special_buttons: # enable/disable with estop
			parent.state_estop_disabled.append(obj_name)
			parent.state_estop_reset_enabled.append(obj_name)

def hal_confirm(parent):
	sender = parent.sender()
	text = sender.text()
	checked_state = sender.isChecked()
	pin = sender.property('pin_name')
	msg = (f'The HAL object "{text}" requests\n'
	'confirmation before changing the HAL\n'
	f'state of the {pin} pin.')
	result = dialogs.confirm_msg_ok_cancel(parent, msg, 'HAL')
	if result:
		setattr(parent.halcomp, pin, checked_state)
	else: # reset the checked state
		sender.blockSignals(True)
		sender.setChecked(not checked_state)
		sender.blockSignals(False)

def jog_toggled(parent):
	if parent.sender().isChecked():
		parent.kb_jog_cb_enabled = True
	else:
		parent.kb_jog_cb_enabled = False

def update_jog_lb(parent):
	val = parent.jog_vel_sl.value()
	if val > 0:
		parent.jog_vel_lb.setText(f'{val} {parent.units}/min')
		parent.status.poll()
		if parent.status.task_state == emc.STATE_ON:
			for item in parent.jog_buttons:
				getattr(parent, item).setEnabled(True)
	elif val == 0:
		parent.jog_vel_lb.setText('N/A')
		for item in parent.jog_buttons:
			getattr(parent, item).setEnabled(False)

def copy_errors(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.errors_pte.toPlainText())
	if 'statusbar' in parent.child_names:
		parent.statusbar.showMessage('Errors copied to clipboard', 10000)

def clear_errors(parent):
	parent.errors_pte.clear()

def clear_info(parent):
	parent.info_pte.clear()

def ok_for_mdi(parent):
	parent.status.poll()
	return not parent.status.estop and parent.status.enabled and (parent.status.homed.count(1) == parent.status.joints) and (parent.status.interp_state == emc.INTERP_IDLE)

def add_mdi(parent): # when you click on the mdi history list widget
	if 'mdi_command_le' in parent.child_names:
		parent.mdi_command_le.setText(f'{parent.mdi_history_lw.currentItem().text()}')

def update_mdi(parent):
	if parent.status.state == emc.RCS_ERROR:
		if 'mdi_command_le' in parent.child_names:
			parent.mdi_command_le.setText('')
	elif 'mdi_history_lw' in parent.child_names:
		rows = parent.mdi_history_lw.count()
		if rows > 0:
			last_item = parent.mdi_history_lw.item(rows - 1).text().strip()
		else:
			last_item = ''
		if last_item != parent.mdi_command:
			parent.mdi_history_lw.addItem(parent.mdi_command)
			path = os.path.dirname(parent.status.ini_filename)
			mdi_file = os.path.join(path, 'mdi_history.txt')
			mdi_codes = []
			for index in range(parent.mdi_history_lw.count()):
				mdi_codes.append(parent.mdi_history_lw.item(index).text())
			with open(mdi_file, 'w') as f:
				f.write('\n'.join(mdi_codes))
		if 'mdi_command_le' in parent.child_names:
			parent.mdi_command_le.setText('')
	parent.command.mode(emc.MODE_MANUAL)
	parent.command.wait_complete()
	parent.mdi_command = ''

def feed_override(parent, value):
	parent.command.feedrate(float(value / 100))

def rapid_override(parent, value):
	parent.command.rapidrate(float(value / 100))

def spindle_override(parent, value):
	parent.command.spindleoverride(float(value / 100), 0)

def max_velocity(parent,value):
	# maxvel(float) set maximum velocity
	parent.command.maxvel(float(value / 60))
	if 'max_vel_lb' in parent.child_names:
		parent.max_vel_lb.setText(f'{value} {parent.units}/min')

def update_qcode_pte(parent):
	extraSelections = []
	if not parent.gcode_pte.isReadOnly():
		selection = QTextEdit.ExtraSelection()
		lineColor = QColor('yellow').lighter(160)
		selection.format.setBackground(lineColor)
		selection.format.setForeground(QColor('black'))
		selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
		selection.cursor = parent.gcode_pte.textCursor()
		selection.cursor.clearSelection()
		extraSelections.append(selection)
	parent.gcode_pte.setExtraSelections(extraSelections)
	if 'start_line_lb' in parent.child_names:
		cursor = parent.gcode_pte.textCursor()
		selected_block = cursor.blockNumber() # get current block number
		parent.start_line_lb.setText(f'{selected_block}')

def nc_code_changed(parent):
	if 'save_pb' in parent.child_names:
		if hasattr(parent.save_pb, 'led'):
			parent.save_pb.led = True

def read_dir(parent): # touch screen file navigator
	if os.path.isdir(parent.nc_code_dir):
		file_list = []
		# get directories
		for item in sorted(os.listdir(parent.nc_code_dir)):
			path = os.path.join(parent.nc_code_dir, item)
			if os.path.isdir(path):
				file_list.append(f'{item} ...')

		# get nc_code files
		for item in sorted(os.listdir(parent.nc_code_dir)):
			if os.path.splitext(item)[1].lower() in parent.extensions:
				file_list.append(item)
		parent.file_lw.clear()
		parent.file_lw.addItem(parent.nc_code_dir)
		parent.file_lw.addItem('Open Parent Directory')
		parent.file_lw.addItems(file_list)
		if parent.touch_file_width:
			parent.file_lw.setMinimumWidth(parent.file_lw.sizeHintForColumn(0)+60)

def sync_checkboxes(parent, sender, receiver):
	parent.settings.setValue(f'PLOT/{sender}',getattr(parent, sender).isChecked())
	if receiver in parent.child_names:
		getattr(parent, receiver).setChecked(getattr(parent, sender).isChecked())
		parent.settings.setValue(f'PLOT/{receiver}', getattr(parent, sender).isChecked())

def sync_toolbuttons(parent, view):
	view_toolbuttons = [
	'flex_View_P',
	'flex_View_X',
	'flex_View_Y',
	'flex_View_Y2',
	'flex_View_Z',
	'flex_View_Z2',
	]

	for t in view_toolbuttons:
		if t in parent.child_names:
			getattr(parent, t).setStyleSheet(parent.deselected_style)

	match view:
		case 'p' if 'flex_View_P' in parent.child_names:
			parent.flex_View_P.setStyleSheet(parent.selected_style)
		case 'x' if 'flex_View_X' in parent.child_names:
			parent.flex_View_X.setStyleSheet(parent.selected_style)
		case 'y' if 'flex_View_Y' in parent.child_names:
			parent.flex_View_Y.setStyleSheet(parent.selected_style)
		case 'y2' if 'flex_View_Y2' in parent.child_names:
			parent.flex_View_Y2.setStyleSheet(parent.selected_style)
		case 'z' if 'flex_View_Z' in parent.child_names:
			parent.flex_View_Z.setStyleSheet(parent.selected_style)
		case 'z2' if 'flex_View_Z2' in parent.child_names:
			parent.flex_View_Z2.setStyleSheet(parent.selected_style)

def var_value_changed(parent, value):
	variable = parent.sender().property('variable')
	parent.cmd = f'#{variable}={value}'
	QTimer.singleShot(500, lambda: sync_var_file(parent))

def sync_var_file(parent):
	parent.status.poll()
	if (parent.status.task_state == emc.STATE_ON
		and parent.status.task_mode == emc.MODE_MANUAL
		and parent.status.motion_mode == emc.TRAJ_MODE_TELEOP
		and parent.status.interp_state == emc.INTERP_IDLE):
		if parent.status.task_mode != emc.MODE_MDI:
			parent.command.mode(emc.MODE_MDI)
			parent.command.wait_complete()
		parent.command.mdi(parent.cmd)
		parent.command.wait_complete()
		parent.command.task_plan_synch()
		parent.command.mode(emc.MODE_MANUAL)
		parent.command.wait_complete()

def var_file_watch(parent):
	parent.status.poll()
	if (parent.status.task_state == emc.STATE_ON
		and parent.status.task_mode == emc.MODE_MANUAL
		and parent.status.motion_mode == emc.TRAJ_MODE_TELEOP
		and parent.status.interp_state == emc.INTERP_IDLE):
		var_current_time = os.stat(os.path.join(parent.config_path, parent.var_file)).st_mtime
		if parent.var_mod_time != var_current_time:
			var_file = os.path.join(parent.config_path, parent.var_file)
			with open(var_file, 'r') as f:
				var_list = f.readlines()
			for key, value in parent.watch_var.items():
				for line in var_list:
					if line.startswith(value[0]):
						getattr(parent, key).setText(f'{float(line.split()[1]):.{value[1]}f}')
			for key, value in parent.set_var.items():
				for line in var_list:
					if line.split()[0] == value:
						getattr(parent, key).setValue(float(line.split()[1]))
			parent.var_mod_time = var_current_time

def io_watch(parent):
	for key, value in parent.hal_io_check.items():
		checked_state = getattr(parent, key).isChecked()
		hal_state = getattr(parent.halcomp, value)
		if checked_state != hal_state:
			getattr(parent, key).setChecked(hal_state)

	for key, value in parent.hal_io_int.items():
		int_value = getattr(parent, key).value()
		hal_value = getattr(parent.halcomp, value)
		if int_value != hal_value:
			getattr(parent, key).setValue(hal_value)

	for key, value in parent.hal_io_float.items():
		float_value = getattr(parent, key).value()
		hal_value = getattr(parent.halcomp, value)
		if float_value != hal_value:
			getattr(parent, key).setValue(hal_value)

def update_home_controls(parent):
	parent.status.poll()
	if parent.status.task_state == emc.STATE_ON: # other states are handled in status.py

		# set home/unhome for each joint
		for joint in range(parent.joints):
			if parent.status.joint[joint]['homed']: # joint is homed
				if f'home_pb_{joint}' in parent.child_names:
					getattr(parent, f'home_pb_{joint}').setEnabled(False)
				if f'actionHome_{joint}' in parent.child_names:
					getattr(parent, f'actionHome_{joint}').setEnabled(False)

				if f'unhome_pb_{joint}' in parent.child_names:
					getattr(parent, f'unhome_pb_{joint}').setEnabled(True)
				if f'actionUnhome_{joint}' in parent.child_names:
					getattr(parent, f'actionUnhome_{joint}').setEnabled(True)

				if f'home_lb_{joint}' in parent.child_names:
					getattr(parent, f'home_lb_{joint}').setText('*')

			elif not parent.status.joint[joint]['homed']: # joint is not homed
				if f'home_pb_{joint}' in parent.child_names:
					getattr(parent, f'home_pb_{joint}').setEnabled(True)
				if f'actionHome_{joint}' in parent.child_names:
					getattr(parent, f'actionHome_{joint}').setEnabled(True)

				if f'unhome_pb_{joint}' in parent.child_names:
					getattr(parent, f'unhome_pb_{joint}').setEnabled(False)
				if f'actionUnhome_{joint}' in parent.child_names:
					getattr(parent, f'actionUnhome_{joint}').setEnabled(False)

				if f'home_lb_{joint}' in parent.child_names:
					getattr(parent, f'home_lb_{joint}').setText('')

		# all joints homed
		if all(v == 1 for v in parent.status.homed[:parent.joints]):
			if 'home_all_pb' in parent.child_names:
				parent.home_all_pb.setEnabled(False)
			if 'actionHoming' in parent.child_names:
				parent.actionHoming.setEnabled(False)
			if 'actionHome_All' in parent.child_names:
				parent.actionHome_All.setEnabled(False)

			if 'unhome_all_pb' in parent.child_names:
				parent.unhome_all_pb.setEnabled(True)
			if 'actionUnhoming' in parent.child_names:
				parent.actionUnhoming.setEnabled(True)
			if 'actionUnhome_All' in parent.child_names:
				parent.actionUnhome_All.setEnabled(True)

			for item in parent.homed_enabled:
				getattr(parent, item).setEnabled(True)

		# no joints are homed
		elif all(v == 0 for v in parent.status.homed[:parent.joints]):
			if 'home_all_pb' in parent.child_names:
				parent.home_all_pb.setEnabled(True)
			if 'actionHoming' in parent.child_names:
				parent.actionHoming.setEnabled(True)
			if 'actionHome_All' in parent.child_names:
				parent.actionHome_All.setEnabled(True)

			if 'unhome_all_pb' in parent.child_names:
				parent.unhome_all_pb.setEnabled(False)
			if 'actionUnhoming' in parent.child_names:
				parent.actionUnhoming.setEnabled(False)
			if 'actionUnhome_All' in parent.child_names:
				parent.actionUnhome_All.setEnabled(False)

			for item in parent.homed_enabled:
				getattr(parent, item).setEnabled(False)

		# some joints homed
		elif any(v == 1 for v in parent.status.homed[:parent.joints]):
			if 'home_all_pb' in parent.child_names and home_all_check(parent):
				parent.home_all_pb.setEnabled(True)
			if 'actionHome_All' in parent.child_names:
				parent.actionHome_All.setEnabled(True)

			if 'unhome_all_pb' in parent.child_names:
				parent.unhome_all_pb.setEnabled(True)
			if 'actionUnhoming' in parent.child_names:
				parent.actionUnhoming.setEnabled(True)
			if 'actionUnhome_All' in parent.child_names:
				parent.actionUnhome_All.setEnabled(True)

			for item in parent.homed_enabled:
				getattr(parent, item).setEnabled(False)

def update_run_controls(parent):
	parent.status.poll()
	all_homed = all(v == 1 for v in parent.status.homed[:parent.joints]) # all joints homed
	file_loaded = len(parent.status.file) > 0 # currently loaded g code file
	interp_state = parent.status.interp_state
	motion_type = parent.status.motion_type
	task_mode = parent.status.task_mode
	task_state = parent.status.task_state
	state = parent.status.state

	if not file_loaded:
		for item in parent.file_save_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.file_edit_controls:
			getattr(parent, item).setEnabled(False)

	if task_state == emc.STATE_ESTOP:
		#print('update run controls STATE_ESTOP')
		for item in parent.power_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.run_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.step_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.pause_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.resume_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.coolant_controls:
			getattr(parent, item).setEnabled(False)

	if task_state == emc.STATE_ESTOP_RESET:
		#print('update run controls STATE_ESTOP_RESET')
		for item in parent.power_controls:
			getattr(parent, item).setEnabled(True)
		for item in parent.run_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.step_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.pause_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.resume_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.coolant_controls:
			getattr(parent, item).setEnabled(False)

	if task_state == emc.STATE_ON:
		#print('update run controls STATE_ON')
		for item in parent.coolant_controls:
			getattr(parent, item).setEnabled(True)
		if task_mode == emc.MODE_AUTO: # program running
			#print('update run controls MODE_AUTO')
			if state == emc.RCS_EXEC: # INTERPRETER RUNNING
				for item in parent.run_controls:
					getattr(parent, item).setEnabled(False)
				for item in parent.step_controls:
					getattr(parent, item).setEnabled(False)
				# FIXME program_running_disabled needs to be handled with x_controls
				for item in parent.program_running_disabled:
					getattr(parent, item).setEnabled(False)
				for item in parent.spindle_controls:
					getattr(parent, item).setEnabled(False)
				for item in parent.file_edit_controls:
					getattr(parent, item).setEnabled(False)
				for item in parent.file_save_controls:
					getattr(parent, item).setEnabled(False)

			if state == emc.RCS_EXEC and interp_state == emc.INTERP_PAUSED:
				#print('paused')
				for item in parent.pause_controls:
					getattr(parent, item).setEnabled(False)
				if parent.step:
					for item in parent.step_controls:
						getattr(parent, item).setEnabled(True)
				else:
					for item in parent.resume_controls:
						getattr(parent, item).setEnabled(True)
			if state == emc.RCS_EXEC and motion_type == 0: # MOTION_TYPE_NONE
				#print('motion none')
				for item in parent.pause_controls:
					getattr(parent, item).setEnabled(False)
				if parent.step:
					for item in parent.step_controls:
						getattr(parent, item).setEnabled(True)
				else:
					for item in parent.resume_controls:
						getattr(parent, item).setEnabled(True)

			if state == emc.RCS_EXEC and motion_type != 0: # NOT MOTION_TYPE_NONE
				if interp_state != emc.INTERP_PAUSED:
					#print('in motion')
					if parent.step:
						for item in parent.step_controls:
							getattr(parent, item).setEnabled(False)
					else:
						for item in parent.pause_controls:
							getattr(parent, item).setEnabled(True)
					for item in parent.resume_controls:
						getattr(parent, item).setEnabled(False)

		elif task_mode == emc.MODE_MANUAL:
			#print('update run controls MODE_MANUAL')
			if all_homed and file_loaded or parent.stop:
				for item in parent.run_controls:
					getattr(parent, item).setEnabled(True)
				for item in parent.step_controls:
					getattr(parent, item).setEnabled(True)
				for item in parent.spindle_controls:
					getattr(parent, item).setEnabled(True)
				for item in parent.pause_controls:
					getattr(parent, item).setEnabled(False)
				for item in parent.resume_controls:
					getattr(parent, item).setEnabled(False)
				parent.stop = False
				parent.step = False

			if file_loaded:
				for item in parent.file_edit_controls:
					getattr(parent, item).setEnabled(True)
				for item in parent.file_save_controls:
					getattr(parent, item).setEnabled(True)

			for item in parent.program_running_disabled:
				getattr(parent, item).setEnabled(True)
			for item in parent.mdi_controls:
				getattr(parent, item).setEnabled(True)
			for item in parent.file_load_controls:
				getattr(parent, item).setEnabled(True)


		elif task_mode == emc.MODE_MDI: # mdi running
			#print('update run controls MODE_MDI')
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(False)
			for item in parent.step_controls:
				getattr(parent, item).setEnabled(False)
			for item in parent.pause_controls:
				getattr(parent, item).setEnabled(False)
			for item in parent.resume_controls:
				getattr(parent, item).setEnabled(False)
			for item in parent.program_running_disabled:
				getattr(parent, item).setEnabled(False)

def update_hal_io(parent, value):
	setattr(parent.halcomp, parent.sender().property('pin_name'), value)

def update_hal_spinbox(parent, value):
	setattr(parent.halcomp, parent.sender().property('pin_name'), value)

def update_hal_slider(parent, value):
	setattr(parent.halcomp, parent.sender().property('pin_name'), value)

def change_page(parent):
	object_name = parent.sender().property('change_page')
	index = int(parent.sender().property('index'))
	getattr(parent, object_name).setCurrentIndex(index)

def next_page(parent):
	btn = parent.sender()
	object_name = btn.property('next_page')
	pages = getattr(parent, object_name).count() -1
	index = getattr(parent, object_name).currentIndex()
	if index < pages:
		getattr(parent, object_name).setCurrentIndex(index + 1)
	elif index == pages:
		getattr(parent, object_name).setCurrentIndex(0)

def previous_page(parent):
	btn = parent.sender()
	object_name = btn.property('previous_page')
	pages = getattr(parent, object_name).count() -1
	index = getattr(parent, object_name).currentIndex()
	if index > 0:
		getattr(parent, object_name).setCurrentIndex(index - 1)
	elif index == 0:
		getattr(parent, object_name).setCurrentIndex(pages)

def flash_buttons(parent):
	# Store a boolean that toggles on each execution
	flash_buttons.value = not getattr(flash_buttons, 'value', False)
	for name in parent.flashing_buttons:
		flashing_state = getattr(parent, name).property('flash_state')
		checked_state =  getattr(parent, name).isChecked()
		if (flashing_state == "unchecked" and not checked_state or
			flashing_state == "checked" and checked_state):
			# This button is flashing.  Update the flashing propery
			# and trigger a refresh of the style sheet.
			getattr(parent, name).setProperty('flashing', str(flash_buttons.value))
			getattr(parent, name).setStyleSheet( getattr(parent, name).styleSheet())
		elif getattr(parent, name).property('flashing') is not None:
			# This button not flashing.  Clear the flashing propery
			# and trigger a refresh of the style sheet.
			getattr(parent, name).setProperty('flashing', None)
			getattr(parent, name).setStyleSheet( getattr(parent, name).styleSheet())

def update_grid_size(parent, grid_size):
	if 'plot_widget' in parent.child_names:
		parent.plotter.grid_size = grid_size
		parent.plotter.update()

		menu = parent.findChild(QAction, 'actionGrids') or parent.findChild(QMenu, 'actionGrids')
		# Handle both top-level QMenu and QAction submenus.
		if isinstance(menu, QAction):
			menu = menu.menu()
		if menu:
			for action in menu.actions():
				if action.data() == grid_size:
					action.setChecked(True)
				else:
					action.setChecked(False)
