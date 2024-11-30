import os, sys, subprocess, shutil
from functools import partial

from PyQt6.QtWidgets import QApplication, QFileDialog, QLabel, QMenu

import linuxcnc as emc
import hal

from libflexgui import dialogs
from libflexgui import utilities
from libflexgui import select

def load_file(parent, gcode_file):
	if os.path.isfile(gcode_file):
		parent.command.program_open(gcode_file)
		parent.command.wait_complete()
		if 'plot_widget' in parent.children:
			parent.plotter.clear_live_plotter()

		text = open(gcode_file).read()
		if 'gcode_pte' in parent.children:
			parent.gcode_pte.setPlainText(text)
		base = os.path.basename(gcode_file)
		if 'file_lb' in parent.children:
			parent.file_lb.setText(base)

		# update controls
		for item in parent.file_edit_items:
			getattr(parent, item).setEnabled(True)
		if 'start_line_lb' in parent.children:
			parent.start_line_lb.setText('0')

		# get recent files from settings
		keys = parent.settings.allKeys()
		file_list = []
		for key in keys:
			if key.startswith('recent_files'):
				file_list.append(parent.settings.value(key))
		# if the g code file is in the list remove it
		if gcode_file in file_list:
			file_list.remove(gcode_file)
		# insert the g code file at the top of the list
		file_list.insert(0, gcode_file)
		# trim the list to 10
		file_list = file_list[:10]

		# add files back into settings
		parent.settings.beginGroup('recent_files')
		parent.settings.remove('')
		for i, item in enumerate(file_list):
			parent.settings.setValue(str(i), item)
		parent.settings.endGroup()

		# clear the recent menu
		if parent.findChild(QMenu, 'menuRecent'):
			parent.menuRecent.clear()
			# add the recent files from settings
			keys = parent.settings.allKeys()
			for key in keys:
				if key.startswith('recent_files'):
					path = parent.settings.value(key)
					name = os.path.basename(path)
					a = parent.menuRecent.addAction(name)
					a.triggered.connect(partial(load_file, parent, path))

		# enable run items
		parent.status.poll()
		if utilities.all_homed(parent) and parent.status.task_state == emc.STATE_ON:
			for item in parent.run_controls:
				getattr(parent, item).setEnabled(True)
	else:
		msg = (f'{gcode_file}\n'
		'was not found. Loading aborted!')
		dialogs.warn_msg_ok(msg, 'File Missing')

def file_selector(parent): # touch screen file selector
	item = parent.file_lw.currentItem().text()

	if item == 'Parent Directory': # move up one directory
		parent.nc_code_dir = os.path.abspath(os.path.join(parent.nc_code_dir, os.pardir))
		utilities.read_dir(parent)
	elif item.endswith('...'): # a subdirectory
		parent.nc_code_dir = os.path.join(parent.nc_code_dir, item.replace(' ...', ''))
		utilities.read_dir(parent)
	else: # must be a file name
		load_file(parent, os.path.join(parent.nc_code_dir, item))

def action_open(parent): # actionOpen
	nc_code_file = utilities.file_chooser(parent, 'Open File', 'open')
	if nc_code_file: load_file(parent, nc_code_file)

def action_edit(parent): # actionEdit
	parent.status.poll
	gcode_file = parent.status.file or False
	if not gcode_file:
		msg = ('No File is open.\nDo you want to open a file?')
		response = dialogs.warn_msg_yes_no(msg, 'No File Loaded')
		if response:
			action_open(parent)
			return
		else:
			return

	if parent.editor:
		if shutil.which(parent.editor.lower()) is not None:
			subprocess.Popen([parent.editor, gcode_file])
		else:
			select_editor(parent, gcode_file)
	else:
		msg = ('No Editor was found\nin the ini Display section\n'
			'Do you want to select an Editor?')
		if dialogs.warn_msg_yes_no(msg, 'No Editor Configured'):
			select_editor(parent, gcode_file)

def select_editor(parent, gcode_file):
	select_dialog = select.editor_dialog()
	if select_dialog.exec():
		editor = select_dialog.choice.currentData()
		if editor:
			subprocess.Popen([editor, gcode_file])

def action_reload(parent): # actionReload
	parent.status.poll()
	gcode_file = parent.status.file or False
	if gcode_file:
		if parent.status.task_mode != emc.MODE_MANUAL:
			parent.command.mode(emc.MODE_MANUAL)
			parent.command.wait_complete()
		parent.command.program_open(gcode_file)
		if 'plot_widget' in parent.children:
			parent.plotter.clear_live_plotter()
			parent.plotter.update()
			parent.plotter.load(gcode_file)

		if 'gcode_pte' in parent.children:
			with open(gcode_file) as f:
				parent.gcode_pte.setPlainText(f.read())

