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
		# setup variables
		setattr(parent, f'lb_{state}', False)
		setattr(parent, f'lb_fg_color_sel_{state}', False)
		setattr(parent, f'lb_bg_color_sel_{state}', False)
		setattr(parent, f'lb_border_color_sel_{state}', False)
		# populate border states
		getattr(parent, f'lb_border_type_{state}').blockSignals(True)
		getattr(parent, f'lb_border_type_{state}').addItems(border_types)
		getattr(parent, f'lb_border_type_{state}').blockSignals(False)
		# connect border states
		getattr(parent, f'lb_border_type_{state}').currentIndexChanged.connect(parent.border)
		# connect color states
		getattr(parent, f'lb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'lb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'lb_border_color_{state}').clicked.connect(parent.color_dialog)

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

