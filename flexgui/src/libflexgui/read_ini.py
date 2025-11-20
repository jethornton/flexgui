import os, sys

from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QColor

from libflexgui import dialogs
from libflexgui import utilities

def to_bool(value):
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    truthy = {'1', 'true', 'yes', 'y', 'on', 't'}
    falsy  = {'0', 'false', 'no', 'n', 'off', 'f'}
    val = str(value).strip().lower()
    if val in truthy:
        return True
    if val in falsy:
        return False
    raise ValueError(f"Cannot convert {value!r} to boolean")

def read(parent):
	# check for theme must be done before using any dialogs
	parent.theme = parent.inifile.find('FLEXGUI', 'THEME') or False

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
	elif parent.inifile.find('DISPLAY', 'VIEW') is not None:
		parent.default_view = parent.inifile.find('DISPLAY', 'VIEW')
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
		dialogs.error_msg_ok(parent, msg, 'INI Error')
		sys.exit()

	# set default spindle speed
	dss = parent.inifile.find('DISPLAY', 'DEFAULT_SPINDLE_SPEED') or 0
	if utilities.is_int(dss):
		parent.spindle_speed = int(dss)
	else:
		parent.spindle_speed = 0
		msg = (f'The INI value {dss} for [DISPLAY] DEFAULT_SPINDLE_SPEED\n'
		'did not evaluate to an integer. 0 will be used.')
		dialogs.error_msg_ok(parent, msg, 'INI Error')

	# set max spindle override
	mso = parent.inifile.find('DISPLAY', 'MAX_SPINDLE_OVERRIDE') or '1.0'
	if utilities.is_number(mso):
		parent.max_spindle_override = float(mso)
	else:
		parent.max_spindle_override = 1.0
		msg = (f'The INI value {mso} for [DISPLAY] MAX_SPINDLE_OVERRIDE\n'
		'did not evaluate to a number. 1.0 will be used')
		dialogs.error_msg_ok(parent, msg, 'INI Error')

	# get spindle increment
	increment = parent.inifile.find('DISPLAY', 'SPINDLE_INCREMENT') or False
	if not increment:
		increment = parent.inifile.find('SPINDLE_0', 'INCREMENT') or False
	parent.increment = int(increment) if increment else 10

	# ***** [FLEXGUI] Section *****

	# ***** Test for old entries *****
	if parent.inifile.find('DISPLAY', 'RESOURCES'):
		msg = ('The key RESOURCES has been moved from the [DISPLAY] section\n'
		'The key RESOURCES needs to be in the [FLEXGUI] section\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('DISPLAY', 'SIZE'):
		msg = ('The key SIZE has been moved from the [DISPLAY] section\n'
		'The key SIZE needs to be in the [FLEXGUI] section\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('DISPLAY', 'DRO_FONT_SIZE'):
		msg = ('DRO_FONT_SIZE has been moved to the\n'
			'[FLEXGUI] section of the ini file.\n'
			'The default font size will be used')
		dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')

	if parent.inifile.find('FLEX_COLORS', 'ESTOP_OPEN'):
		msg = ('The [FLEX_COLORS] section has been changed to [FLEXGUI]\n'
		'The key ESTOP_OPEN is now ESTOP_OPEN_COLOR\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('FLEX_COLORS', 'ESTOP_CLOSED'):
		msg = ('The [FLEX_COLORS] section has been changed to [FLEXGUI]\n'
		'The key ESTOP_CLOSED is now ESTOP_CLOSED_COLOR\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('FLEX_COLORS', 'POWER_OFF'):
		msg = ('The [FLEX_COLORS] section has been changed to [FLEXGUI]\n'
		'The key POWER_OFF is now POWER_OFF_COLOR\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('FLEX_COLORS', 'POWER_ON'):
		msg = ('The [FLEX_COLORS] section has been changed to [FLEXGUI]\n'
		'The key POWER_ON is now POWER_ON_COLOR\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('FLEX', 'PLOT_BACKGROUND_COLOR'):
		msg = ('The [FLEX] section has been changed to [FLEXGUI]\n'
		'The key PLOT_BACKGROUND_COLOR needs to be in the [FLEXGUI] section\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('FLEX', 'TOUCH_FILE_WIDTH'):
		msg = ('The [FLEX] section has been changed to [FLEXGUI]\n'
		'The key TOUCH_FILE_WIDTH needs to be in the [FLEXGUI] section\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('FLEX', 'MANUAL_TOOL_CHANGE'):
		msg = ('The [FLEX] section has been changed to [FLEXGUI]\n'
		'The key MANUAL_TOOL_CHANGE needs to be in the [FLEXGUI] section\n'
		'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.findall('FLEX', 'IMPORT'):
		msg = ('The [FLEX] section has been changed to [FLEXGUI]\n'
		'The key IMPORT has been changed to IMPORT_PYTHON\n'
		'Check Python section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('DISPLAY', 'THEME'):
		msg = ('THEME has been moved to the [FLEXGUI]\n'
			'section of the ini file.\n'
			'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	if parent.inifile.find('DISPLAY', 'QSS'):
		msg = ('QSS has been moved to the [FLEXGUI]\n'
			'section of the ini file.\n'
			'Check the INI section of the Documents for correct INI entries.')
		dialogs.warn_msg_ok(parent, msg, 'Configuration Error')

	# check for a RESOURCES
	parent.resources_file = parent.inifile.find('FLEXGUI', 'RESOURCES') or False

	# check for QSS
	parent.qss_file = parent.inifile.find('FLEXGUI', 'QSS') or False

	# test for both THEME and QSS
	if parent.theme and parent.qss_file:
		msg = (f'The THEME {parent.theme} and QSS {parent.qss_file}\n'
			'were both found in the ini file.\n'
			f'the QSS {parent.qss_file} will not be used.\n'
			'Only one can be specified in the ini.')
		dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')
		parent.qss_file = False

	# check for screen size
	parent.screen_size = parent.inifile.find('FLEXGUI', 'SIZE') or False

	# check for touch screen defaults
	parent.touch_spinbox = to_bool(parent.inifile.find('FLEXGUI', 'TOUCH_SPINBOX') or False)

	# check for LED defaults in the ini file
	parent.led_diameter = parent.inifile.find('FLEXGUI', 'LED_DIAMETER')
	if parent.led_diameter is None:
		parent.led_diameter = 15
	else:
		parent.led_diameter =  int(parent.led_diameter)

	parent.led_right_offset = parent.inifile.find('FLEXGUI', 'LED_RIGHT_OFFSET')
	if parent.led_right_offset is None:
		parent.led_right_offset = 5
	else:
		parent.led_right_offset =  int(parent.led_right_offset)

	parent.led_top_offset = parent.inifile.find('FLEXGUI', 'LED_TOP_OFFSET')
	if parent.led_top_offset is None:
		parent.led_top_offset = 5
	else:
		parent.led_top_offset =  int(parent.led_top_offset)

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

	# FIXME remove this in 1.3.2
	color_nag = False
	parent.estop_open_color = parent.inifile.find('FLEXGUI', 'ESTOP_OPEN_COLOR') or False
	if parent.estop_open_color: # get a valid color string
		color = utilities.string_to_rgba(parent, parent.estop_open_color, 'ESTOP_OPEN_COLOR')
		if color:
			parent.estop_open_color = f'background-color: {color};'
			color_nag = True

	# FIXME remove this in 1.3.2
	parent.estop_closed_color = parent.inifile.find('FLEXGUI', 'ESTOP_CLOSED_COLOR') or False
	if parent.estop_closed_color: # get a valid color string
		color = utilities.string_to_rgba(parent, parent.estop_closed_color, 'ESTOP_CLOSED_COLOR')
		if color:
			parent.estop_closed_color = f'background-color: {color};'
			color_nag = True

	# FIXME remove this in 1.3.2
	parent.power_off_color = parent.inifile.find('FLEXGUI', 'POWER_OFF_COLOR') or False
	if parent.power_off_color: # get a valid color string
		color = utilities.string_to_rgba(parent, parent.power_off_color, 'POWER_OFF_COLOR')
		if color:
			parent.power_off_color = f'background-color: {color};'
			color_nag = True

	# FIXME remove this in 1.3.2
	parent.power_on_color = parent.inifile.find('FLEXGUI', 'POWER_ON_COLOR') or False
	if parent.power_on_color: # get a valid color string
		color = utilities.string_to_rgba(parent, parent.power_on_color, 'POWER_ON_COLOR')
		if color:
			parent.power_on_color = f'background-color: {color};'
			color_nag = True

	if color_nag:
		msg = (f'The FLEXGUI E Stop and Power Colors\n'
		'function from the ini file will be removed in v1.3.2.\n'
		'Use the qss stylesheet to set this option.\n'
		'See the Stylesheet Controls section of the\n'
		'Documents for instructions.')
		dialogs.warn_msg_ok(parent, msg, 'INI Configuration ERROR!')

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

	parent.plot_background_color = parent.inifile.find('FLEXGUI', 'PLOT_BACKGROUND_COLOR') or False
	if parent.plot_background_color:
		parent.plot_background_color = tuple(map(float, parent.plot_background_color.split(',')))

	parent.auto_plot_units = to_bool(parent.inifile.find('FLEXGUI', 'PLOT_UNITS') or False)
	parent.auto_dro_units = to_bool(parent.inifile.find('FLEXGUI', 'DRO_UNITS') or False)

	parent.manual_tool_change = to_bool(parent.inifile.find('FLEXGUI', 'MANUAL_TOOL_CHANGE') or False)

	parent.touch_file_width = parent.inifile.find('FLEXGUI', 'TOUCH_FILE_WIDTH') or False
	if parent.touch_file_width in ['True', 'true', '1']:
		parent.touch_file_width = True
	else:
		parent.touch_file_width = False

	# check for keyboard jogging
	parent.ctrl_kb_jogging = to_bool(parent.inifile.find('FLEXGUI', 'KEYBOARD_JOG') or False)
	parent.no_ctrl_kb_jogging = to_bool(parent.inifile.find('FLEXGUI', 'NO_CTRL_KEYBOARD_JOGGING') or False)

	# disable keyboard jog during text endry
	parent.text_entry_keyboard_jog_disable = to_bool(parent.inifile.find('FLEXGUI', 'TEXT_ENTRY_KEYBOARD_JOG_DISABLE') or False)

	# check for dro font size
	parent.dro_font_size = parent.inifile.find('FLEXGUI', 'DRO_FONT_SIZE') or '12'

	# ***** [EMCIO] Section *****
	parent.tool_table = parent.inifile.find('EMCIO', 'TOOL_TABLE') or False

	# ***** [RS274NGC] Section *****
	parent.var_file = parent.inifile.find('RS274NGC', 'PARAMETER_FILE') or False

	# ***** [HAL] Section *****
	parent.postgui_halfiles = parent.inifile.findall('HAL', 'POSTGUI_HALFILE') or False

	# ***** [KINS] Section *****
	# FIXME this might be better than status.joints which fails sometimes
	parent.joints = parent.inifile.find('KINS', 'JOINTS') or False

	# ***** [SPINDLE_0] Section *****
	parent.min_rpm = parent.inifile.find('SPINDLE_0', 'MIN_FORWARD_VELOCITY') or False
	parent.max_rpm = parent.inifile.find('SPINDLE_0', 'MAX_FORWARD_VELOCITY') or False

	# ***** [TRAJ] Section *****
	# LINEAR_UNITS = the machine units for linear axes. Possible choices are mm or inch.
	parent.default_metric = 3
	parent.default_inch = 4
	match parent.inifile.find('TRAJ', 'LINEAR_UNITS') or False:
		case 'inch':
			parent.default_precision = 4
			parent.units = 'INCH'
		case 'mm':
			parent.default_precision = 3
			parent.units = 'MM'
		case _:
			msg = ('[TRAJ] LINEAR_UNITS is a required\n'
			'INI entry. LinuxCNC will close now.')
			dialogs.error_msg_ok(parent, msg, 'Configuration Error')
			sys.exit()

	# The maximum velocity for any axis or coordinated move, in machine units per second.
	parent.max_linear_vel = parent.inifile.find('TRAJ', 'MAX_LINEAR_VELOCITY') or False


