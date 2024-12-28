from functools import partial



def startup(parent):

	parent.tbar_normal = False

	tb_style = 'QToolBar {\n'
	tb_style += 'background: rgb(85, 170, 125);\n'
	tb_style += 'spacing: 30px;\n'
	tb_style += 'border-style: solid;\n'
	tb_style += 'border-color: #000000;\n'
	tb_style += 'border-width: 4px;\n'
	tb_style += 'border-radius: 10px;\n'
	tb_style += 'padding: 5px;\n'
	tb_style += '}\n'

	'''
	tb_style += 'QToolButton {\n'
	tb_style += 'border: 2px solid #8f8f91;\n'
	tb_style += 'border-radius: 6px;\n'
	tb_style += 'background-color: #c0c0c0;\n'
	tb_style += '}\n'
	tb_style += 'QToolButton:hover {\n'
	tb_style += 'border: 2px solid purple;\n'
	tb_style += 'border-radius: 6px;\n'
	tb_style += 'background-color: green\n'
	tb_style += '}'
	tb_style += 'QToolButton:pressed {\n'
	tb_style += 'border: 2px solid #8f8f91;\n'
	tb_style += 'border-radius: 6px;\n'
	tb_style += 'background-color: yellow\n'
	tb_style += '}'
	tb_style += 'QToolButton:checked {\n'
	tb_style += 'color: 2px solid yellow;\n'
	tb_style += 'border: 2px solid red;\n'
	tb_style += 'border-radius: 6px;\n'
	tb_style += 'background-color: green\n'
	tb_style += '}'
	'''
	'''

  background-color:
	 /* all types of tool button */
			border: 2px solid #8f8f91;
			border-radius: 6px;
			background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
			                                  stop: 0 #f6f7fa, stop: 1 #dadbde);
	}
	tb_style += 'QToolButton {\n'
	tb_style += 'background-color: #e0e0e0;\n'
	tb_style += 'border: 1px solid #c0c0c0;\n'
	tb_style += 'padding: 5px;\n'
	tb_style += 'margin: 2px;\n'
	tb_style += 'QToolButton:hover {\n'
	tb_style += 'background-color: #d0d0d0;\n'
	tb_style += '}\n'
	tb_style += 'QToolButton:pressed {\n'
	tb_style += 'background-color: #c0c0c0;\n'
	tb_style += '}'
	'''
	#parent.toolBar.setStyleSheet('''
	#QToolBar {
	#background: red;
	#spacing: 3px;
	#}
	#''')
	parent.toolBar.setStyleSheet(tb_style)
	#parent.toolBar.setStyleSheet(textwrap.dedent(tb_style))

	'''
	def hex_to_rgb(hex_color):
			"""Converts a hex color code to RGB."""

			hex_color = hex_color.lstrip('#')
			return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

	hex_color = "#e0e0e0"
	rgb_color = hex_to_rgb(hex_color)

	print(rgb_color)  # Output: (224, 224, 224)
	'''


	# QToolBar
	parent.tbar_bg_color_normal.clicked.connect(parent.color_dialog)
	parent.toolbar_spacing.valueChanged.connect(partial(spacing, parent))
	parent.tbar_border_color_normal.clicked.connect(parent.color_dialog)
	parent.tbar_apply_style.clicked.connect(partial(tbar_create_stylesheet, parent))
	# variables to build sections in the stylesheet
	parent.build_toolbar = False

	parent.toolbar_bg_color = False
	parent.toolbar_border_color = False

	border_types = ['none', 'solid', 'dashed', 'dotted', 'double', 'groove',
		'ridge', 'inset', 'outset']
	parent.tbar_border_type.addItems(border_types)

	parent.tbar_padding_normal.valueChanged.connect(parent.padding)
	parent.tbar_padding_left_normal.valueChanged.connect(parent.padding)
	parent.tbar_padding_right_normal.valueChanged.connect(parent.padding)
	parent.tbar_padding_top_normal.valueChanged.connect(parent.padding)
	parent.tbar_padding_bottom_normal.valueChanged.connect(parent.padding)

	parent.tbar_margin_normal.valueChanged.connect(parent.margin)
	parent.tbar_margin_left_normal.valueChanged.connect(parent.margin)
	parent.tbar_margin_right_normal.valueChanged.connect(parent.margin)
	parent.tbar_margin_top_normal.valueChanged.connect(parent.margin)
	parent.tbar_margin_bottom_normal.valueChanged.connect(parent.margin)


######### QToolBar Stylesheet #########

def tbar_create_stylesheet(parent):
	style = False

	# QToolBar
	if parent.tbar_normal:
		style = 'QToolBar {\n'

		# background color and spacing
		if parent.toolbar_bg_color:
			style += f'\tbackground: {parent.toolbar_bg_color};\n'
		if parent.toolbar_spacing.value() > 0:
			style += f'\tspacing: {parent.toolbar_spacing.value()}px;\n'

		# border
		border_type = parent.tbar_border_type.currentText()
		if border_type != 'none':
			style += f'\tborder-style: {border_type};\n'
			if parent.tbar_border_color_normal:
				style += f'\tborder-color: {parent.toolbar_border_color};\n'
			if parent.tbar_border_width.value() > 0:
				style += f'\tborder-width: {parent.tbar_border_width.value()}px;\n'
			if parent.tbar_border_radius.value() > 0:
				style += f'\tborder-radius: {parent.tbar_border_radius.value()}px;\n'

		# padding
		if parent.tbar_padding_normal.value() > 0:
			style += f'\tpadding: {parent.tbar_padding_normal.value()};\n'
		if parent.tbar_padding_left_normal.value() > 0:
			style += f'\tpadding-left: {parent.tbar_padding_left_normal.value()};\n'
		if parent.tbar_padding_right_normal.value() > 0:
			style += f'\tpadding-right: {parent.tbar_padding_right_normal.value()};\n'
		if parent.tbar_padding_top_normal.value() > 0:
			style += f'\tpadding-top: {parent.tbar_padding_top_normal.value()};\n'
		if parent.tbar_padding_bottom_normal.value() > 0:
			style += f'\tpadding-bottom: {parent.tbar_padding_bottom_normal.value()};\n'

		# margin
		if parent.tbar_margin_normal.value() > 0:
			style += f'\tmargin: {parent.tbar_margin_normal.value()};\n'
		if parent.tbar_margin_left_normal.value() > 0:
			style += f'\tmargin-left: {parent.tbar_margin_left_normal.value()};\n'
		if parent.tbar_margin_right_normal.value() > 0:
			style += f'\tmargin-right: {parent.tbar_margin_right_normal.value()};\n'
		if parent.tbar_margin_top_normal.value() > 0:
			style += f'\tmargin-top: {parent.tbar_margin_top_normal.value()};\n'
		if parent.tbar_margin_bottom_normal.value() > 0:
			style += f'\tmargin-bottom: {parent.tbar_margin_bottom_normal.value()};\n'


		style += '}\n' # End of QToolBar

	parent.tbar_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.tbar_stylesheet.appendPlainText(line)

		parent.toolBar.setStyleSheet(style)

def spacing(parent):
	obj = parent.sender().objectName().split('_')[0]
	if parent.sender().value() > 0:
		parent.tbar_normal = True





