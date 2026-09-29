#!/usr/bin/env python3

def create_stylesheet(parent, widget_type, prefix):
	print(f'create_stylesheet {widget_type} prefix {prefix}')


def clear_stylesheet(parent, widget_type, widget_name, prefix):
	print(f'clear_stylesheet type {widget_type} name {widget_name} prefix {prefix}')

	setattr(parent, f'{prefix}_normal', False)

	# 1. Map the widget types to their corresponding lists using a dictionary
	states_map = {
		'QCheckBox': ['normal', 'hover', 'pressed', 'checked', 'disabled'],
		'QPushButton': ['normal', 'hover', 'pressed', 'checked', 'disabled'],
		'QRadioButton': ['normal', 'hover', 'pressed', 'checked', 'disabled'],
		'QLabel': ['normal', 'hover', 'disabled'],
		'QLineEdit': ['normal', 'hover', 'disabled'],
		'QSpinBox': ['normal', 'hover', 'disabled']
	}

	# 2. Safely grab the correct list of states (default to empty list if not found)
	pseudo_states = states_map.get(widget_type, [])

	# set all the variables to False
	for item in pseudo_states:
		setattr(parent, f'{prefix}_{item}', False) # build section flag
		setattr(parent, f'{prefix}_fg_color_sel_{item}', False)
		setattr(parent, f'{prefix}_bg_color_sel_{item}', False)
		setattr(parent, f'{prefix}_border_color_sel_{item}', False)

	# clear all the colors
	for item in pseudo_states:
		label = getattr(parent, f'{prefix}_fg_color_{item}').property('label')
		getattr(parent, label).setStyleSheet('background-color: none;')
		
		label = getattr(parent, f'{prefix}_bg_color_{item}').property('label')
		getattr(parent, label).setStyleSheet('background-color: none;')
		
		label = getattr(parent, f'{prefix}_border_color_{item}').property('label')
		getattr(parent, label).setStyleSheet('background-color: none;')

	# set border to none and 0
	for item in pseudo_states:
		getattr(parent, f'{prefix}_border_type_{item}').setCurrentIndex(0)
		getattr(parent, f'{prefix}_border_width_{item}').setValue(0)
		getattr(parent, f'{prefix}_border_radius_{item}').setValue(0)

	# clear the font variables
	setattr(parent, f'{prefix}_font_family', False)
	setattr(parent, f'{prefix}_font_size', False)
	setattr(parent, f'{prefix}_font_weight', False)
	setattr(parent, f'{prefix}_font_style', False)
	setattr(parent, f'{prefix}_font_italic', False)

	getattr(parent, f'{prefix}_min_width_normal').setValue(0)
	getattr(parent, f'{prefix}_min_height_normal').setValue(0)
	getattr(parent, f'{prefix}_max_width_normal').setValue(0)
	getattr(parent, f'{prefix}_max_height_normal').setValue(0)
	getattr(parent, f'{prefix}_padding_normal').setValue(0)
	getattr(parent, f'{prefix}_padding_left_normal').setValue(0)
	getattr(parent, f'{prefix}_padding_right_normal').setValue(0)
	getattr(parent, f'{prefix}_padding_top_normal').setValue(0)
	getattr(parent, f'{prefix}_padding_bottom_normal').setValue(0)
	getattr(parent, f'{prefix}_margin_normal').setValue(0)
	getattr(parent, f'{prefix}_margin_left_normal').setValue(0)
	getattr(parent, f'{prefix}_margin_right_normal').setValue(0)
	getattr(parent, f'{prefix}_margin_top_normal').setValue(0)
	getattr(parent, f'{prefix}_margin_top_normal').setValue(0)

	getattr(parent, f'{prefix}_stylesheet').clear()

	if widget_name == 'checkBox':
		parent.checkBox.setStyleSheet('')
		parent.cb_indicator_color_normal.setStyleSheet('background-color: none;')
		parent.cb_indicator_width_normal.setValue(0)
		parent.cb_indicator_height_normal.setValue(0)
	elif widget_name == 'radioButton':
		parent.radioButton_0.setStyleSheet('')
		parent.radioButton_1.setStyleSheet('')
	else:
		getattr(parent, f'{widget_name}').setStyleSheet('')

