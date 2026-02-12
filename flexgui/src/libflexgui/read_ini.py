import os, sys

from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QColor

from libflexgui import dialogs
from libflexgui import utilities

def read(parent):
	# check for theme must be done before using any dialogs
	parent.theme = parent.inifile.find('FLEXGUI', 'THEME') or False

	# make a list of lists with every old section/item and warn if found
	old_ini_items = [
	['FLEX_COLORS', 'ESTOP_OPEN'],
	['FLEX_COLORS', 'ESTOP_CLOSED'],
	['FLEX_COLORS', 'POWER_OFF'],
	['FLEX_COLORS', 'POWER_ON'],
	['FLEXGUI', 'ESTOP_OPEN_COLOR'],
	['FLEXGUI', 'ESTOP_CLOSED_COLOR'],
	['FLEXGUI', 'POWER_OFF_COLOR'],
	['FLEXGUI', 'POWER_ON_COLOR'],
	['FLEXGUI', 'TOUCH_QSS'],
	['DISPLAY', 'RESOURCES'],
	['DISPLAY', 'SIZE'],
	['DISPLAY', 'VIEW'],
	['DISPLAY', 'THEME'],
	['DISPLAY', 'QSS'],
	['DISPLAY', 'DRO_FONT_SIZE'],
	['FLEX', 'PLOT_BACKGROUND_COLOR'],
	['FLEX', 'TOUCH_FILE_WIDTH'],
	['FLEX', 'MANUAL_TOOL_CHANGE'],
	['FLEX', 'IMPORT'],
	]
	for item in old_ini_items:
		if parent.inifile.find(item[0], item[1]):
			msg = (f'The key {item[1]} has been moved from the\n'
			f'[{item[0]}] section or is no longer used\n'
			'by FlexGUI or the name has been changed.\n'
			'Check the INI section of the Documents\n'
			'for correct INI entries.')
			dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	# ***** [EMC] Section *****
	machine_name = parent.inifile.find('EMC', 'MACHINE') or False
	if machine_name:
		parent.settings = QSettings('Flex', machine_name)
	else:
		parent.settings = QSettings('Flex', 'unknown')

	# ***** [DISPLAY] Section *****
	# get file extensions
	parent.extensions = ['.ngc'] # used by the touch file selector
	extensions = parent.inifile.find('DISPLAY', 'EXTENSIONS') or False
	if extensions: # add any extensions from the ini to ngc
		for ext in extensions.split(','):
			parent.extensions.append(ext.strip())
		extensions = extensions.split(',')
		extensions = ' '.join(extensions).strip()
		parent.ext_filter = f'G code Files ({extensions});;All Files (*)'
	else:
		parent.ext_filter = 'G code Files (*.ngc *.NGC);;All Files (*)'

	# set the nc code directory to some valid directory
	directory = parent.inifile.find('DISPLAY', 'PROGRAM_PREFIX') or False
	ini_dir = False
	if directory: # expand directory if needed
		ini_dir = True
		if directory.startswith('./'): # in this directory
			directory = os.path.join(parent.config_path, directory[2:])
		elif directory.startswith('../'): # up one directory
			directory = os.path.join(os.path.dirname(parent.config_path), directory[3:])
		elif directory.startswith('~'): # users home directory
			directory = os.path.expanduser(directory)

	if os.path.isdir(directory):
		parent.nc_code_dir = directory
	else: # try and find a directory
		if os.path.isdir(os.path.expanduser('~/linuxcnc/nc_files')):
			parent.nc_code_dir = os.path.expanduser('~/linuxcnc/nc_files')
		else:
			parent.nc_code_dir = os.path.expanduser('~/')
		if ini_dir: # a nc code directory was in the ini file but is not valid
			msg = (f'The path {directory}\n'
				'does not exist. Check the\n'
				'PROGRAM_PREFIX key in the\n'
				'[DISPLAY] section of the\n'
				'INI file for a valid path.\n'
				f'{parent.nc_code_dir} will be used.')
			dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	parent.editor = parent.inifile.find('DISPLAY', 'EDITOR') or False
	parent.tool_editor = parent.inifile.find('DISPLAY', 'TOOL_EDITOR') or False
	if parent.inifile.find('DISPLAY', 'LATHE') is not None:
		parent.default_view = 'y'
	elif parent.inifile.find('FLEXGUI', 'PLOT_VIEW') is not None:
		parent.default_view = parent.inifile.find('FLEXGUI', 'PLOT_VIEW')
	else:
		parent.default_view = 'p'

	parent.jog_increments = parent.inifile.find('DISPLAY', 'INCREMENTS') or False

	# check for default file to open
	parent.open_file = parent.inifile.find('DISPLAY', 'OPEN_FILE') or False

	# minimum jog velocity
	parent.min_jog_vel = parent.inifile.find("DISPLAY","MIN_LINEAR_VELOCITY") or False

	# default jog velocity
	parent.default_jog_vel = parent.inifile.find("DISPLAY","DEFAULT_LINEAR_VELOCITY") or False

	# maximum jog velocity
	parent.max_jog_vel = parent.inifile.find("DISPLAY","MAX_LINEAR_VELOCITY") or False

	# set max feed override
	mfo = parent.inifile.find('DISPLAY', 'MAX_FEED_OVERRIDE') or '1.0'
	if utilities.is_number(mfo):
		parent.max_feed_override = float(mfo)
	else:
		msg = (f'The INI value {mfo} for [DISPLAY] MAX_FEED_OVERRIDE\n'
		'did not evaluate to a number. LinuxCNC will shut down.')
		dialogs.error_msg_ok(msg, 'INI Error')
		sys.exit()

	# set default spindle speed
	dss = parent.inifile.find('DISPLAY', 'DEFAULT_SPINDLE_SPEED') or 0
	if utilities.is_int(dss):
		parent.spindle_speed = int(dss)
	else:
		parent.spindle_speed = 0
		msg = (f'The INI value {dss} for [DISPLAY] DEFAULT_SPINDLE_SPEED\n'
		'did not evaluate to an integer. 0 will be used.')
		dialogs.error_msg_ok(msg, 'INI Error')

	# set max spindle override
	mso = parent.inifile.find('DISPLAY', 'MAX_SPINDLE_OVERRIDE') or '1.0'
	if utilities.is_number(mso):
		parent.max_spindle_override = float(mso)
	else:
		parent.max_spindle_override = 1.0
		msg = (f'The INI value {mso} for [DISPLAY] MAX_SPINDLE_OVERRIDE\n'
		'did not evaluate to a number. 1.0 will be used')
		dialogs.error_msg_ok(msg, 'INI Error')

	# get spindle increment
	increment = parent.inifile.find('DISPLAY', 'SPINDLE_INCREMENT') or False
	if not increment:
		increment = parent.inifile.find('SPINDLE_0', 'INCREMENT') or False
	if increment and utilities.is_int(increment):
		parent.spindle_increment = int(increment)
	else:
		parent.spindle_increment = 10

	# ***** [FLEXGUI] Section *****

	# check for a RESOURCES file
	parent.resources_file = parent.inifile.find('FLEXGUI', 'RESOURCES') or False
	if parent.resources_file:
		if not os.path.exists(os.path.join(parent.config_path, parent.resources_file)):
			msg = (f'The RESOURCES file {parent.resources_file}\n'
				'Was not found. Resourses can not be imported')
			dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
			parent.resources_file = False

	# check for QSS file
	parent.qss_file = parent.inifile.find('FLEXGUI', 'QSS') or False
	if parent.qss_file:
		if not os.path.exists(os.path.join(parent.config_path, parent.qss_file)):
			msg = (f'The QSS file {parent.qss_file}\n'
				'Was not found. QSS can not be applied')
			dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
			parent.qss_file = False

	# check for popup QSS file FIXME change this to POPUP_QSS
	parent.popup_qss = parent.inifile.find('FLEXGUI', 'POPUP_QSS') or False
	if parent.popup_qss:
		if not os.path.exists(os.path.join(parent.config_path, parent.popup_qss)):
			msg = (f'The Touch Popup QSS file {parent.popup_qss}\n'
				'Was not found. QSS can not be applied')
			dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
			parent.popup_qss = os.path.join(parent.lib_path, 'popup.qss')
	else: # TOUCH_QSS not in ini file
		parent.popup_qss = os.path.join(parent.lib_path, 'popup.qss')

	# test for both THEME and QSS
	if parent.theme and parent.qss_file:
		msg = (f'The THEME {parent.theme} and QSS {parent.qss_file}\n'
			'were both found in the ini file.\n'
			f'the QSS {parent.qss_file} will not be used.\n'
			'Only one can be specified in the ini.')
		dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
		parent.qss_file = False

	# check for screen size, a non valid entry will just use self.show()
	parent.screen_size = parent.inifile.find('FLEXGUI', 'SIZE') or False

	# check for touch screen defaults, anything other than true is false
	parent.touch_spinbox = parent.inifile.find('FLEXGUI', 'TOUCH_SPINBOX') or False
	if parent.touch_spinbox:
		parent.touch_spinbox = parent.touch_spinbox.strip().lower() == "true"

	# check for LED defaults in the ini file, find returns a string must be an int
	parent.led_diameter = parent.inifile.find('FLEXGUI', 'LED_DIAMETER') or False
	if not parent.led_diameter: # no value found
		parent.led_diameter = 15
	elif not utilities.is_int(parent.led_diameter): # not an int
		msg = (f'The FLEXGUI LED_DIAMETER did not\n'
			'evaluate to and integer value.\n'
			'The LED_DIAMETER will be set to 15.')
		dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
	else:
		parent.led_diameter =  int(parent.led_diameter)

	parent.led_right_offset = parent.inifile.find('FLEXGUI', 'LED_RIGHT_OFFSET') or False
	if parent.led_right_offset is None:
		parent.led_right_offset = 5
	elif not utilities.is_int(parent.led_right_offset): # not an int
		msg = (f'The FLEXGUI LED_RIGHT_OFFSET did not\n'
			'evaluate to and integer value.\n'
			'The LED_RIGHT_OFFSET will be set to 15.')
		dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
	else:
		parent.led_right_offset =  int(parent.led_right_offset)

	parent.led_top_offset = parent.inifile.find('FLEXGUI', 'LED_TOP_OFFSET') or False
	if parent.led_top_offset is None:
		parent.led_top_offset = 5
	elif not utilities.is_int(parent.led_top_offset): # not an int
		msg = (f'The FLEXGUI LED_TOP_OFFSET did not\n'
			'evaluate to and integer value.\n'
			'The LED_TOP_OFFSET will be set to 15.')
		dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
	else:
		parent.led_top_offset =  int(parent.led_top_offset)

	# Colors are checked for validity in string_to_qcolor
	parent.led_on_color = parent.inifile.find('FLEXGUI', 'LED_ON_COLOR') or False
	if parent.led_on_color: # convert string to QColor
		parent.led_on_color = utilities.string_to_qcolor(parent, parent.led_on_color, 'LED_ON_COLOR')
	if not parent.led_on_color: # use default led on color
		parent.led_on_color = QColor(0, 255, 0, 255)

	parent.led_off_color = parent.inifile.find('FLEXGUI', 'LED_OFF_COLOR') or False
	if parent.led_off_color: # convert string to QColor
		parent.led_off_color = utilities.string_to_qcolor(parent, parent.led_off_color, 'LED_OFF_COLOR')
	if not parent.led_off_color: # use default led off color
		parent.led_off_color = QColor(255, 0, 0, 255)

	parent.probe_enable_on_color = parent.inifile.find('FLEXGUI', 'PROBE_ENABLE_ON_COLOR') or False
	if parent.probe_enable_on_color: # get a valid color string
		color = utilities.string_to_rgba(parent, parent.probe_enable_on_color, 'PROBE_ENABLE_ON_COLOR')
		if color:
			parent.probe_enable_on_color = f'background-color: {color};'

	parent.probe_enable_off_color = parent.inifile.find('FLEXGUI', 'PROBE_ENABLE_OFF_COLOR') or False
	if parent.probe_enable_off_color: # get a valid color string
		color = utilities.string_to_rgba(parent, parent.probe_enable_off_color, 'PROBE_ENABLE_OFF_COLOR')
		if color:
			parent.probe_enable_off_color = f'background-color: {color};'

	color_string = parent.inifile.find('FLEXGUI', 'PLOT_BACKGROUND_COLOR') or False
	if color_string:
		components = [c.strip() for c in color_string.split(',')]
		if len(components) == 3:
			for comp in components:
				value = float(comp)
				if not (0.0 <= value <= 1.0):
					parent.plot_background_color = False
					msg = ('The PLOT_BACKGROUND_COLOR in the\n'
					f'FLEXGUI section {color_string} is not valid.\n'
					'The plot background color will be black')
					dialogs.error_msg_ok(msg, 'Configuration Error')
					break
				parent.plot_background_color = tuple(map(float, color_string.split(',')))
	else:
		parent.plot_background_color = False

	parent.grids = parent.inifile.find('FLEXGUI', 'PLOT_GRID') or False
	parent.auto_plot_units = parent.inifile.find('FLEXGUI', 'PLOT_UNITS') or False
	parent.auto_dro_units = parent.inifile.find('FLEXGUI', 'DRO_UNITS') or False

	parent.manual_tool_change = parent.inifile.find('FLEXGUI', 'MANUAL_TOOL_CHANGE') or False
	if parent.manual_tool_change:
		parent.manual_tool_change = parent.manual_tool_change.strip().lower() == "true"

	parent.touch_file_width = parent.inifile.find('FLEXGUI', 'TOUCH_FILE_WIDTH') or False
	if parent.touch_file_width in ['True', 'true', '1']:
		parent.touch_file_width = True
	else:
		parent.touch_file_width = False

	# check for keyboard jogging
	parent.ctrl_kb_jogging = parent.inifile.find('FLEXGUI', 'KEYBOARD_JOG') or False
	if parent.ctrl_kb_jogging:
		parent.ctrl_kb_jogging = parent.ctrl_kb_jogging.strip().lower() == "true"

	# check for kb_jog_focus
	parent.kb_jog_focus = parent.inifile.find('FLEXGUI', 'KB_JOG_FOCUS')
	if parent.kb_jog_focus:
		parent.kb_jog_focus = parent.kb_jog_focus.strip().lower() == "true"

	# check for dro font size
	parent.dro_font_size = parent.inifile.find('FLEXGUI', 'DRO_FONT_SIZE') or '12'
	if not parent.dro_font_size: # no value found
		parent.dro_font_size = 12
	elif not utilities.is_int(parent.dro_font_size): # not an int
		msg = (f'The FLEXGUI DRO_FONT_SIZE did not\n'
			'evaluate to an integer value.\n'
			'The DRO_FONT_SIZE will be set to 12.')
		dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
	else:
		parent.dro_font_size =  int(parent.dro_font_size)

	# ***** [EMCIO] Section *****
	# this ini file items will cause EMC to fail to load if missing
	parent.tool_table = parent.inifile.find('EMCIO', 'TOOL_TABLE')

	# ***** [RS274NGC] Section *****
	# this ini file items will cause EMC to fail to load if missing
	parent.var_file = parent.inifile.find('RS274NGC', 'PARAMETER_FILE')

	# ***** [HAL] Section *****
	# this ini file items will cause EMC to fail to load if missing
	parent.postgui_halfiles = parent.inifile.findall('HAL', 'POSTGUI_HALFILE')

	# ***** [KINS] Section *****
	# this ini file items will cause EMC to fail to load if missing
	parent.joints = parent.inifile.find('KINS', 'JOINTS') or False
	if parent.joints: # convert string to int
		parent.joints = int(parent.joints)

	# ***** [SPINDLE_0] Section *****
	parent.min_rpm = parent.inifile.find('SPINDLE_0', 'MIN_FORWARD_VELOCITY') or False
	parent.max_rpm = parent.inifile.find('SPINDLE_0', 'MAX_FORWARD_VELOCITY') or False

	# ***** [TRAJ] Section *****
	# LINEAR_UNITS = the machine units for linear axes. Possible choices are mm or inch.
	parent.default_metric = 3
	parent.default_inch = 4

	# this ini file items will cause EMC to fail to load if missing
	match parent.inifile.find('TRAJ', 'LINEAR_UNITS'):
		case 'inch':
			parent.default_precision = 4
			parent.units = 'INCH'
		case 'mm':
			parent.default_precision = 3
			parent.units = 'MM'
		case _:
			sys.exit()

	# The maximum velocity for any axis or coordinated move, in machine units per second.
	parent.max_linear_vel = parent.inifile.find('TRAJ', 'MAX_LINEAR_VELOCITY') or False


