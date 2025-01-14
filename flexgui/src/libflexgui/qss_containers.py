from functools import partial

from PyQt6.QtWidgets import QVBoxLayout, QMenuBar, QStatusBar

def startup(parent):

######### QMainWindow Setup #########
	parent.mw_normal = False

	parent.mw_fg_color_normal.clicked.connect(parent.color_dialog)
	parent.mw_bg_color_normal.clicked.connect(parent.color_dialog)

	parent.mw_fg_color_sel = False
	parent.mw_bg_color_sel = False

	parent.mw_apply_style.clicked.connect(partial(create_mw_stylesheet, parent))
	parent.mw_clear_style.clicked.connect(partial(clear_mw_stylesheet, parent))

######### QFrame Setup #########
	parent.fr_normal = False

	parent.fr_fg_color_normal.clicked.connect(parent.color_dialog)
	parent.fr_bg_color_normal.clicked.connect(parent.color_dialog)

	parent.fr_fg_color_sel = False
	parent.fr_bg_color_sel = False

	parent.fr_apply_style.clicked.connect(partial(create_fr_stylesheet, parent))
	parent.fr_clear_style.clicked.connect(partial(clear_fr_stylesheet, parent))

######### QGroupBox Setup #########
	parent.gb_normal = False

	parent.gb_fg_color_normal.clicked.connect(parent.color_dialog)
	parent.gb_bg_color_normal.clicked.connect(parent.color_dialog)

	parent.gb_fg_color_sel = False
	parent.gb_bg_color_sel = False

	parent.gb_apply_style.clicked.connect(partial(create_gb_stylesheet, parent))
	parent.gb_clear_style.clicked.connect(partial(clear_gb_stylesheet, parent))


######### QMainWindow Stylesheet #########

def create_mw_stylesheet(parent):
	style = False
	style_print = 'QMainWindow'
	style_apply = 'QFrame'

	# QMainWindow normal pseudo-state
	if parent.mw_normal:
		style = 'replace_here {\n'

		# color
		if parent.mw_fg_color_sel:
			style += f'\tcolor: {parent.mw_fg_color_sel};\n'
		if parent.mw_bg_color_sel:
			style += f'\tbackground-color: {parent.mw_bg_color_sel};\n'

		style += '}' # End of QMainWindow normal pseudo-state

	# QMainWindow build and apply the stylesheet
	parent.mw_stylesheet.clear()
	if style:
		stylesheet = style.replace('replace_here', style_print)
		lines = stylesheet.splitlines()
		for line in lines:
			parent.mw_stylesheet.appendPlainText(line)

		parent.mw_frame.setStyleSheet(style.replace('replace_here', style_apply))

def clear_mw_stylesheet(parent):
	parent.mw_normal = False
	parent.mw_fg_color_sel = False
	parent.mw_bg_color_sel = False
	parent.mw_fg_color_lb.setStyleSheet('')
	parent.mw_bg_color_lb.setStyleSheet('')
	parent.mw_frame.setStyleSheet('')
	parent.mw_stylesheet.clear()

######### QFrame Stylesheet #########

def create_fr_stylesheet(parent):
	style = False

	# QMainWindow normal pseudo-state
	if parent.fr_normal:
		style = 'QFrame {\n'

		# color
		if parent.fr_fg_color_sel:
			style += f'\tcolor: {parent.fr_fg_color_sel};\n'
		if parent.fr_bg_color_sel:
			style += f'\tbackground-color: {parent.fr_bg_color_sel};\n'

		style += '}' # End of QMainWindow normal pseudo-state

	# QMainWindow build and apply the stylesheet
	parent.fr_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.fr_stylesheet.appendPlainText(line)

		parent.fr_frame.setStyleSheet(style)

def clear_fr_stylesheet(parent):
	parent.fr_normal = False
	parent.fr_fg_color_sel = False
	parent.fr_bg_color_sel = False
	parent.fr_fg_color_lb.setStyleSheet('')
	parent.fr_bg_color_lb.setStyleSheet('')
	parent.fr_frame.setStyleSheet('')
	parent.fr_stylesheet.clear()

######### QGroupBox Stylesheet #########

def create_gb_stylesheet(parent):
	style = False

	# QMainWindow normal pseudo-state
	if parent.gb_normal:
		style = 'QGroupBox {\n'

		# color
		if parent.gb_fg_color_sel:
			style += f'\tcolor: {parent.gb_fg_color_sel};\n'
		if parent.gb_bg_color_sel:
			style += f'\tbackground-color: {parent.gb_bg_color_sel};\n'

		style += '}' # End of QMainWindow normal pseudo-state

	# QMainWindow build and apply the stylesheet
	parent.gb_stylesheet.clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			parent.gb_stylesheet.appendPlainText(line)

		parent.gb_groupbox.setStyleSheet(style)

def clear_gb_stylesheet(parent):
	parent.gb_normal = False
	parent.gb_fg_color_sel = False
	parent.gb_bg_color_sel = False
	parent.gb_fg_color_lb.setStyleSheet('')
	parent.gb_bg_color_lb.setStyleSheet('')
	parent.gb_groupbox.setStyleSheet('')
	parent.gb_stylesheet.clear()


