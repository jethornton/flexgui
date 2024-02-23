import os, subprocess

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import Qt
app = Qt.QApplication([])

import linuxcnc as emc

from libflexgui import editor

def file_open(parent):
	if os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
		gcode_dir = os.path.expanduser('~/linuxcnc/nc_files')
	else:
		gcode_dir = os.path.expanduser('~/')
	fileName = QFileDialog.getOpenFileName(None,
	caption="Select G code File", directory=gcode_dir,
	filter='G code Files (*.ngc *.NGC);;All Files (*)', options=QFileDialog.DontUseNativeDialog,)
	gcode_file = fileName[0]
	if gcode_file:
		parent.command.program_open(gcode_file)
		text = open(gcode_file).read()
		parent.gcode_pte.setPlainText(text)
		parent.actionReload.setEnabled(True)
		base = os.path.basename(gcode_file)
		if parent.file_lb_exists:
			parent.file_lb.setText(f'G code: {base}')

def file_reload(parent):
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
		if parent.start_line_lb_exists:
			parent.start_line_lb.setText('')
		editor.clear_highlight(parent)
		text = open(gcode_file).read()
		parent.gcode_pte.setPlainText(text)

def app_close(parent):
	parent.close()

def clear_mdi(parent):
	parent.mdi_history_lw.clear()
	path = os.path.dirname(parent.status.ini_filename)
	mdi_file = os.path.join(path, 'mdi_history.txt')
	with open(mdi_file, 'w') as f:
		f.write('')

def show_hal(parent):
	subprocess.Popen('halshow')

def load_tool_table(parent):
	parent.command.load_tool_table()

