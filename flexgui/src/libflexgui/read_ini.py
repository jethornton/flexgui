import os, sys

from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget

from libflexgui import dialogs
from libflexgui import utilities

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
	directory = parent.inifile.find('DISPLAY', 'PROGRAM_PREFIX')
	print(f'directory {directory}')

	# get the path to the nc code directory
	if directory == None: # no ini entry
		paths = ['~/linuxcnc/nc_files', '~/linuxcnc', '~']
		for path in paths:
			if os.path.isdir(os.path.expanduser(path)):
				parent.nc_code_dir = os.path.expanduser(path)
				break
	elif directory.startswith('./'): # in this directory
		directory = os.path.join(parent.config_path, directory[2:])
	elif directory.startswith('../'): # up one directory
		directory = os.path.join(os.path.dirname(parent.config_path), directory[3:])
	elif directory.startswith('~'): # users home directory
		directory = os.path.expanduser(directory)

	if directory is not None:
		if os.path.isdir(directory):
			parent.nc_code_dir = directory
		else: # verified
			title = 'Configuration Error'
			msg = (f'The INI entry [DISPLAY] PROGRAM_PREFIX "{directory}" does not exist.')
			info = f'{os.path.expanduser("~/")} will be used.'
			dialogs.error_msg_ok(parent, title, msg, info)
			parent.nc_code_dir = os.path.expanduser('~/')

	parent.editor = parent.inifile.find('DISPLAY', 'EDITOR') or False

	parent.tool_editor = parent.inifile.find('DISPLAY', 'TOOL_EDITOR') or False

	if parent.inifile.find('DISPLAY', 'LATHE') is not None:
		parent.default_view = 'y'
	elif parent.inifile.find('FLEXGUI', 'PLOT_VIEW') is not None:
		parent.default_view = parent.inifile.find('FLEXGUI', 'PLOT_VIEW')
	else:
		parent.default_view = 'p'

	# the check for valid increments is done in startup.py
	if (parent.inifile.find('FLEXGUI', 'JOG_INCREMENTS') and
		parent.inifile.find('DISPLAY', 'INCREMENTS')): # verified
		title = 'Configuration Error'
		msg = ('Both DISPLAY INCREMENTS and FLEXGUI JOG_INCREMENTS were found.')
		info = 'FLEXGUI JOG_INCREMENTS will be used.'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.jog_increments = False
	else:
		parent.jog_increments = parent.inifile.find('DISPLAY', 'INCREMENTS') or False

	# check for default file to open
	parent.open_file = parent.inifile.find('DISPLAY', 'OPEN_FILE') or False

	# set max feed override if not a number shut down
	mfo = parent.inifile.find('DISPLAY', 'MAX_FEED_OVERRIDE') or '1.0'
	if utilities.is_number(mfo):
		parent.max_feed_override = float(mfo)
	else: # verified
		title = 'Critical Error!'
		msg = (f'The INI entry [DISPLAY] MAX_FEED_OVERRIDE "{mfo}" '
		'did not evaluate to a number.')
		info = 'LinuxCNC will shut down!'
		dialogs.error_msg_ok(parent, title, msg, info)
		sys.exit()

	# ***** [FLEXGUI] Section *****

	# check for POPUP_QSS file, this must be checked first before any dialogs
	parent.popup_qss = parent.inifile.find('FLEXGUI', 'POPUP_QSS') or False
	if parent.popup_qss:
		if not os.path.exists(os.path.join(parent.config_path, parent.popup_qss)): # verified
			title = 'INI Error!'
			msg = (f'The INI entry [FLEXGUI] POPUP_QSS file "{parent.popup_qss}" Was '
			'not found.')
			info = 'The default Popup QSS will be used.'
			dialogs.error_msg_ok(parent, title, msg, info)
			parent.popup_qss = os.path.join(parent.lib_path, 'popup.qss')
	else: # POPUP_QSS not in ini file
		parent.popup_qss = os.path.join(parent.lib_path, 'popup.qss')

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
		if parent.inifile.find(item[0], item[1]): # verified
			title = 'Configuration Error'
			msg = (f'The key "{item[1]}" has been moved from the [{item[0]}] section '
			'or is no longer used by FlexGUI or the name has been changed. Check the '
			'INI section of the Documents for correct INI entries.')
			dialogs.error_msg_ok(parent, title, msg)

	old_display_spindle_items = [
	['DISPLAY', 'DEFAULT_SPINDLE_SPEED'],
	['DISPLAY', 'SPINDLE_INCREMENT'],
	['DISPLAY', 'MAX_SPINDLE_OVERRIDE']
	]

	for item in old_display_spindle_items:
		if parent.inifile.find(item[0], item[1]): # verified
			title = 'Configuration Error'
			msg = (f'The key "{item[1]}" in the [{item[0]}] section was depreciated '
			'with multiple spindles addition. The Spindle keys are now in [SPINDLE_0] '
			'section. Check the INI section of the Documents for correct INI entries.')
			dialogs.error_msg_ok(parent, title, msg)

	old_probe_items = [
	['FLEXGUI', 'PROBE_ENABLE_ON_COLOR'],
	['FLEXGUI', 'PROBE_ENABLE_OFF_COLOR'],
	]

	for item in old_probe_items:
		if parent.inifile.find(item[0], item[1]): # verified
			title = 'Configuration Error'
			msg = (f'The key "{item[1]}" in the [{item[0]}] section was depreciated. '
			'Use the stylesheet to set the On and Off colors. See the probing '
			'section of the manual.')
			info = 'The Probe On/Off Colors will not function!'
			dialogs.error_msg_ok(parent, title, msg, info)

	old_spindle_items = []
	old_spindle_keys = ['MIN_FORWARD_VELOCITY', 'MAX_FORWARD_VELOCITY']
	for item in old_spindle_keys:
		for i in range(9):
			old_spindle_items.append([f'SPINDLE_{i}', item])
	for item in old_spindle_items:
		if parent.inifile.find(item[0], item[1]): # verified
			title = 'Configuration Error'
			msg = (f'The key "{item[1]}" in the [{item[0]}] section was depreciated. '
			'Check the INI section of the Documents for correct INI entries.')
			dialogs.error_msg_ok(parent, title, msg)

	old_jog_items = [
	['DISPLAY', 'MIN_LINEAR_VELOCITY'],
	['DISPLAY', 'DEFAULT_LINEAR_VELOCITY'],
	['DISPLAY', 'MAX_LINEAR_VELOCITY'],
	]

	for item in old_jog_items:
		if parent.inifile.find(item[0], item[1]): # verified
			title = 'Configuration Error'
			msg = (f'The jog settings key "{item[1]}" in the [{item[0]}] section was '
			'depreciated. Check the INI section of the Documents for correct INI entries.')
			info = 'The Jog Setting will not be used!'
			dialogs.error_msg_ok(parent, title, msg, info)

	# check for CYCLE_TIME
	parent.cycle_time = parent.inifile.find('FLEXGUI', 'CYCLE_TIME') or 100
	if isinstance(parent.cycle_time, str): # the ini file had a setting
		if utilities.is_int(parent.cycle_time):
			parent.cycle_time = int(parent.cycle_time)
			if not 50 <= parent.cycle_time <= 200: # verified
				title = 'Configuration Error'
				msg = (f'The INI entry [FLEXGUI] CYCLE_TIME value '
				'"{parent.cycle_time}" is not in the range of 50-200.')
				info = 'The cycle time will be set to 100 ms!'
				dialogs.error_msg_ok(parent, title, msg, info)
				parent.cycle_time = 100
		else: # verified
			title = 'Configuration Error'
			msg = (f'The INI entry [FLEXGUI] CYCLE_TIME value '
			'"{parent.cycle_time}" did not evaluate to a number.')
			info = 'The cycle time will be set to 100 ms!'
			dialogs.error_msg_ok(parent, title, msg, info)
			parent.cycle_time = 100

	# check for jog velocity settings
	# minimum jog velocity
	min_jog_vel = parent.inifile.find('FLEXGUI','MIN_JOG_VELOCITY')
	if min_jog_vel is None:
		parent.min_jog_vel = False
	elif utilities.is_number(min_jog_vel):
		parent.min_jog_vel = min_jog_vel
	else:
		title = 'Configuration Error'
		msg = (f'The INI entry [FLEXGUI] MIN_JOG_VELOCITY value '
		f'"{min_jog_vel}" did not evaluate to a number.')
		info = 'The MIN_JOG_VELOCITY will be set to 0!'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.min_jog_vel = 0

	# default jog velocity
	default_jog_vel = parent.inifile.find('FLEXGUI','DEFAULT_JOG_VELOCITY')
	if default_jog_vel is None:
		parent.default_jog_vel = False
	elif utilities.is_number(default_jog_vel):
		parent.default_jog_vel = default_jog_vel
	else:
		title = 'Configuration Error'
		msg = (f'The INI entry [FLEXGUI] DEFAULT_JOG_VELOCITY value '
		f'"{default_jog_vel}" did not evaluate to a number.')
		info = 'The DEFAULT_JOG_VELOCITY will not be used!'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.default_jog_vel = False

	# maximum jog velocity
	max_jog_vel = parent.inifile.find('FLEXGUI','MAX_JOG_VELOCITY')
	if max_jog_vel is None:
		parent.max_jog_vel = False
	elif utilities.is_number(max_jog_vel):
		parent.max_jog_vel = max_jog_vel
	else:
		title = 'Configuration Error'
		msg = (f'The INI entry [FLEXGUI] MAX_JOG_VELOCITY value '
		f'"{max_jog_vel}" did not evaluate to a number.')
		info = 'The MAX_JOG_VELOCITY will not be used!'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.max_jog_vel = False

	# check for FLASH time
	flash_time = parent.inifile.find('FLEXGUI', 'FLASH_TIME') or '1000'
	if utilities.is_int(flash_time):
		parent.flash_time = int(flash_time)
	else: # verified
		parent.flash_time = 1000
		title = 'INI Error!'
		msg = (f'The INI entry [FLEXGUI] FLASH_TIME value "{flash_time}" '
		'did not evaluate to an integer.')
		info = '1000 will be used.'
		dialogs.error_msg_ok(parent, title, msg, info)

	# check for a RESOURCES file
	parent.resources_file = parent.inifile.find('FLEXGUI', 'RESOURCES') or False
	if parent.resources_file:
		if not os.path.exists(os.path.join(parent.config_path, parent.resources_file)): # verified
			title = 'Configuration Error'
			msg = (f'The INI entry [FLEXGUI] RESOURCES file "{parent.resources_file}" '
			'was not found.')
			info = 'Resourses can not be imported!'
			dialogs.error_msg_ok(parent, title, msg, info)
			parent.resources_file = False

	# check for QSS file
	parent.qss_file = parent.inifile.find('FLEXGUI', 'QSS') or False
	if parent.qss_file:
		if not os.path.exists(os.path.join(parent.config_path, parent.qss_file)): # verified
			title = 'Configuration Error'
			msg = (f'The INI entry [FLEXGUI] QSS file "{parent.qss_file}" was not found.')
			info = 'The Style Sheet can not be applied!'
			dialogs.error_msg_ok(parent, title, msg, info)
			parent.qss_file = False

	# test for both THEME and QSS
	if parent.theme and parent.qss_file: # verified
		title = 'Configuration Error'
		msg = (f'The INI entry [FLEXGUI] THEME "{parent.theme}" and QSS '
		f'"{parent.qss_file}" were both found in the ini file. The QSS '
		f'"{parent.qss_file}" will not be used.')
		info = 'Only one can be specified in the ini.'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.qss_file = False

	# check for screen size, a non valid entry will just use self.show()
	parent.screen_size = parent.inifile.find('FLEXGUI', 'SIZE') or False

	# check for touch screen defaults, anything other than true is false
	touch_spinbox = parent.inifile.find('FLEXGUI', 'TOUCH_SPINBOX') or 'false'
	parent.touch_spinbox = touch_spinbox.strip().lower() == 'true'

	# check for LED defaults in the ini file, find returns a string must be an int
	led_diameter = parent.inifile.find('FLEXGUI', 'LED_DIAMETER') or False
	if not led_diameter: # no value found
		parent.led_diameter = 15
	elif not utilities.is_int(led_diameter): # verified
		title = 'Configuration Error'
		msg = (f'The INI entry [FLEXGUI] LED_DIAMETER "{led_diameter}" did not '
		'evaluate to an integer value.')
		info = 'The LED_DIAMETER will be set to 15.'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.led_diameter = 15
	else:
		parent.led_diameter =  int(led_diameter)

	led_right_offset = parent.inifile.find('FLEXGUI', 'LED_RIGHT_OFFSET')
	if led_right_offset is None:
		parent.led_right_offset = 5
	elif not utilities.is_int(led_right_offset): # verified
		title = 'Configuration Error'
		msg = (f'The INI entry [FLEXGUI] LED_RIGHT_OFFSET "{led_right_offset}" did '
		'not evaluate to an integer value.')
		info = 'The LED_RIGHT_OFFSET will be set to 5.'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.led_right_offset = 5
	else:
		parent.led_right_offset =  int(led_right_offset)

	led_top_offset = parent.inifile.find('FLEXGUI', 'LED_TOP_OFFSET')
	if led_top_offset is None:
		parent.led_top_offset = 5
	elif not utilities.is_int(led_top_offset): # verified
		title = 'Configuration Error'
		msg = (f'The INI entry [FLEXGUI] LED_TOP_OFFSET "{led_top_offset}" did not '
		'evaluate to an integer value.')
		info = 'The LED_TOP_OFFSET will be set to 5.'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.led_top_offset = 5
	else:
		parent.led_top_offset =  int(led_top_offset)

	led_on = parent.inifile.find('FLEXGUI', 'LED_ON_COLOR')
	if led_on is not None:
		led_on_color = utilities.is_valid_qcolor(led_on)
		if led_on_color:
			parent.led_on_color = led_on_color
		else: # verified
			title = 'Configuration Error'
			msg = (f'The INI entry [FLEXGUI] LED_ON_COLO" value "{led_on}" is not a '
			'valid RGB or HEX color string.')
			info = 'The default color will be used.'
			dialogs.error_msg_ok(parent, title, msg, info)
			parent.led_on_color = QColor(0, 255, 0, 255)
	else:
		parent.led_on_color = QColor(0, 255, 0, 255)

	led_off = parent.inifile.find('FLEXGUI', 'LED_OFF_COLOR')
	if led_off is not None:
		led_off_color = utilities.is_valid_qcolor(led_off)
		if led_off_color:
			parent.led_off_color = led_off_color
		else: # verified
			title = 'Configuration Error'
			msg = (f'The INI entry [FLEXGUI] LED_OFF_COLOR value "{led_off}" is not a '
			'valid RGB or HEX color string.')
			info = 'The default color will be used.'
			dialogs.error_msg_ok(parent, title, msg, info)
			parent.led_off_color = QColor(255, 0, 0, 255)
	else:
		parent.led_off_color = QColor(255, 0, 0, 255)

	#### Plotter Settings ####
	plotter = parent.findChild(QWidget, 'plot_widget')

	if plotter is not None:
		color_string = parent.inifile.find('FLEXGUI', 'PLOT_BACKGROUND_COLOR') or False
		if color_string:
			components = [c.strip() for c in color_string.split(',')]
			if len(components) == 3:
				for comp in components:
					try:
						value = float(comp)
					except ValueError:
						value = False
					if not (0.0 <= value <= 1.0) or value is False: # verified
						parent.plot_background_color = False
						title = 'INI Configuration Error!'
						msg = (f'The INI entry [FLEXGUI] PLOT_BACKGROUND_COLOR '
						f'"{color_string}" is not a valid plotter color. Each color must '
						'be in the range of 0.0 to 1.0.')
						info = 'The background color will be black'
						dialogs.error_msg_ok(parent, title, msg, info)
						break
					parent.plot_background_color = tuple(map(float, color_string.split(',')))
		else:
			parent.plot_background_color = False

		parent.grids = parent.inifile.find('FLEXGUI', 'PLOT_GRID') or False

		auto_plot_units = parent.inifile.find('FLEXGUI', 'PLOT_UNITS') or 'false'
		parent.auto_plot_units = auto_plot_units.strip().lower() == 'true'
	else:
		parent.plot_background_color = False
		parent.grids = False
		parent.auto_plot_units = False

	auto_dro_units = parent.inifile.find('FLEXGUI', 'DRO_UNITS') or 'false'
	parent.auto_dro_units = auto_dro_units.strip().lower() == 'true'

	manual_tool_change = parent.inifile.find('FLEXGUI', 'MANUAL_TOOL_CHANGE') or 'false'
	parent.manual_tool_change = manual_tool_change.strip().lower() == 'true'

	touch_file_width = parent.inifile.find('FLEXGUI', 'TOUCH_FILE_WIDTH') or 'false'
	parent.touch_file_width = touch_file_width.strip().lower() == 'true'

	# the check for valid increments is done in startup.py
	if not parent.jog_increments:
		parent.jog_increments = parent.inifile.find('FLEXGUI', 'JOG_INCREMENTS') or False

	# check for keyboard jog increment setting
	kb_jog_increment = parent.inifile.find('FLEXGUI', 'KB_JOG_INCREMENT') or 'false'
	parent.kb_jog_increment = kb_jog_increment.strip().lower() == 'true'

	# check for keyboard jogging
	ctrl_kb_jogging = parent.inifile.find('FLEXGUI', 'KEYBOARD_JOG') or 'false'
	parent.ctrl_kb_jogging = ctrl_kb_jogging.strip().lower() == 'true'

	# check for kb_jog_focus
	kb_jog_focus = parent.inifile.find('FLEXGUI', 'KB_JOG_FOCUS') or 'false'
	parent.kb_jog_focus = kb_jog_focus.strip().lower() == 'true'

	# check for dro font size
	dro_font_size = parent.inifile.find('FLEXGUI', 'DRO_FONT_SIZE') or '12'
	if not dro_font_size: # no value found
		parent.dro_font_size = 12
	elif not utilities.is_int(dro_font_size): # verified
		title = 'Configuration Error'
		msg = (f'The INI entry [FLEXGUI] DRO_FONT_SIZE "{dro_font_size}" did not '
		'evaluate to an integer value.')
		info = 'The DRO_FONT_SIZE will be set to 12.'
		dialogs.error_msg_ok(parent, title, msg, info)
		parent.dro_font_size = 12
	else:
		parent.dro_font_size =  int(dro_font_size)

	# Digital I/O
	dio = parent.inifile.find('FLEXGUI', 'DIO') or False
	if isinstance(dio, str):
		parent.dio = utilities.to_int(dio)
	else:
		parent.dio = 4

	# Analog I/O
	aio = parent.inifile.find('FLEXGUI', 'AIO') or 4
	if isinstance(aio, str):
		parent.aio = utilities.to_int(aio)
	else:
		parent.aio = 4

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

	# ***** [SPINDLE_n] Sections ***** 
	if parent.status.spindles == 0:
		increment = parent.inifile.find('SPINDLE_0', 'INCREMENT')
		if increment is not None:
			title = 'Configuration Error'
			msg = (f'The INI entry SPINDLE_0 INCREMENT "{increment}" did not '
			'evaluate to an integer value. This entry is used somehow by LinuxCNC.')
			info = 'LinuxCNC will now SHUT DOWN!'
			dialogs.error_msg_ok(parent, title, msg, info)
			sys.exit()

	for i in range(parent.status.spindles):

		#### MIN_RPM ####
		min_rpm = parent.inifile.find(f'SPINDLE_{i}', 'MIN_RPM')
		if min_rpm is None: # no ini entry
			setattr(parent, f'spindle_{i}_min_fwd_rpm', 0)
		elif not utilities.is_int(min_rpm): # ini entry not a valid int
			title = 'Configuration Error'
			msg = (f'The INI entry SPINDLE_{i} MIN_RPM "{min_rpm}" did not '
			'evaluate to an integer value.')
			info = 'The "MIN_RPM" will be set to 0.'
			dialogs.error_msg_ok(parent, title, msg, info)
			setattr(parent, f'spindle_{i}_min_fwd_rpm', 0)
		else: # valid ini entry
			min_rpm = utilities.to_int(min_rpm, 0)
			if min_rpm >= 0:
				setattr(parent, f'spindle_{i}_min_fwd_rpm', min_rpm)
			else:
				title = 'Configuration Error'
				msg = (f'The INI entry SPINDLE_{i} MIN_RPM "{min_rpm}" is not greater '
				'than or equal to 0')
				info = 'The "MIN_RPM" will be set to 0.'
				dialogs.error_msg_ok(parent, title, msg, info)
				setattr(parent, f'spindle_{i}_min_fwd_rpm', 0)

		#### MAX_RPM ####
		max_rpm = parent.inifile.find(f'SPINDLE_{i}', 'MAX_RPM')
		if max_rpm is None: # no ini entry
			setattr(parent, f'spindle_{i}_max_fwd_rpm', 1000)
		elif not utilities.is_int(max_rpm): # ini entry not a valid int
			title = 'Configuration Error'
			msg = (f'The INI entry SPINDLE_{i} MAX_RPM "{max_rpm}" did not '
			'evaluate to an integer value.')
			info = 'The "MAX_RPM" will be set to 1000.'
			dialogs.error_msg_ok(parent, title, msg, info)
			setattr(parent, f'spindle_{i}_max_fwd_rpm', 1000)
		else: # valid ini entry
			max_rpm = utilities.to_int(max_rpm, 1000)
			min_rpm = getattr(parent, f'spindle_{i}_min_fwd_rpm')
			if max_rpm > 0:
				setattr(parent, f'spindle_{i}_max_fwd_rpm', max_rpm)
			else:
				title = 'Configuration Error'
				msg = (f'The INI entry SPINDLE_{i} MAX_RPM "{max_rpm}" is not greater '
				'than 0')
				info = 'The "MAX_RPM" will be set to 1000.'
				dialogs.error_msg_ok(parent, title, msg, info)
				setattr(parent, f'spindle_{i}_max_fwd_rpm', 1000)
			if min_rpm > max_rpm:
				title = 'Configuration Error'
				msg = (f'The INI entry SPINDLE_{i} MIN_RPM "{min_rpm}" is greater '
				f'than MAX_RPM "{max_rpm}"')
				info = f'The "MIN_RPM" will be set to "{max_rpm}".'
				dialogs.error_msg_ok(parent, title, msg, info)
				setattr(parent, f'spindle_{i}_min_fwd_rpm', max_rpm)

		#### INCREMENT ####
		increment = parent.inifile.find(f'SPINDLE_{i}', 'INCREMENT')
		if increment is None: # no ini entry
			setattr(parent, f'spindle_{i}_rpm_increment', 100)
		elif not utilities.is_int(increment): # ini entry not a valid int
			title = 'Configuration Error'
			msg = (f'The INI entry SPINDLE_{i} INCREMENT "{increment}" did not '
			'evaluate to an integer value.')
			info = 'The "INCREMENT" will be set to 100.'
			dialogs.error_msg_ok(parent, title, msg, info)
			setattr(parent, f'spindle_{i}_rpm_increment', 100)
		else: # valid ini entry
			increment = utilities.to_int(increment, 100)
			max_rpm = getattr(parent, f'spindle_{i}_max_fwd_rpm')
			if 0 < increment <= max_rpm:
				setattr(parent, f'spindle_{i}_rpm_increment', utilities.to_int(increment, 100))
			else:
				title = 'Configuration Error'
				msg = (f'The INI entry SPINDLE_{i} INCREMENT "{increment}" is not '
				f'greater than 0 or less than MAX_RPM "{max_rpm}".')
				info = 'The "INCREMENT" will be set to 100.'
				dialogs.error_msg_ok(parent, title, msg, info)
				setattr(parent, f'spindle_{i}_rpm_increment', 100)

		#### DEFAULT_RPM ####
		default_rpm = parent.inifile.find(f'SPINDLE_{i}', 'DEFAULT_RPM')
		if default_rpm is None: # no ini entry
			setattr(parent, f'spindle_rpm_{i}', 100)
		elif not utilities.is_int(default_rpm): # ini entry not a valid int
			title = 'Configuration Error'
			msg = (f'The INI entry SPINDLE_{i} DEFAULT_RPM "{default_rpm}" did not '
			'evaluate to an integer value.')
			info = 'The "DEFAULT_RPM" will be set to 100.'
			dialogs.error_msg_ok(parent, title, msg, info)
			setattr(parent, f'spindle_rpm_{i}', 100)
		else: # verified
			default_rpm = utilities.to_int(default_rpm, 100)
			min_rpm = getattr(parent, f'spindle_{i}_min_fwd_rpm')
			max_rpm = getattr(parent, f'spindle_{i}_max_fwd_rpm')
			if min_rpm <= default_rpm <= max_rpm:
				setattr(parent, f'spindle_rpm_{i}', default_rpm)
			else:
				title = 'Configuration Error'
				msg = (f'The INI entry SPINDLE_{i} DEFAULT_RPM "{default_rpm}" is not '
				f'between or equal to MIN_RPM "{min_rpm}" or MAX_RPM "{max_rpm}".')
				info = f'The "DEFAULT_RPM" will be set to {max(min_rpm, min(default_rpm, max_rpm))}.'
				dialogs.error_msg_ok(parent, title, msg, info)
				setattr(parent, f'spindle_rpm_{i}', max(min_rpm, min(default_rpm, max_rpm)))

		min_override = parent.inifile.find(f'SPINDLE_{i}', 'MIN_OVERRIDE') or False
		if isinstance(min_override, str):
			min_override = utilities.to_int(min_override, 0)
		else:
			min_override = 0
		setattr(parent, f'spindle_{i}_min_override', min_override)

		max_override = parent.inifile.find(f'SPINDLE_{i}', 'MAX_OVERRIDE') or False
		if isinstance(max_override, str):
			max_override = utilities.to_int(max_override, 100)
			if max_override < 100: # verified
				title = 'Configuration Error'
				msg = (f'SPINDLE_{i} MAX_OVERRIDE is set to "{max_override}". '
				'The minimum for MAX_OVERRIDE is 100.')
				info = 'MAX_OVERRIDE has been set to 100.'
				dialogs.error_msg_ok(parent, title, msg, info)
				max_override = 100
		else:
			max_override = 100
		setattr(parent, f'spindle_{i}_max_override', max_override)

	# ***** [TRAJ] Section *****
	# LINEAR_UNITS = the machine units for linear axes. Possible choices are mm or inch.
	parent.default_metric = 3
	parent.default_inch = 4

	# this ini file items will cause EMC to fail to load if missing
	match parent.inifile.find('TRAJ', 'LINEAR_UNITS'):
		case 'inch':
			parent.default_precision = 4
			parent.units = 'IN'
		case 'mm':
			parent.default_precision = 3
			parent.units = 'MM'
		case _:
			sys.exit()

	# The maximum velocity for any axis or coordinated move, in machine units per second.
	parent.max_linear_vel = parent.inifile.find('TRAJ', 'MAX_LINEAR_VELOCITY') or False


