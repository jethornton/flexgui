from functools import partial


def startup(parent):

	# QLineEdit
	parent.le_normal = False

	parent.le_apply_style.clicked.connect(partial(create_stylesheet, parent))
	parent.le_clear_style.clicked.connect(partial(clear_stylesheet, parent))

	#parent.le_read_only.clicked.connect(partial(parent.disable, 'lineEdit')) FIXME
	border_types = ['none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	pseudo_states = ['normal', 'hover', 'disabled']

	for state in pseudo_states: # color dialog connections
		getattr(parent, f'le_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'le_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'le_border_color_{state}').clicked.connect(parent.color_dialog)

	for item in pseudo_states: # populate border combo boxes
		getattr(parent, f'le_border_type_{item}').addItems(border_types)

	# setup enable variables
	for item in pseudo_states:
		setattr(parent, f'le_{item}', False)
		setattr(parent, f'le_fg_color_sel_{item}', False)
		setattr(parent, f'le_bg_color_sel_{item}', False)
		setattr(parent, f'le_border_color_sel_{item}', False)

	parent.le_font_family = False
	parent.le_font_size = False
	parent.le_font_weight = False
	parent.le_font_style = False
	parent.le_font_italic = False
	'''

	parent.le_min_width_normal.valueChanged.connect(parent.size)
	parent.le_min_height_normal.valueChanged.connect(parent.size)
	parent.le_max_width_normal.valueChanged.connect(parent.size)
	parent.le_max_height_normal.valueChanged.connect(parent.size)

	parent.le_padding_normal.valueChanged.connect(parent.padding)
	parent.le_padding_left_normal.valueChanged.connect(parent.padding)
	parent.le_padding_right_normal.valueChanged.connect(parent.padding)
	parent.le_padding_top_normal.valueChanged.connect(parent.padding)
	parent.le_padding_bottom_normal.valueChanged.connect(parent.padding)

	parent.le_margin_normal.valueChanged.connect(parent.margin)
	parent.le_margin_left_normal.valueChanged.connect(parent.margin)
	parent.le_margin_right_normal.valueChanged.connect(parent.margin)
	parent.le_margin_top_normal.valueChanged.connect(parent.margin)
	parent.le_margin_bottom_normal.valueChanged.connect(parent.margin)

	parent.le_font_picker.clicked.connect(parent.font_dialog)
	'''
######### QLineEdit Stylesheet #########

def create_stylesheet(parent):
	style = False

	# QLineEdit normal pseudo-state
	if parent.le_normal:
		style = 'QLineEdit {\n'

		# color
		if parent.le_fg_color_sel_normal:
			style += f'\tcolor: {parent.le_fg_color_sel_normal};\n'
		if parent.le_bg_color_sel_normal:
			style += f'\tbackground-color: {parent.le_bg_color_sel_normal};\n'

		# font
		if parent.le_font_family:
			style += f'\tfont-family: {parent.le_font_family};\n'
		if parent.le_font_size:
			style += f'\tfont-size: {parent.le_font_size}pt;\n'
		if parent.le_font_weight:
			style += f'\tfont-weight: {parent.le_font_weight};\n'

		# size
		if parent.le_min_width_normal.value() > 0:
			style += f'\tmin-width: {parent.le_min_width_normal.value()}px;\n'
		if parent.le_min_height_normal.value() > 0:
			style += f'\tmin-height: {parent.le_min_height_normal.value()}px;\n'
		if parent.le_max_width_normal.value() > 0:
			style += f'\tmax-width: {parent.le_max_width_normal.value()}px;\n'
		if parent.le_max_height_normal.value() > 0:
			style += f'\tmax-height: {parent.le_max_height_normal.value()}px;\n'

		# border
		border_type_normal = parent.le_border_type_normal.currentText()
		if border_type_normal != 'none':
			style += f'\tborder-style: {border_type_normal};\n'
		if parent.le_border_color_sel_normal:
			style += f'\tborder-color: {parent.le_border_color_sel_normal};\n'
		if parent.le_border_width_normal.value() > 0:
			style += f'\tborder-width: {parent.le_border_width_normal.value()}px;\n'
		if parent.le_border_radius_normal.value() > 0:
			style += f'\tborder-radius: {parent.le_border_radius_normal.value()}px;\n'

		# padding
		if parent.le_padding_normal.value() > 0:
			style += f'\tpadding: {parent.le_padding_normal.value()};\n'
		if parent.le_padding_left_normal.value() > 0:
			style += f'\tpadding-left: {parent.le_padding_left_normal.value()};\n'
		if parent.le_padding_right_normal.value() > 0:
			style += f'\tpadding-right: {parent.le_padding_right_normal.value()};\n'
		if parent.le_padding_top_normal.value() > 0:
			style += f'\tpadding-top: {parent.le_padding_top_normal.value()};\n'
		if parent.le_padding_bottom_normal.value() > 0:
			style += f'\tpadding-bottom: {parent.le_padding_bottom_normal.value()};\n'

		# margin
		if parent.le_margin_normal.value() > 0:
			style += f'\tmargin: {parent.le_margin_normal.value()};\n'
		if parent.le_margin_left_normal.value() > 0:
			style += f'\tmargin-left: {parent.le_margin_left_normal.value()};\n'
		if parent.le_margin_right_normal.value() > 0:
			style += f'\tmargin-right: {parent.le_margin_right_normal.value()};\n'
		if parent.le_margin_top_normal.value() > 0:
			style += f'\tmargin-top: {parent.le_margin_top_normal.value()};\n'
		if parent.le_margin_bottom_normal.value() > 0:
			style += f'\tmargin-bottom: {parent.le_margin_bottom_normal.value()};\n'

		style += '}' # End of QLineEdit normal pseudo-state

	# QLineEdit hover pseudo-state
	if parent.le_hover:
		if style: # style is not False
			style += '\n\nQLineEdit:hover {\n'
		else:
			style = '\n\nQLineEdit:hover {\n'

		# color
		if parent.le_fg_color_sel_hover:
			style += f'\tcolor: {parent.le_fg_color_sel_hover};\n'
		if parent.le_bg_color_sel_hover:
			style += f'\tbackground-color: {parent.le_bg_color_sel_hover};\n'

		# border
		border_type_hover = parent.le_border_type_hover.currentText()
		if border_type_hover != 'none':
			style += f'\tborder-style: {border_type_hover};\n'
		if parent.le_border_color_sel_hover:
			style += f'\tborder-color: {parent.le_border_color_sel_hover};\n'
		if parent.le_border_width_hover.value() > 0:
			style += f'\tborder-width: {parent.le_border_width_hover.value()}px;\n'
		if parent.le_border_radius_hover.value() > 0:
			style += f'\tborder-radius: {parent.le_border_radius_hover.value()}px;\n'

		style += '}' # End of QLineEdit hover pseudo-state

	# QLineEdit disabled pseudo-state
	if parent.le_disabled:

		# color
		if style: # style is not False
			style += '\n\nQLineEdit:disabled {\n'
		else:
			style = '\n\nQLineEdit:disabled {\n'

		if parent.le_fg_color_sel_disabled:
			style += f'\tcolor: {parent.le_fg_color_sel_disabled};\n'
		if parent.le_bg_color_sel_disabled:
			style += f'\tbackground-color: {parent.le_bg_color_sel_disabled};\n'

		# border
		border_type_disabled = parent.le_border_type_disabled.currentText()
		if border_type_disabled != 'none':
			style += f'\tborder-style: {border_type_disabled};\n'
		if parent.le_border_color_sel_disabled:
			style += f'\tborder-color: {parent.le_border_color_sel_disabled};\n'
		if parent.le_border_width_disabled.value() > 0:
			style += f'\tborder-width: {parent.le_border_width_disabled.value()}px;\n'
		if parent.le_border_radius_disabled.value() > 0:
			style += f'\tborder-radius: {parent.le_border_radius_disabled.value()}px;\n'

		style += '}' # End of QLineEdit disabled pseudo-state

	# QLineEdit build and apply the stylesheet
	parent.le_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.le_stylesheet.appendPlainText(line)
		parent.lineEdit.setStyleSheet(style)

def clear_stylesheet(parent):
	parent.le_normal = False

	pseudo_states = ['normal', 'hover', 'disabled']

	# set all the variables to False
	for item in pseudo_states:
		setattr(parent, f'le_{item}', False) # build section flag
		setattr(parent, f'le_fg_color_sel_{item}', False)
		setattr(parent, f'le_bg_color_sel_{item}', False)
		setattr(parent, f'le_border_color_sel_{item}', False)

	# clear all the colors
	for item in pseudo_states:
		label = getattr(parent, f'le_fg_color_{item}').property('label')
		getattr(parent, label).setStyleSheet('background-color: none;')
		label = getattr(parent, f'le_bg_color_{item}').property('label')
		getattr(parent, label).setStyleSheet('background-color: none;')
		label = getattr(parent, f'le_border_color_{item}').property('label')
		getattr(parent, label).setStyleSheet('background-color: none;')

	# set border to none and 0
	for item in pseudo_states:
		getattr(parent, f'le_border_type_{item}').setCurrentIndex(0)
		getattr(parent, f'le_border_width_{item}').setValue(0)
		getattr(parent, f'le_border_radius_{item}').setValue(0)

	# clear the font variables
	parent.le_font_family = False
	parent.le_font_size = False
	parent.le_font_weight = False
	parent.le_font_style = False
	parent.le_font_italic = False

	parent.le_min_width_normal.setValue(0)
	parent.le_min_height_normal.setValue(0)
	parent.le_max_width_normal.setValue(0)
	parent.le_max_height_normal.setValue(0)
	parent.le_padding_normal.setValue(0)
	parent.le_padding_left_normal.setValue(0)
	parent.le_padding_right_normal.setValue(0)
	parent.le_padding_top_normal.setValue(0)
	parent.le_padding_top_normal.setValue(0)
	parent.le_margin_normal.setValue(0)
	parent.le_margin_left_normal.setValue(0)
	parent.le_margin_right_normal.setValue(0)
	parent.le_margin_top_normal.setValue(0)
	parent.le_margin_top_normal.setValue(0)

	parent.le_stylesheet.clear()
	parent.lineEdit.setStyleSheet('')


