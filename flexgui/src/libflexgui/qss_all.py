from functools import partial

from libflexgui import qss_pushbutton
from libflexgui import qss_checkbox
from libflexgui import qss_radiobutton
from libflexgui import qss_toolbar
from libflexgui import qss_toolbutton
from libflexgui import qss_spinbox
from libflexgui import qss_label

def startup(parent):

	# All
	parent.all_normal = False
	parent.all_apply_style.clicked.connect(partial(all_create_stylesheet, parent))

	parent.all_fg_color_normal.clicked.connect(parent.color_dialog)
	parent.all_bg_color_normal.clicked.connect(parent.color_dialog)

	parent.all_fg_color_sel_normal = False
	parent.all_bg_color_sel_normal = False

def all_create_stylesheet(parent):
	style = False

	# Foreground Color
	if parent.all_fg_color_sel_normal:
		color = parent.all_fg_color_sel_normal

		# QPushButton
		parent.pb_normal = True
		label = parent.pb_fg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.pb_fg_color_sel_normal = color

		# QCheckBox
		parent.cb_normal = True
		label = parent.cb_fg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.cb_fg_color_sel_normal = color

		# QRadioButton
		parent.rb_normal = True
		label = parent.rb_fg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.rb_fg_color_sel_normal = color

		# QToolButton
		parent.tb_normal = True
		label = parent.tb_fg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.tb_fg_color_sel_normal = color

		# QSpinBox
		parent.sb_normal = True
		label = parent.sb_fg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.sb_fg_color_sel_normal = color

		# QLabel
		parent.lb_normal = True
		label = parent.lb_fg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.lb_fg_color_sel_normal = color

	# Background Color
	if parent.all_bg_color_sel_normal:
		color = parent.all_bg_color_sel_normal

		# QPushButton
		parent.pb_normal = True
		label = parent.pb_bg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.pb_bg_color_sel_normal = color

		# QCheckBox
		parent.cb_normal = True
		label = parent.cb_bg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.cb_bg_color_sel_normal = color

		# QRadioButton
		parent.rb_normal = True
		label = parent.rb_bg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.rb_bg_color_sel_normal = color

		# QToolButton
		parent.tb_normal = True
		label = parent.tb_bg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.tb_bg_color_sel_normal = color

		# QSpinBox
		parent.sb_normal = True
		label = parent.sb_bg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.sb_bg_color_sel_normal = color

		# QLabel
		parent.lb_normal = True
		label = parent.lb_bg_color_normal.property('label')
		getattr(parent, label).setStyleSheet(f'background-color: {color};')
		parent.lb_bg_color_sel_normal = color

	qss_pushbutton.create_stylesheet(parent)
	qss_checkbox.create_stylesheet(parent)
	qss_radiobutton.create_stylesheet(parent)
	qss_toolbutton.create_stylesheet(parent)
	qss_spinbox.create_stylesheet(parent)
	qss_label.create_stylesheet(parent)