def action_save_as(parent): # actionSave_As
	current_gcode_file = parent.status.file or False
	if not current_gcode_file:
		msg = ('No File is Open')
		dialogs.warn_msg_ok(msg, 'Error')
		return
	if os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
		gcode_dir = os.path.expanduser('~/linuxcnc/nc_files')
	else:
		gcode_dir = os.path.expanduser('~/')
	new_gcode_file, file_type = QFileDialog.getSaveFileName(None,
	caption="Save As", directory=gcode_dir,
	filter='G code Files (*.ngc *.NGC);;All Files (*)', options=QFileDialog.Option.DontUseNativeDialog,)
	if new_gcode_file:
		with open(current_gcode_file, 'r') as cf:
			gcode = cf.read()
		with open(new_gcode_file, 'w') as f:
			f.write(gcode)
		load_file(parent, new_gcode_file)

def action_edit_tool_table(parent): # actionEdit_Tool_Table
	tool_table_file = os.path.join(parent.ini_path, parent.tool_table)
	if os.path.isfile(tool_table_file):
		file_size = os.path.getsize(tool_table_file)
		if file_size == 0:
			msg = ('Can not edit an empty tool file.\n'
			'The tool file must have at least one entry.\n'
			'the first line must be just a semicolon\n'
			'the minimum second line has a tool and pocket\n'
			';\n'
			'T1 P1')
			dialogs.critical_msg_ok(msg, 'Empty File')
			return

		cmd = []
		if parent.tool_editor:
			for item in parent.tool_editor.split():
				cmd.append(item)
		else:
			cmd.append('tooledit')
			for axis in parent.axis_letters:
				cmd.append(axis)
			cmd.append('diam')
		cmd.append(parent.tool_table)
		subprocess.Popen(cmd, cwd=parent.ini_path)

def action_reload_tool_table(parent): # actionReload_Tool_Table
	parent.command.load_tool_table()
	parent.status.poll()
	tool_len = len(parent.status.tool_table)
	if 'tool_change_cb' in parent.children:
		parent.tool_change_cb.clear()
		parent.tool_change_cb.addItem('Tool 0', 0)
		for i in range(1, tool_len):
			tool_id = parent.status.tool_table[i][0]
			parent.tool_change_cb.addItem(f'Tool {tool_id}', tool_id)

def action_ladder_editor(parent): # actionLadder_Editor
	if hal.component_exists("classicladder_rt"):
		p = os.popen("classicladder  &", "w")
	else:
		msg = ('The Classic Ladder component\n is not loaded.')
		dialogs.warn_msg_ok(msg, 'Error')

def action_quit(parent): # actionQuit
	parent.close()

	parent.estop_open_color = parent.inifile.find('FLEX_COLORS', 'ESTOP_OPEN') or ''
	parent.estop_closed_color = parent.inifile.find('FLEX_COLORS', 'ESTOP_CLOSED') or '#ff6666'
	parent.power_off_color =  parent.inifile.find('FLEX_COLORS', 'POWER_OFF') or ''
	parent.power_on_color =  parent.inifile.find('FLEX_COLORS', 'POWER_ON') or '#00ff00'


def action_estop(parent): # actionEstop
	if parent.status.task_state == emc.STATE_ESTOP:
		parent.command.state(emc.STATE_ESTOP_RESET)
		if parent.estop_closed_color: # if False just don't bother
			if 'estop_pb' in parent.children:
				closed_color = f'QPushButton{{background-color: {parent.estop_closed_color};}}'
				parent.estop_pb.setStyleSheet(closed_color)
			if 'flex_E_Stop' in parent.children:
				closed_color = f'QToolButton{{background-color: {parent.estop_closed_color};}}'
				parent.flex_E_Stop.setStyleSheet(closed_color)
	else:
		parent.command.state(emc.STATE_ESTOP)
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

