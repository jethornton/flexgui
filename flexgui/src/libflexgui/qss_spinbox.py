from functools import partial

def startup(parent):

	# QSpinBox
	parent.sb_normal = False
	parent.sb_apply_style.clicked.connect(partial(sb_create_stylesheet, parent))
	parent.sb_disable.clicked.connect(partial(parent.disable, 'spinBox'))

	border_types = ['none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	pseudo_states = ['normal', 'hover', 'pressed', 'disabled']

	for state in pseudo_states: # color dialog connections
		getattr(parent, f'sb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'sb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'sb_border_color_{state}').clicked.connect(parent.color_dialog)

	for item in pseudo_states: # populate border combo boxes
		getattr(parent, f'sb_border_type_{item}').addItems(border_types)

	# setup enable variables
	for item in pseudo_states:
		setattr(parent, f'sb_{item}', False)
		setattr(parent, f'sb_fg_color_sel_{item}', False)
		setattr(parent, f'sb_bg_color_sel_{item}', False)
		setattr(parent, f'sb_border_color_sel_{item}', False)

	parent.sb_font_family = False
	parent.sb_font_size = False
	parent.sb_font_weight = False
	parent.sb_font_style = False
	parent.sb_font_italic = False

	parent.sb_min_width_normal.valueChanged.connect(parent.size)
	parent.sb_min_height_normal.valueChanged.connect(parent.size)
	parent.sb_max_width_normal.valueChanged.connect(parent.size)
	parent.sb_max_height_normal.valueChanged.connect(parent.size)

	parent.sb_padding_normal.valueChanged.connect(parent.padding)
	parent.sb_padding_left_normal.valueChanged.connect(parent.padding)
	parent.sb_padding_right_normal.valueChanged.connect(parent.padding)
	parent.sb_padding_top_normal.valueChanged.connect(parent.padding)
	parent.sb_padding_bottom_normal.valueChanged.connect(parent.padding)

	parent.sb_margin_normal.valueChanged.connect(parent.margin)
	parent.sb_margin_left_normal.valueChanged.connect(parent.margin)
	parent.sb_margin_right_normal.valueChanged.connect(parent.margin)
	parent.sb_margin_top_normal.valueChanged.connect(parent.margin)
	parent.sb_margin_bottom_normal.valueChanged.connect(parent.margin)

	parent.sb_font_picker.clicked.connect(parent.font_dialog)

######### QSpinBox Stylesheet #########

def sb_create_stylesheet(parent):
	style = False

	# QSpinBox normal pseudo-state
	if parent.sb_normal:
		style = 'QSpinBox {\n'

		# color
		if parent.sb_fg_color_sel_normal:
			style += f'\tcolor: {parent.sb_fg_color_sel_normal};\n'
		if parent.sb_bg_color_sel_normal:
			style += f'\tbackground-color: {parent.sb_bg_color_sel_normal};\n'

		# font
		if parent.sb_font_family:
			style += f'\tfont-family: {parent.sb_font_family};\n'
		if parent.sb_font_size:
			style += f'\tfont-size: {parent.sb_font_size}pt;\n'
		if parent.sb_font_weight:
			style += f'\tfont-weight: {parent.sb_font_weight};\n'

		# size
		if parent.sb_min_width_normal.value() > 0:
			style += f'\tmin-width: {parent.sb_min_width_normal.value()};\n'
		if parent.sb_min_height_normal.value() > 0:
			style += f'\tmin-height: {parent.sb_min_height_normal.value()};\n'
		if parent.sb_max_width_normal.value() > 0:
			style += f'\tmax-width: {parent.sb_max_width_normal.value()};\n'
		if parent.sb_max_height_normal.value() > 0:
			style += f'\tmax-height: {parent.sb_max_height_normal.value()};\n'

		# border
		border_type_normal = parent.sb_border_type_normal.currentText()
		if border_type_normal != 'none':
			style += f'\tborder-style: {border_type_normal};\n'
		if parent.sb_border_color_sel_normal:
			style += f'\tborder-color: {parent.sb_border_color_sel_normal};\n'
		if parent.sb_border_width_normal.value() > 0:
			style += f'\tborder-width: {parent.sb_border_width_normal.value()}px;\n'
		if parent.sb_border_radius_normal.value() > 0:
			style += f'\tborder-radius: {parent.sb_border_radius_normal.value()}px;\n'

		# padding
		if parent.sb_padding_normal.value() > 0:
			style += f'\tpadding: {parent.sb_padding_normal.value()};\n'
		if parent.sb_padding_left_normal.value() > 0:
			style += f'\tpadding-left: {parent.sb_padding_left_normal.value()};\n'
		if parent.sb_padding_right_normal.value() > 0:
			style += f'\tpadding-right: {parent.sb_padding_right_normal.value()};\n'
		if parent.sb_padding_top_normal.value() > 0:
			style += f'\tpadding-top: {parent.sb_padding_top_normal.value()};\n'
		if parent.sb_padding_bottom_normal.value() > 0:
			style += f'\tpadding-bottom: {parent.sb_padding_bottom_normal.value()};\n'

		# margin
		if parent.sb_margin_normal.value() > 0:
			style += f'\tmargin: {parent.sb_margin_normal.value()};\n'
		if parent.sb_margin_left_normal.value() > 0:
			style += f'\tmargin-left: {parent.sb_margin_left_normal.value()};\n'
		if parent.sb_margin_right_normal.value() > 0:
			style += f'\tmargin-right: {parent.sb_margin_right_normal.value()};\n'
		if parent.sb_margin_top_normal.value() > 0:
			style += f'\tmargin-top: {parent.sb_margin_top_normal.value()};\n'
		if parent.sb_margin_bottom_normal.value() > 0:
			style += f'\tmargin-bottom: {parent.sb_margin_bottom_normal.value()};\n'


		style += '}' # End of QSpinBox normal pseudo-state


	# QSpinBox build and apply the stylesheet
	parent.sb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.sb_stylesheet.appendPlainText(line)
		parent.spinBox.setStyleSheet(style)

