from functools import partial

from libflexgui import qss_utilities

def startup(parent):

	# QSpinBox
	parent.sb_normal = False

	parent.sb_apply_style.clicked.connect(partial(qss_utilities.create_stylesheet, parent, 'QSpinBox', 'spinBox', 'sb'))
	parent.sb_clear_style.clicked.connect(partial(qss_utilities.clear_stylesheet, parent, 'QSpinBox', 'spinBox', 'sb'))

	parent.sb_disable.clicked.connect(partial(parent.disable, 'spinBox'))

	border_types = ['Select', 'none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	pseudo_states = ['normal', 'hover', 'pressed', 'disabled']

	for state in pseudo_states: # color dialog connections
		getattr(parent, f'sb_fg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'sb_bg_color_{state}').clicked.connect(parent.color_dialog)
		getattr(parent, f'sb_border_color_{state}').clicked.connect(parent.color_dialog)

	for item in pseudo_states: # populate border combo boxes
		getattr(parent, f'sb_border_type_{item}').addItems(border_types)

	origins = ['none', 'content', 'padding', 'border', 'margin']
	parent.sb_up_origin.addItems(origins)
	parent.sb_down_origin.addItems(origins)

	positions = ['none', 'right', 'left', 'top', 'bottom', 'top left',
	'top right', 'bottom left', 'bottom right']
	parent.sb_up_position.addItems(positions)
	parent.sb_down_position.addItems(positions)

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
	parent.sb_up = False
	parent.sb_down = False

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

	parent.sb_up_origin.currentIndexChanged.connect(partial(sub_controls, parent))
	parent.sb_up_position.currentIndexChanged.connect(partial(sub_controls, parent))
	parent.sb_up_hide.toggled.connect(partial(sub_controls, parent))
	parent.sb_up_padding.valueChanged.connect(partial(sub_controls, parent))

	parent.sb_down_origin.currentIndexChanged.connect(partial(sub_controls, parent))
	parent.sb_down_position.currentIndexChanged.connect(partial(sub_controls, parent))
	parent.sb_down_hide.toggled.connect(partial(sub_controls, parent))

