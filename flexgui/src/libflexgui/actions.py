import os

from functools import partial

from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication([])

def load_file(parent, gcode_file):
	parent.command.program_open(gcode_file)
	text = open(gcode_file).read()
	if parent.gcode_pte_exists:
		parent.gcode_pte.setPlainText(text)
	#parent.actionReload.setEnabled(True)
	base = os.path.basename(gcode_file)

	keys = parent.settings.allKeys()
	files = []
	for key in keys:
		if key.startswith('recent_files'):
			files.append(parent.settings.value(key))
			#print(parent.settings.value(key))
	if gcode_file in files:
		files.remove(gcode_file)

	files.insert(0, gcode_file)
	#print(files)

	files = files[:5]
	#print(files)

	parent.settings.beginGroup('recent_files')
	parent.settings.remove('')
	for i, item in enumerate(files):
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

def action_test(parent, text):
	print(text)
	print(parent.sender().objectName())

def action_recent(parent, text): # actionRecent
	print(parent.sender().objectName())

def action_edit(parent): # actionEdit
	print(parent.sender().objectName())

def action_reload(parent): # actionReload
	print(parent.sender().objectName())

def action_save_as(parent): # actionSave_As
	print(parent.sender().objectName())

def action_edit_tool_table(parent): # actionEdit_Tool_Table
	print(parent.sender().objectName())

def action_reload_tool_table(parent): # actionReload_Tool_Table
	print(parent.sender().objectName())

def action_ladder_editor(parent): # actionLadder_Editor
	print(parent.sender().objectName())

def action_quit(parent): # actionQuit
	print(parent.sender().objectName())

def action_clear_mdi(parent): # actionClear_MDI
	print(parent.sender().objectName())

def action_copy_mdi(parent): # actionCopy_MDI
	print(parent.sender().objectName())

def action_show_hal(parent): # actionShow_HAL
	print(parent.sender().objectName())
	# subprocess.Popen(r'c:\mytool\tool.exe', cwd=r'd:\test\local')
	# os.path.dirname(os.path.realpath(__file__)) 

def action_hal_meter(parent): # actionHal_Meter
	print(parent.sender().objectName())

def action_hal_scope(parent): # actionHal_Scope
	print(parent.sender().objectName())

def action_about(parent): # actionAbout
	print(parent.sender().objectName())

def action_quick_reference(parent): # actionQuick_Reference
	print(parent.sender().objectName())


