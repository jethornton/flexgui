from functools import partial

from libflexgui import qss_utilities

def startup(parent):

	# QLabel
	parent.lb_normal = False

	parent.lb_apply_style.clicked.connect(partial(qss_utilities.create_stylesheet, parent, 'QLabel', 'label', 'lb'))
	parent.lb_clear_style.clicked.connect(partial(qss_utilities.clear_stylesheet, parent, 'QLabel', 'label', 'lb'))

	parent.lb_disable.clicked.connect(partial(parent.disable, 'label'))

	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	pseudo_states = ['normal', 'hover', 'disabled']

	for state in pseudo_states: # color dialog connections
		getattr(parent, f'lb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'lb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'lb_border_color_{state}').clicked.connect(parent.color_dialog)

	for item in pseudo_states: # populate border combo boxes
		getattr(parent, f'lb_border_type_{item}').addItems(border_types)

	# setup enable variables
	for item in pseudo_states:
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