def action_power(parent): # actionPower
	if parent.status.task_state == emc.STATE_ESTOP_RESET:
		if 'override_limits_cb' in parent.children:
			if parent.override_limits_cb.isChecked():
				parent.command. override_limits()
		parent.command.state(emc.STATE_ON)
		if parent.power_on_color: # if False just don't bother
			if 'power_pb' in parent.children:
				on_color = f'QPushButton{{background-color: {parent.power_on_color};}}'
				parent.power_pb.setStyleSheet(on_color)
			if 'flex_Power' in parent.children:
				on_color = f'QToolButton{{background-color: {parent.power_on_color};}}'
				parent.flex_Power.setStyleSheet(on_color)
	else:
		parent.command.state(emc.STATE_OFF)
		if parent.power_off_color: # if False just don't bother
			if 'power_pb' in parent.children:
				off_color = f'QPushButton{{background-color: {parent.power_off_color};}}'
				parent.power_pb.setStyleSheet(off_color)
			if 'flex_Power' in parent.children:
				off_color = f'QToolButton{{background-color: {parent.power_off_color};}}'
				parent.flex_Power.setStyleSheet(off_color)

def action_run(parent, line = 0): # actionRun
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_AUTO:
			parent.command.mode(emc.MODE_AUTO)
			parent.command.wait_complete()
		if 'start_line_lb' in parent.children:
			parent.start_line_lb.setText('0')
		parent.command.auto(emc.AUTO_RUN, line)

def action_run_from_line(parent): # actionRun_from_Line
	if 'gcode_pte' in parent.children:
		cursor = parent.gcode_pte.textCursor()
		selected_block = cursor.blockNumber() # get current block number
		action_run(parent, selected_block)

def action_step(parent): # actionStep
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_AUTO:
			parent.command.mode(emc.MODE_AUTO)
			parent.command.wait_complete()
		parent.command.auto(emc.AUTO_STEP)

def action_pause(parent): # actionPause
	if parent.status.state == emc.RCS_EXEC: # program is running
		parent.command.auto(emc.AUTO_PAUSE)

def action_resume(parent): # actionResume
	if parent.status.paused:
		parent.command.auto(emc.AUTO_RESUME)

def action_stop(parent): # actionStop
	parent.command.abort()

def action_clear_mdi(parent): # actionClear_MDI
	parent.mdi_history_lw.clear()
	path = os.path.dirname(parent.status.ini_filename)
	mdi_file = os.path.join(path, 'mdi_history.txt')
	with open(mdi_file, 'w') as f:
		f.write('')

def action_copy_mdi(parent): # actionCopy_MDI
	items = [parent.mdi_history_lw.item(x) for x in range(parent.mdi_history_lw.count())]
	mdi_list = []
	for item in items:
		mdi_list.append(item.text())
	qclip = QApplication.clipboard()
	qclip.setText('\n'.join(mdi_list))

def action_save_mdi(parent): # actionSave_MDI
	file_path = utilities.file_chooser(parent, 'Caption', 'save')
	if file_path:
		mdi_history_file = os.path.join(parent.ini_path, 'mdi_history.txt')
		if os.path.isfile(mdi_history_file):
			shutil.copyfile(mdi_history_file, file_path)
		else:
			msg = ('No MDI history file was found!')
			dialogs.info_msg_ok(msg , 'No MDI History')

def action_toggle_dro(parent):
	if parent.sender().isChecked():
		parent.plotter.enable_dro = True
	else:
		parent.plotter.enable_dro = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_dro_cb':
		utilities.sync_checkboxes(parent, 'view_dro_cb', 'actionDRO')
	elif name == 'actionDRO':
		utilities.sync_checkboxes(parent, 'actionDRO', 'view_dro_cb')

def action_toggle_limits(parent):
	if parent.sender().isChecked():
		parent.plotter.show_limits = True
	else:
		parent.plotter.show_limits = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_limits_cb':
		utilities.sync_checkboxes(parent, 'view_limits_cb', 'actionLimits')
	elif name == 'actionLimits':
		utilities.sync_checkboxes(parent, 'actionLimits', 'view_limits_cb')

def action_toggle_extents_option(parent):
	if parent.sender().isChecked():
		parent.plotter.show_extents_option = True
	else:
		parent.plotter.show_extents_option = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_extents_option_cb':
		utilities.sync_checkboxes(parent, 'view_extents_option_cb', 'actionExtents_Option')
	elif name == 'actionExtents_Option':
		utilities.sync_checkboxes(parent, 'actionExtents_Option', 'view_extents_option_cb')

def action_toggle_live_plot(parent):
	if parent.sender().isChecked():
		parent.plotter.show_live_plot = True
	else:
		parent.plotter.show_live_plot = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_live_plot_cb':
		utilities.sync_checkboxes(parent, 'view_live_plot_cb', 'actionLive_Plot')
	elif name == 'actionLive_Plot':
		utilities.sync_checkboxes(parent, 'actionLive_Plot', 'view_live_plot_cb')

