from functools import partial

def startup(parent):

	# QLabel
	parent.lb_normal = False
	parent.lb_apply_style.clicked.connect(partial(lb_create_stylesheet, parent))
	parent.lb_disable.clicked.connect(partial(parent.disable, 'label'))

	border_types = ['none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	lb_pseudo_states = ['normal', 'hover', 'disabled']

	for state in lb_pseudo_states: # color dialog connections
		getattr(parent, f'lb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'lb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'lb_border_color_{state}').clicked.connect(parent.color_dialog)

	for item in lb_pseudo_states: # populate border combo boxes
		getattr(parent, f'lb_border_type_{item}').addItems(border_types)

	# setup enable variables
	for item in lb_pseudo_states:
		setattr(parent, f'lb_{item}', False)
		setattr(parent, f'lb_fg_color_sel_{item}', False)
		setattr(parent, f'lb_bg_color_sel_{item}', False)
		setattr(parent, f'lb_border_color_sel_{item}', False)

	parent.lb_font_family = False
	parent.lb_font_size = False
	parent.lb_font_weight = False
	parent.lb_font_style = False
	parent.lb_font_italic = False

	parent.lb_min_width_normal.valueChanged.connect(parent.size)
	parent.lb_min_height_normal.valueChanged.connect(parent.size)
	parent.lb_max_width_normal.valueChanged.connect(parent.size)
	parent.lb_max_height_normal.valueChanged.connect(parent.size)

	parent.lb_padding_normal.valueChanged.connect(parent.padding)
	parent.lb_padding_left_normal.valueChanged.connect(parent.padding)
	parent.lb_padding_right_normal.valueChanged.connect(parent.padding)
	parent.lb_padding_top_normal.valueChanged.connect(parent.padding)
	parent.lb_padding_bottom_normal.valueChanged.connect(parent.padding)

	parent.lb_margin_normal.valueChanged.connect(parent.margin)
	parent.lb_margin_left_normal.valueChanged.connect(parent.margin)
	parent.lb_margin_right_normal.valueChanged.connect(parent.margin)
	parent.lb_margin_top_normal.valueChanged.connect(parent.margin)
	parent.lb_margin_bottom_normal.valueChanged.connect(parent.margin)

	parent.lb_font_picker.clicked.connect(parent.font_dialog)

######### QLabel Stylesheet #########

def lb_create_stylesheet(parent):
	style = False

	# QLabel normal pseudo-state
	if parent.lb_normal:
		style = 'QLabel {'

		# color
		if parent.lb_fg_color_sel_normal:
			style += f'\n\tcolor: {parent.lb_fg_color_sel_normal};'
		if parent.lb_bg_color_sel_normal:
			style += f'\n\tbackground-color: {parent.lb_bg_color_sel_normal};'

		# font
		if parent.lb_font_family:
			style += f'\n\tfont-family: {parent.lb_font_family};'
		if parent.lb_font_size:
			style += f'\n\tfont-size: {parent.lb_font_size}pt;'
		if parent.lb_font_weight:
			style += f'\n\tfont-weight: {parent.lb_font_weight};'


		# size
		if parent.lb_min_width_normal.value() > 0:
			style += f'\n\tmin-width: {parent.lb_min_width_normal.value()};'
		if parent.lb_min_height_normal.value() > 0:
			style += f'\n\tmin-height: {parent.lb_min_height_normal.value()};'
		if parent.lb_max_width_normal.value() > 0:
			style += f'\n\tmax-width: {parent.lb_max_width_normal.value()};'
		if parent.lb_max_height_normal.value() > 0:
			style += f'\n\tmax-height: {parent.lb_max_height_normal.value()};'

		# border
		border_type_normal = parent.lb_border_type_normal.currentText()
		if border_type_normal != 'none':
			style += f'\n\tborder-style: {border_type_normal};'
		if parent.lb_border_color_sel_normal:
			style += f'\n\tborder-color: {parent.lb_border_color_sel_normal};'
		if parent.lb_border_width_normal.value() > 0:
			style += f'\n\tborder-width: {parent.lb_border_width_normal.value()}px;'
		if parent.lb_border_radius_normal.value() > 0:
			style += f'\n\tborder-radius: {parent.lb_border_radius_normal.value()}px;'

		# padding
		if parent.lb_padding_normal.value() > 0:
			style += f'\n\tpadding: {parent.lb_padding_normal.value()};'
		if parent.lb_padding_left_normal.value() > 0:
			style += f'\n\tpadding-left: {parent.lb_padding_left_normal.value()};'
		if parent.lb_padding_right_normal.value() > 0:
			style += f'\n\tpadding-right: {parent.lb_padding_right_normal.value()};'
		if parent.lb_padding_top_normal.value() > 0:
			style += f'\n\tpadding-top: {parent.lb_padding_top_normal.value()};'
		if parent.lb_padding_bottom_normal.value() > 0:
			style += f'\n\tpadding-bottom: {parent.lb_padding_bottom_normal.value()};'

		# margin
		if parent.lb_margin_normal.value() > 0:
			style += f'\n\tmargin: {parent.lb_margin_normal.value()};'
		if parent.lb_margin_left_normal.value() > 0:
			style += f'\n\tmargin-left: {parent.lb_margin_left_normal.value()};'
		if parent.lb_margin_right_normal.value() > 0:
			style += f'\n\tmargin-right: {parent.lb_margin_right_normal.value()};'
		if parent.lb_margin_top_normal.value() > 0:
			style += f'\n\tmargin-top: {parent.lb_margin_top_normal.value()};'
		if parent.lb_margin_bottom_normal.value() > 0:
			style += f'\n\tmargin-bottom: {parent.lb_margin_bottom_normal.value()};'

		style += '\n}' # End of QLabel normal pseudo-state

	# QLabel hover pseudo-state
	if parent.lb_hover:

		if style: # style is not False
			style += '\n\nQLabel:hover {'
		else:
			style = '\n\nQLabel:hover {'

		# color
		if parent.lb_fg_color_sel_hover:
			style += f'\n\tcolor: {parent.lb_fg_color_sel_hover};'
		if parent.lb_bg_color_sel_hover:
			style += f'\n\tbackground-color: {parent.lb_bg_color_sel_hover};'

		# border
		border_type_hover = parent.lb_border_type_hover.currentText()
		if border_type_hover != 'none':
			style += f'\n\tborder-style: {border_type_hover};'
		if parent.lb_border_color_sel_hover:
			style += f'\n\tborder-color: {parent.lb_border_color_sel_hover};'
		if parent.lb_border_width_hover.value() > 0:
			style += f'\n\tborder-width: {parent.lb_border_width_hover.value()}px;'
		if parent.lb_border_radius_hover.value() > 0:
			style += f'\n\tborder-radius: {parent.lb_border_radius_hover.value()}px;'

		style += '\n}' # End of QLabel hover pseudo-state

	# QLabel disabled pseudo-state
	if parent.lb_disabled:

		# color
		if style: # style is not False
			style += '\n\nQLabel:disabled {'
		else:
			style = '\n\nQLabel:disabled {'

		if parent.lb_fg_color_sel_disabled:
			style += f'\n\tcolor: {parent.lb_fg_color_sel_disabled};'
		if parent.lb_bg_color_sel_disabled:
			style += f'\n\tbackground-color: {parent.lb_bg_color_sel_disabled};'

		# border
		border_type_disabled = parent.lb_border_type_disabled.currentText()
		if border_type_disabled != 'none':
			style += f'\n\tborder-style: {border_type_disabled};'
		if parent.lb_border_color_sel_disabled:
			style += f'\n\tborder-color: {parent.lb_border_color_sel_disabled};'
		if parent.lb_border_width_disabled.value() > 0:
			style += f'\n\tborder-width: {parent.lb_border_width_disabled.value()}px;'
		if parent.lb_border_radius_disabled.value() > 0:
			style += f'\n\tborder-radius: {parent.lb_border_radius_disabled.value()}px;'

		style += '\n}' # End of QLabel disabled pseudo-state

	# QLabel build and apply the stylesheet
	parent.lb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.lb_stylesheet.appendPlainText(line)
		parent.label.setStyleSheet(style)

