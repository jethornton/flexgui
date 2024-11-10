import os

from PyQt6.QtCore import QSettings

def read(parent):
	machine_name = parent.inifile.find('EMC', 'MACHINE') or False
	if machine_name:
		parent.settings = QSettings('Flex', machine_name)
	else:
		parent.settings = QSettings('Flex', 'unknown')

	units = parent.inifile.find('TRAJ', 'LINEAR_UNITS') or False # mm or inch
	if units.lower() == 'inch':
		parent.default_precision = 4
	elif units.lower() == 'mm':
		parent.default_precision = 3
	else:
		parent.default_precision = 4

	# get file extensions
	parent.extensions = ['.ngc'] # used by the touch file selector
	extensions = parent.inifile.find('DISPLAY', 'EXTENSIONS') or False
	if extensions: # add any extensions from the ini to ngc
		for ext in ini_extensions.split(','):
			parent.extensions.append(ext.strip())
		extensions = extensions.split(',')
		extensions = ' '.join(extensions).strip()
		parent.ext_filter = f'G code Files ({extensions});;All Files (*)'
	else:
		parent.ext_filter = 'G code Files (*.ngc *.NGC);;All Files (*)'

	parent.estop_open_color = parent.inifile.find('FLEX_COLORS', 'ESTOP_OPEN') or False
	parent.estop_closed_color = parent.inifile.find('FLEX_COLORS', 'ESTOP_CLOSED') or False
	parent.power_off_color =  parent.inifile.find('FLEX_COLORS', 'POWER_OFF') or False
	parent.power_on_color =  parent.inifile.find('FLEX_COLORS', 'POWER_ON') or False

	units = parent.inifile.find('TRAJ', 'LINEAR_UNITS') or False
	if units == 'inch':
		parent.units = 'in'
	else:
		parent.units = 'mm'

	directory = parent.inifile.find('DISPLAY', 'PROGRAM_PREFIX') or False
	if directory:
		if directory.startswith('./'): # in this directory
			parent.nc_code_dir = os.path.join(parent.ini_path, directory[2:])
		elif directory.startswith('../'): # up one directory
			parent.nc_code_dir = os.path.dirname(parent.ini_path)
		elif directory.startswith('~'): # users home directory
			parent.nc_code_dir = os.path.expanduser(directory)
		elif os.path.isdir(directory):
			parent.nc_code_dir = directory
		else:
			parent.nc_code_dir = os.path.expanduser('~/')
	elif os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
		parent.nc_code_dir = os.path.expanduser('~/linuxcnc/nc_files')
	else:
		parent.nc_code_dir = os.path.expanduser('~/')


	parent.tool_editor = parent.inifile.find('DISPLAY', 'TOOL_EDITOR') or False
	parent.tool_table = parent.inifile.find('EMCIO', 'TOOL_TABLE') or False
	parent.var_file = parent.inifile.find('RS274NGC', 'PARAMETER_FILE') or False

	parent.plot_background_color = parent.inifile.find('FLEX', 'PLOT_BACKGROUND_COLOR') or False
	#print(type(background_color))
	#print(background_color)
	if parent.plot_background_color:
		parent.plot_background_color = tuple(map(float, parent.plot_background_color.split(',')))
	print(parent.plot_background_color)


