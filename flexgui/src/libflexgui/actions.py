import os, sys, subprocess

from functools import partial

from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel

import linuxcnc
import hal

from libflexgui import dialogs

app = QApplication([])

def load_file(parent, gcode_file):
	parent.command.program_open(gcode_file)
	parent.command.wait_complete()
	for item in parent.file_enable:
		getattr(parent, item).setEnabled(True)

	text = open(gcode_file).read()
	if parent.gcode_pte_exists:
		parent.gcode_pte.setPlainText(text)
	#parent.actionReload.setEnabled(True)
	base = os.path.basename(gcode_file)
	if parent.findChild(QLabel, 'file_lb'):
		parent.file_lb.setText(base)

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

def action_open(parent): # actionOpen
	if os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
		gcode_dir = os.path.expanduser('~/linuxcnc/nc_files')
	else:
		gcode_dir = os.path.expanduser('~/')
	gcode_file, file_type = QFileDialog.getOpenFileName(None,
	caption="Select G code File", directory=gcode_dir,
	filter='G code Files (*.ngc *.NGC);;All Files (*)', options=QFileDialog.DontUseNativeDialog,)
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
		cmd = ['which', editor]
		output = subprocess.run(cmd, capture_output=True, text=True)
		if output.returncode == 0:
			subprocess.Popen([editor, gcode_file])
		else: # FIXME get fancy and offer up and editor that's installed
			msg = ('The Editor configured in the ini file\n'
				'is not installed.')
			dialogs.warn_msg_ok(msg, 'Error')
	else:
		msg = ('No Editor was found\nin the ini Display section')
		dialogs.warn_msg_ok(msg, 'Editor')

def action_reload(parent): # actionReload
	parent.status.poll
	gcode_file = parent.status.file or False
	if gcode_file:
		parent.status.poll()
		if len(parent.status.file) > 0:
			if parent.status.task_mode != linuxcnc.MODE_MANUAL:
				parent.command.mode(linuxcnc.MODE_MANUAL)
				parent.command.wait_complete()
			gcode_file = parent.status.file 
			# Force a sync of the interpreter, which writes out the var file.
			parent.command.task_plan_synch()
			parent.command.wait_complete()
			parent.command.program_open(gcode_file)
		parent.command.program_open(gcode_file)
		text = open(gcode_file).read()
		if parent.gcode_pte_exists:
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
	filter='G code Files (*.ngc *.NGC);;All Files (*)', options=QFileDialog.DontUseNativeDialog,)
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
	subprocess.Popen([tool_editor, tool_file])

def action_reload_tool_table(parent): # actionReload_Tool_Table
	parent.command.load_tool_table()

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
	if parent.status.task_state == linuxcnc.STATE_ESTOP:
		parent.command.state(linuxcnc.STATE_ESTOP_RESET)
	else:
		parent.command.state(linuxcnc.STATE_ESTOP)

def action_power(parent): # actionPower
	if parent.status.task_state == linuxcnc.STATE_ESTOP_RESET:
		parent.command.state(linuxcnc.STATE_ON)
	else:
		parent.command.state(linuxcnc.STATE_OFF)

def action_run_program(parent): # actionRun_Program
	if parent.status.task_state == linuxcnc.STATE_ON:
		if parent.status.task_mode != linuxcnc.MODE_AUTO:
			parent.command.mode(linuxcnc.MODE_AUTO)
			parent.command.wait_complete()
		n = 0
		parent.command.auto(linuxcnc.AUTO_RUN, n)

def action_run_from_line(parent): # actionRun_from_Line
	print(parent.sender().objectName())

def action_step(parent): # actionStep
	if parent.status.task_state == linuxcnc.STATE_ON:
		if parent.status.task_mode != linuxcnc.MODE_AUTO:
			parent.command.mode(linuxcnc.MODE_AUTO)
			parent.command.wait_complete()
		parent.command.auto(linuxcnc.AUTO_STEP)

def action_pause(parent): # actionPause
	if parent.status.state == linuxcnc.RCS_EXEC: # program is running
		parent.command.auto(linuxcnc.AUTO_PAUSE)

def action_resume(parent): # actionResume
	if parent.status.paused:
		parent.command.auto(linuxcnc.AUTO_RESUME)

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


