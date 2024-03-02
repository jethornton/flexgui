import os

from PyQt5.QtWidgets import QApplication, QFileDialog, QPlainTextEdit
def action_open(parent): # actionOpen
	app = QApplication([])

	file_name, _ = QFileDialog.getOpenFileName(None, caption='Open file')
	return
	parent.file_dialog()
	

	'''

	if os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
		gcode_dir = os.path.expanduser('~/linuxcnc/nc_files')
	else:
		gcode_dir = os.path.expanduser('~/')
	file_name, _ = QFileDialog.getOpenFileName(parent, caption='Open file')
	print(file_name)

	fileName = QFileDialog.getOpenFileName(parent,
	caption="Select G code File", directory=gcode_dir,
	filter='G code Files (*.ngc *.NGC);;All Files (*)', options=QFileDialog.DontUseNativeDialog,)
	gcode_file = fileName[0]
	if gcode_file:
		parent.command.program_open(gcode_file)
		text = open(gcode_file).read()
		if parent.findChild(QPlainTextEdit, 'gcode_pte'):
			parent.gcode_pte.setPlainText(text)
		parent.actionReload.setEnabled(True)
		base = os.path.basename(gcode_file)
		if parent.file_lb_exists:
			parent.file_lb.setText(f'G code: {base}')
	'''
def action_recent(parent): # actionRecent
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


