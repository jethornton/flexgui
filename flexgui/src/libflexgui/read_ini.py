from PyQt6.QtCore import QSettings


def read(parent):
	machine_name = parent.inifile.find("EMC", "MACHINE") or False
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
	parent.extensions = ['.ngc']
	ini_extensions = parent.inifile.find('DISPLAY', 'EXTENSIONS') or False
	if ini_extensions: # add any extensions from the ini to ngc
		for ext in ini_extensions.split(','):
			parent.extensions.append(ext.strip())

