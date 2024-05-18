import os, sys, subprocess, shutil
from functools import partial

from PyQt6.QtWidgets import QFileDialog, QLabel

import linuxcnc as emc
import hal

from libflexgui import dialogs
from libflexgui import utilities
from libflexgui import select

def load_file(parent, gcode_file):
	parent.command.program_open(gcode_file)
	parent.command.wait_complete()
	if utilities.all_homed(parent):
		for item in parent.file_edit_items:
			getattr(parent, item).setEnabled(True)

	text = open(gcode_file).read()
	if 'gcode_pte' in parent.children:
		parent.gcode_pte.setPlainText(text)
	base = os.path.basename(gcode_file)
	if 'file_lb' in parent.children:
		parent.file_lb.setText(base)

	# update controls
	for item in parent.file_edit_items:
		getattr(parent, item).setEnabled(True)

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
	# trim the list to 5
	file_list = file_list[:5]

	# add files back into settings
	parent.settings.beginGroup('recent_files')
	parent.settings.remove('')
	for i, item in enumerate(file_list):
		parent.settings.setValue(str(i), item)
	parent.settings.endGroup()

	# clear the recent menu
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

def action_open(parent): # actionOpen
	extensions = parent.inifile.findall("FILTER", "PROGRAM_EXTENSION") or False
	if extensions:
		ext_groups = ['G code Files (*.ngc *.NGC)']
		for extension in extensions:
			filter_type = extension.split(' ', 1)
			if len(filter_type) > 1:
				ext_list = []
				desc = filter_type[1]
				exts = filter_type[0].split(',')
				for ext in exts:
					ext_list.append(f'*{ext}')
				ext_groups.append(f'{desc} ({" ".join(ext_list)})')
		ext_filter = ';;'.join(ext_groups)
	else:
		ext_filter = 'G code Files (*.ngc *.NGC);;All Files (*)'
	if os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
		gcode_dir = os.path.expanduser('~/linuxcnc/nc_files')
	else:
		gcode_dir = os.path.expanduser('~/')
	gcode_file, file_type = QFileDialog.getOpenFileName(None,
	caption="Select G code File", directory=gcode_dir,
	filter=ext_filter, options=QFileDialog.Option.DontUseNativeDialog)
	if gcode_file: load_file(parent, gcode_file)

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

	editor = parent.inifile.find('DISPLAY', 'EDITOR') or False
	if editor:
		if shutil.which(editor.lower()) is not None:
			subprocess.Popen([editor, gcode_file])
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
	parent.status.poll
	gcode_file = parent.status.file or False
	if gcode_file:
		parent.status.poll()
		if len(parent.status.file) > 0:
			if parent.status.task_mode != emc.MODE_MANUAL:
				parent.command.mode(emc.MODE_MANUAL)
				parent.command.wait_complete()
			gcode_file = parent.status.file 
			# Force a sync of the interpreter, which writes out the var file.
			parent.command.task_plan_synch()
			parent.command.wait_complete()
			parent.command.program_open(gcode_file)
		parent.command.program_open(gcode_file)
		text = open(gcode_file).read()
	if 'gcode_pte' in parent.children:
		parent.gcode_pte.setPlainText(text)

	else:
		msg = ('No File is open to reload')
		response = dialogs.warn_msg_ok(msg, 'Error')

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
	ini_path = parent.ini_path
	tool_editor = parent.inifile.find('DISPLAY', 'TOOL_EDITOR') or False
	if not tool_editor:
		tool_editor = 'tooledit'
	tool_table = parent.inifile.find('EMCIO', 'TOOL_TABLE') or False
	tool_file = os.path.join(ini_path, tool_table)
	cmd = tool_editor.split()
	cmd.append(tool_file)
	subprocess.Popen(cmd, cwd=parent.ini_path)

def action_reload_tool_table(parent): # actionReload_Tool_Table
	parent.command.load_tool_table()
	parent.status.poll()
	tool_len = len(parent.status.tool_table)
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
	#sys.exit()
	parent.close()

def action_estop(parent): # actionEstop
	if parent.status.task_state == emc.STATE_ESTOP:
		parent.command.state(emc.STATE_ESTOP_RESET)
	else:
		parent.command.state(emc.STATE_ESTOP)

def action_power(parent): # actionPower
	if parent.status.task_state == emc.STATE_ESTOP_RESET:
		parent.command.state(emc.STATE_ON)
	else:
		parent.command.state(emc.STATE_OFF)

def action_run(parent, line = 0): # actionRun
	if parent.status.task_state == emc.STATE_ON:
		if parent.status.task_mode != emc.MODE_AUTO:
			parent.command.mode(emc.MODE_AUTO)
			parent.command.wait_complete()
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

def action_show_hal(parent): # actionShow_HAL
	subprocess.Popen('halshow', cwd=parent.ini_path)

def action_hal_meter(parent): # actionHal_Meter
	subprocess.Popen('halmeter', cwd=parent.ini_path)

def action_hal_scope(parent): # actionHal_Scope
	subprocess.Popen('halscope', cwd=parent.ini_path)

def action_about(parent): # actionAbout
	print(parent.sender().objectName())

def action_quick_reference(parent): # actionQuick_Reference
	print(parent.sender().objectName())


