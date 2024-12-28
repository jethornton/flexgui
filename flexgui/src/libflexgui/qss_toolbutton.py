from functools import partial

from libflexgui import qss_toolbar

def startup(parent):

	# QToolButton
	parent.tb_normal = False
	parent.tb_apply_style.clicked.connect(partial(tb_create_stylesheet, parent))

	parent.tb_min_width_normal.valueChanged.connect(parent.size)
	parent.tb_min_height_normal.valueChanged.connect(parent.size)
	parent.tb_max_width_normal.valueChanged.connect(parent.size)
	parent.tb_max_height_normal.valueChanged.connect(parent.size)

	border_types = ['none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	abstract_button_states = ['normal', 'hover', 'pressed', 'checked', 'disabled']

	for item in abstract_button_states: # populate border combo boxes
		getattr(parent, f'tb_border_type_{item}').addItems(border_types)
		setattr(parent, f'tb_{item}', False)
		setattr(parent, f'tbtn_fg_color_{item}', False)
		setattr(parent, f'tbtn_bg_color_{item}', False)
		setattr(parent, f'tbtn_border_color_{item}', False)

	for state in abstract_button_states: # color dialog connections
		getattr(parent, f'tb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'tb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'tb_border_color_{state}').clicked.connect(parent.color_dialog)

	parent.tb_font_picker.clicked.connect(parent.font_dialog)
	parent.tb_font_family = False
	parent.tb_font_size = False
	parent.tb_font_weight = False
	parent.tb_font_style = False
	parent.tb_font_italic = False

######### QToolButton Stylesheet #########

def tb_create_stylesheet(parent):
	style = False

	# check for toolbar style set
	if parent.sender().objectName() == 'tb_apply_style':
		if parent.tbar_normal:
			style = qss_toolbar.tbar_create_stylesheet(parent)

	# QToolButton normal pseudo-state
	if parent.tb_normal:

		if style: # style is not False
			style += 'QToolBar QToolButton {\n'
		else:
			style = 'QToolBar QToolButton {\n'

		# color 
		if parent.tbtn_fg_color_normal:
			style += f'\tcolor: {parent.tbtn_fg_color_normal};\n'
		if parent.tbtn_bg_color_normal:
			style += f'\tbackground-color: {parent.tbtn_bg_color_normal};\n'

		# size
		if parent.tb_min_width_normal.value() > 0:
			style += f'\tmin-width: {parent.tb_min_width_normal.value()};\n'
		if parent.tb_min_height_normal.value() > 0:
			style += f'\tmin-height: {parent.tb_min_height_normal.value()};\n'
		if parent.tb_max_width_normal.value() > 0:
			style += f'\tmax-width: {parent.tb_max_width_normal.value()};\n'
		if parent.tb_max_height_normal.value() > 0:
			style += f'\tmax-height: {parent.tb_max_height_normal.value()};\n'

		# border
		border_type_normal = parent.tb_border_type_normal.currentText()
		if border_type_normal != 'none':
			style += f'\tborder-style: {border_type_normal};\n'
		if parent.tbtn_border_color_normal:
			style += f'\tborder-color: {parent.tbtn_border_color_normal};\n'
		if parent.tb_border_width_normal.value() > 0:
			style += f'\tborder-width: {parent.tb_border_width_normal.value()}px;\n'
		if parent.tb_border_radius_normal.value() > 0:
			style += f'\tborder-radius: {parent.tb_border_radius_normal.value()}px;\n'

		# font
		if parent.tb_font_family:
			style += f'\tfont-family: {parent.tb_font_family};\n'
		if parent.tb_font_size:
			style += f'\tfont-size: {parent.tb_font_size}pt;\n'
		if parent.tb_font_weight:
			style += f'\tfont-weight: {parent.tb_font_weight};\n'


		style += '\tspacing: 25px;\n'

		style += '}\n' # End of QToolButton

	parent.tb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.tb_stylesheet.appendPlainText(line)

		parent.toolBar.setStyleSheet(style)

	if parent.sender().objectName() == 'tbar_apply_style':
		return style


