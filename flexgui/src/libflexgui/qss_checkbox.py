from functools import partial

from libflexgui import qss_utilities

def startup(parent):

	# QCheckBox
	parent.cb_normal = False

	#parent.cb_apply_style.clicked.connect(partial(create_stylesheet, parent))

	parent.cb_apply_style.clicked.connect(partial(qss_utilities.create_stylesheet, parent, 'QCheckBox', 'checkBox', 'cb'))
	parent.cb_clear_style.clicked.connect(partial(qss_utilities.clear_stylesheet, parent, 'QCheckBox', 'checkBox', 'cb'))

	parent.cb_disable.clicked.connect(partial(parent.disable, 'checkBox'))

	parent.cb_min_width_normal.valueChanged.connect(parent.size)
	parent.cb_min_height_normal.valueChanged.connect(parent.size)
	parent.cb_max_width_normal.valueChanged.connect(parent.size)
	parent.cb_max_height_normal.valueChanged.connect(parent.size)

	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	pseudo_states = ['normal', 'hover', 'pressed', 'checked', 'disabled']

	for item in pseudo_states:
		# setup variables
		setattr(parent, f'cb_{item}', False) # build section flag
		setattr(parent, f'cb_fg_color_sel_{item}', False)
		setattr(parent, f'cb_bg_color_sel_{item}', False)
		setattr(parent, f'cb_border_color_sel_{item}', False)
		# populate border combo boxes
		getattr(parent, f'cb_border_type_{item}').addItems(border_types)
		# connect border items
		getattr(parent, f'cb_border_type_{item}').currentIndexChanged.connect(parent.border)

	for state in pseudo_states: # color dialog connections
		getattr(parent, f'cb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'cb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'cb_border_color_{state}').clicked.connect(parent.color_dialog)
	parent.cb_indicator_bg_color_normal.clicked.connect(parent.color_dialog)
	parent.cb_indicator_bg_color = False

	parent.cb_font_picker.clicked.connect(parent.font_dialog)
	parent.cb_font_family = False
	parent.cb_font_size = False
	parent.cb_font_weight = False
	parent.cb_font_style = False
	parent.cb_font_italic = False
	parent.cb_indicator = False
	parent.cb_indicator_normal = False
	parent.cb_indicator_checked = False
	parent.cb_indicator_unchecked = False

	parent.cb_padding_normal.valueChanged.connect(parent.padding)
	parent.cb_padding_left_normal.valueChanged.connect(parent.padding)
	parent.cb_padding_right_normal.valueChanged.connect(parent.padding)
	parent.cb_padding_top_normal.valueChanged.connect(parent.padding)
	parent.cb_padding_bottom_normal.valueChanged.connect(parent.padding)

	parent.cb_margin_normal.valueChanged.connect(parent.margin)
	parent.cb_margin_left_normal.valueChanged.connect(parent.margin)
	parent.cb_margin_right_normal.valueChanged.connect(parent.margin)
	parent.cb_margin_top_normal.valueChanged.connect(parent.margin)
	parent.cb_margin_bottom_normal.valueChanged.connect(parent.margin)

	parent.cb_indicator_width_normal.valueChanged.connect(parent.indicator)
	parent.cb_indicator_height_normal.valueChanged.connect(parent.indicator)

	parent.cb_indicator_icon_checked.editingFinished.connect(parent.indicator)
	parent.cb_indicator_icon_unchecked.editingFinished.connect(parent.indicator)


