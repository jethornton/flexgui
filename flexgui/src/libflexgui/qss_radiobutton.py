from functools import partial

from libflexgui import qss_utilities

def startup(parent):

	# QRadioButton
	parent.rb_normal = False

	parent.rb_apply_style.clicked.connect(partial(qss_utilities.create_stylesheet, parent, 'QRadioButton', 'radioButton', 'rb'))
	parent.rb_clear_style.clicked.connect(partial(qss_utilities.clear_stylesheet, parent, 'QRadioButton', 'radioButton', 'rb'))

	parent.rb_disable.clicked.connect(partial(parent.disable, 'radioButton_0'))

	parent.rb_min_width_normal.valueChanged.connect(parent.size)
	parent.rb_min_height_normal.valueChanged.connect(parent.size)
	parent.rb_max_width_normal.valueChanged.connect(parent.size)
	parent.rb_max_height_normal.valueChanged.connect(parent.size)

	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	pseudo_states = ['normal', 'hover', 'pressed', 'checked', 'disabled']

	for item in pseudo_states:
		# populate border combo boxes
		getattr(parent, f'rb_border_type_{item}').addItems(border_types)
		# setup variables
		setattr(parent, f'rb_{item}', False) # build section flag
		setattr(parent, f'rb_fg_color_sel_{item}', False)
		setattr(parent, f'rb_bg_color_sel_{item}', False)
		setattr(parent, f'rb_border_color_sel_{item}', False)

	for state in pseudo_states: # color dialog connections
		getattr(parent, f'rb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'rb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'rb_border_color_{state}').clicked.connect(parent.color_dialog)

	parent.rb_font_picker.clicked.connect(parent.font_dialog)
	parent.rb_font_family = False
	parent.rb_font_size = False
	parent.rb_font_weight = False
	parent.rb_font_style = False
	parent.rb_font_italic = False
	parent.rb_indicator = False

	parent.rb_padding_normal.valueChanged.connect(parent.padding)
	parent.rb_padding_left_normal.valueChanged.connect(parent.padding)
	parent.rb_padding_right_normal.valueChanged.connect(parent.padding)
	parent.rb_padding_top_normal.valueChanged.connect(parent.padding)
	parent.rb_padding_bottom_normal.valueChanged.connect(parent.padding)

	parent.rb_margin_normal.valueChanged.connect(parent.margin)
	parent.rb_margin_left_normal.valueChanged.connect(parent.margin)
	parent.rb_margin_right_normal.valueChanged.connect(parent.margin)
	parent.rb_margin_top_normal.valueChanged.connect(parent.margin)
	parent.rb_margin_bottom_normal.valueChanged.connect(parent.margin)

	parent.rb_indicator_width_normal.valueChanged.connect(parent.indicator)
	parent.rb_indicator_height_normal.valueChanged.connect(parent.indicator)

