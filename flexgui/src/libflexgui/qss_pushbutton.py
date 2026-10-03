from functools import partial

from libflexgui import qss_utilities

def startup(parent):

	# QPushButton
	parent.pb_normal = False

	parent.pb_apply_style.clicked.connect(partial(qss_utilities.create_stylesheet, parent, 'QPushButton', 'pushButton', 'pb'))
	parent.pb_clear_style.clicked.connect(partial(qss_utilities.clear_stylesheet, parent, 'QPushButton', 'pushButton', 'pb'))

	parent.pb_set_checkable.released.connect(parent.set_checkable)
	parent.pb_disable.clicked.connect(partial(parent.disable, 'pushButton'))

	parent.pb_min_width_normal.valueChanged.connect(parent.size)
	parent.pb_min_height_normal.valueChanged.connect(parent.size)
	parent.pb_max_width_normal.valueChanged.connect(parent.size)
	parent.pb_max_height_normal.valueChanged.connect(parent.size)

	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	pseudo_states = ['normal', 'hover', 'pressed', 'checked', 'disabled']

	for item in pseudo_states:
		# populate border combo boxes
		getattr(parent, f'pb_border_type_{item}').addItems(border_types)
		# setup variables
		setattr(parent, f'pb_{item}', False) # build section flag
		setattr(parent, f'pb_fg_color_sel_{item}', False)
		setattr(parent, f'pb_bg_color_sel_{item}', False)
		setattr(parent, f'pb_border_color_sel_{item}', False)

	for state in pseudo_states: # color dialog connections
		getattr(parent, f'pb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'pb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'pb_border_color_{state}').clicked.connect(parent.color_dialog)

	parent.pb_font_picker.clicked.connect(parent.font_dialog)
	parent.pb_font_family = False
	parent.pb_font_size = False
	parent.pb_font_weight = False
	parent.pb_font_style = False
	parent.pb_font_italic = False

	parent.pb_padding_normal.valueChanged.connect(parent.padding)
	parent.pb_padding_left_normal.valueChanged.connect(parent.padding)
	parent.pb_padding_right_normal.valueChanged.connect(parent.padding)
	parent.pb_padding_top_normal.valueChanged.connect(parent.padding)
	parent.pb_padding_bottom_normal.valueChanged.connect(parent.padding)

	parent.pb_margin_normal.valueChanged.connect(parent.margin)
	parent.pb_margin_left_normal.valueChanged.connect(parent.margin)
	parent.pb_margin_right_normal.valueChanged.connect(parent.margin)
	parent.pb_margin_top_normal.valueChanged.connect(parent.margin)
	parent.pb_margin_bottom_normal.valueChanged.connect(parent.margin)