def action_toggle_velocity(parent):
	if parent.sender().isChecked():
		parent.plotter.show_velocity = True
	else:
		parent.plotter.show_velocity = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_velocity_cb':
		utilities.sync_checkboxes(parent, 'view_velocity_cb', 'actionVelocity')
	elif name == 'actionVelocity':
		utilities.sync_checkboxes(parent, 'actionVelocity', 'view_velocity_cb')

def action_toggle_metric_units(parent):
	if parent.sender().isChecked():
		parent.plotter.metric_units = True
	else:
		parent.plotter.metric_units = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_metric_units_cb':
		utilities.sync_checkboxes(parent, 'view_metric_units_cb', 'actionMetric_Units')
	elif name == 'actionMetric_Units':
		utilities.sync_checkboxes(parent, 'actionMetric_Units', 'view_metric_units_cb')

def action_toggle_program(parent):
	if parent.sender().isChecked():
		parent.plotter.show_program = True
	else:
		parent.plotter.show_program = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_program_cb':
		utilities.sync_checkboxes(parent, 'view_program_cb', 'actionProgram')
	elif name == 'actionProgram':
		utilities.sync_checkboxes(parent, 'actionProgram', 'view_program_cb')

def action_toggle_rapids(parent):
	if parent.sender().isChecked():
		parent.plotter.show_rapids = True
	else:
		parent.plotter.show_rapids = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_rapids_cb':
		utilities.sync_checkboxes(parent, 'view_rapids_cb', 'actionRapids')
	elif name == 'actionRapids':
		utilities.sync_checkboxes(parent, 'actionRapids', 'view_rapids_cb')

def action_toggle_tool(parent):
	if parent.sender().isChecked():
		parent.plotter.show_tool = True
	else:
		parent.plotter.show_tool = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_tool_cb':
		utilities.sync_checkboxes(parent, 'view_tool_cb', 'actionTool')
	elif name == 'actionTool':
		utilities.sync_checkboxes(parent, 'actionTool', 'view_tool_cb')

def action_toggle_lathe_radius(parent):
	if parent.sender().isChecked():
		parent.plotter.show_lathe_radius = True
	else:
		parent.plotter.show_lathe_radius = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_lathe_radius_cb':
		utilities.sync_checkboxes(parent, 'view_lathe_radius_cb', 'actionLathe_Radius')
	elif name == 'actionLathe_Radius':
		utilities.sync_checkboxes(parent, 'actionLathe_Radius', 'view_lathe_radius_cb')

def action_toggle_dtg(parent):
	if parent.sender().isChecked():
		parent.plotter.show_dtg = True
	else:
		parent.plotter.show_dtg = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_dtg_cb':
		utilities.sync_checkboxes(parent, 'view_dtg_cb', 'actionDTG')
	elif name == 'actionDTG':
		utilities.sync_checkboxes(parent, 'actionDTG', 'view_dtg_cb')

def action_toggle_offsets(parent):
	if parent.sender().isChecked():
		parent.plotter.show_offsets = True
	else:
		parent.plotter.show_offsets = False
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_offsets_cb':
		utilities.sync_checkboxes(parent, 'view_offsets_cb', 'actionOffsets')
	elif name == 'actionOffsets':
		utilities.sync_checkboxes(parent, 'actionOffsets', 'view_offsets_cb')

def action_toggle_overlay(parent):
	if parent.sender().isChecked():
		parent.plotter.show_overlay = False
	else:
		parent.plotter.show_overlay = True
	parent.plotter.update()

	name = parent.sender().objectName()
	if name == 'view_overlay_cb':
		utilities.sync_checkboxes(parent, 'view_overlay_cb', 'actionOverlay')
	elif name == 'actionOverlay':
		utilities.sync_checkboxes(parent, 'actionOverlay', 'view_overlay_cb')

def action_clear_live_plot(parent):
	parent.plotter.clear_live_plotter()

def action_show_hal(parent): # actionShow_HAL
	subprocess.Popen('halshow', cwd=parent.ini_path)

def action_hal_meter(parent): # actionHal_Meter
	subprocess.Popen('halmeter', cwd=parent.ini_path)

def action_hal_scope(parent): # actionHal_Scope
	subprocess.Popen('halscope', cwd=parent.ini_path)

def action_about(parent): # actionAbout
	dialogs.about_dialog(parent)

def action_quick_reference(parent): # actionQuick_Reference
	dialogs.quick_reference_dialog(parent)


