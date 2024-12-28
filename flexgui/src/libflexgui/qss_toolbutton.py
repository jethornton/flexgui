from functools import partial

from libflexgui import qss_toolbar

def startup(parent):

	# QToolButton
	parent.tb_normal = False
	parent.tb_apply_style.clicked.connect(partial(tb_create_stylesheet, parent))

	parent.tb_fg_color_normal.clicked.connect(parent.color_dialog)
	parent.tb_bg_color_normal.clicked.connect(parent.color_dialog)


	parent.tbtn_fg_color_normal = False
	parent.tbtn_bg_color_normal = False


######### QToolButton Stylesheet #########

def tb_create_stylesheet(parent):
	style = False

	# check for toolbar style set
	if parent.sender().objectName() == 'tb_apply_style':
		if parent.tbar_normal:
			style = qss_toolbar.tbar_create_stylesheet(parent)

	# QToolButton normal pseudo-state
	if parent.tb_normal:

		if style: # style is not False
			style += 'QToolBar QToolButton {\n'
		else:
			style = 'QToolBar QToolButton {\n'

		# color 
		if parent.tbtn_fg_color_normal:
			style += f'\tcolor: {parent.tbtn_fg_color_normal};\n'
		if parent.tbtn_bg_color_normal:
			style += f'\tbackground-color: {parent.tbtn_bg_color_normal};\n'

		style += '\tspacing: 25px;\n'

		style += '}\n' # End of QToolButton

	parent.tb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.tb_stylesheet.appendPlainText(line)

		parent.toolBar.setStyleSheet(style)

	if parent.sender().objectName() == 'tbar_apply_style':
		return style


