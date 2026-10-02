#!/usr/bin/env python3

STATES_MAP = {
	'QCheckBox': ['normal', 'hover', 'pressed', 'checked', 'disabled'],
	'QPushButton': ['normal', 'hover', 'pressed', 'checked', 'disabled'],
	'QRadioButton': ['normal', 'hover', 'pressed', 'checked', 'disabled'],
	'QLabel': ['normal', 'hover', 'disabled'],
	'QLineEdit': ['normal', 'hover', 'disabled'],
	'QSpinBox': ['normal', 'hover', 'disabled']
}

def create_stylesheet(parent, widget_type, widget_name, prefix):
	style = ''

	# normal pseudo-state
	if getattr(parent, f'{prefix}_normal'):
		style = f'{widget_type}' + ' {\n' # the { can't be in the f string

		# color
		fg_color = getattr(parent, f'{prefix}_fg_color_sel_normal')
		if fg_color:
			style += f'\tcolor: {fg_color};\n'

		bg_color = getattr(parent, f'{prefix}_bg_color_sel_normal')
		if bg_color:
			style += f'\tbackground-color: {bg_color};\n'

		# font
		font_family = getattr(parent, f'{prefix}_font_family')
		if font_family:
			style += f'\tfont-family: {font_family};\n'

		font_size = getattr(parent, f'{prefix}_font_size')
		if font_size:
			style += f'\tfont-size: {font_size}pt;\n'

		font_weight = getattr(parent, f'{prefix}_font_weight')
		if font_weight:
			style += f'\tfont-weight: {font_weight};\n'

		# size
		min_width = getattr(parent, f'{prefix}_min_width_normal').value()
		if min_width > 0:
			style += f'\tmin-width: {min_width}px;\n'

		min_height = getattr(parent, f'{prefix}_min_height_normal').value()
		if min_height > 0:
			style += f'\tmin-height: {min_height}px;\n'

		max_width = getattr(parent, f'{prefix}_max_width_normal').value()
		if max_width > 0:
			style += f'\tmax-width: {max_width}px;\n'

		max_height = getattr(parent, f'{prefix}_max_height_normal').value()
		if max_height > 0:
			style += f'\tmax-height: {max_height}px;\n'

		# border width must be bigger than 0
		border_type = getattr(parent, f'{prefix}_border_type_normal').currentText()
		if border_type != 'Select':
			style += f'\tborder-style: {border_type};\n'

			border_width = getattr(parent, f'{prefix}_border_width_normal').value()
			if border_width > 0:
				style += f'\tborder-width: {border_width}px;\n'
			else:
				getattr(parent, f'{prefix}_border_width_normal').setValue(1)
				style += '\tborder-width: 1px;\n'

			border_radius = getattr(parent, f'{prefix}_border_radius_normal').value()
			style += f'\tborder-radius: {border_radius}px;\n'

			border_color = getattr(parent, f'{prefix}_border_color_sel_normal')
			if border_color:
				style += f'\tborder-color: {border_color};\n'
			else:
				#cb_border_color_normal_lb
				getattr(parent, f'{prefix}_border_color_normal_lb').setStyleSheet(f'background-color: black;')
				style += '\tborder-color: black;\n'

		# padding
		padding = getattr(parent, f'{prefix}_padding_normal').value()
		if padding > 0:
			style += f'\tpadding: {padding};\n'

		padding_left = getattr(parent, f'{prefix}_padding_left_normal').value()
		if padding_left > 0:
			style += f'\tpadding-left: {padding_left};\n'

		padding_right = getattr(parent, f'{prefix}_padding_right_normal').value()
		if padding_right > 0:
			style += f'\tpadding-right: {padding_right};\n'

		padding_top = getattr(parent, f'{prefix}_padding_top_normal').value()
		if padding_top > 0:
			style += f'\tpadding-top: {padding_top};\n'

		padding_bottom = getattr(parent, f'{prefix}_padding_bottom_normal').value()
		if padding_bottom > 0:
			style += f'\tpadding-bottom: {padding_bottom};\n'

		# margin
		margin = getattr(parent, f'{prefix}_margin_normal').value()
		if margin > 0:
			style += f'\tmargin: {margin};\n'

		margin_left = getattr(parent, f'{prefix}_margin_left_normal').value()
		if margin_left > 0:
			style += f'\tmargin-left: {margin_left};\n'

		margin_right = getattr(parent, f'{prefix}_margin_right_normal').value()
		if margin_right > 0:
			style += f'\tmargin-right: {margin_right};\n'

		margin_top = getattr(parent, f'{prefix}_margin_top_normal').value()
		if margin_top > 0:
			style += f'\tmargin-top: {margin_top};\n'

		margin_bottom = getattr(parent, f'{prefix}_margin_bottom_normal').value()
		if margin_bottom > 0:
			style += f'\tmargin-bottom: {margin_bottom};\n'

		style += '}' # End of normal pseudo-state

	# checked pseudo-state
	if 'checked' in STATES_MAP[widget_type] and getattr(parent, f'{prefix}_checked'):
		style += f'\n\n{widget_type}:checked' + ' {\n'

		# color
		fg_color_checked = getattr(parent, f'{prefix}_fg_color_sel_checked')
		if fg_color_checked:
			style += f'\tcolor: {fg_color_checked};\n'

		bg_color_checked = getattr(parent, f'{prefix}_bg_color_sel_checked')
		if bg_color_checked:
			style += f'\tbackground-color: {bg_color_checked};\n'

		# border FIXME like normal
		border_type_checked = getattr(parent, f'{prefix}_border_type_checked').currentText()
		if border_type_checked != 'Select':
			style += f'\tborder-style: {border_type_checked};\n'

		border_width_checked = getattr(parent, f'{prefix}_border_width_checked').value()
		if border_width_checked > 0:
			style += f'\tborder-width: {border_width_checked}px;\n'

		border_radius_checked = getattr(parent, f'{prefix}_border_radius_checked').value()
		if border_radius_checked > 0:
			style += f'\tborder-radius: {border_radius_checked}px;\n'

		border_color_checked = getattr(parent, f'{prefix}_border_color_sel_checked')
		if border_color_checked:
			style += f'\tborder-color: {border_color_checked};\n'

		style += '}' # End of QCheckBox checked pseudo-state

	# pressed pseudo-state
	if 'pressed' in STATES_MAP[widget_type] and getattr(parent, f'{prefix}_pressed'):
		style += f'\n\n{widget_type}:pressed' + ' {\n'

		# color
		fg_color_pressed = getattr(parent, f'{prefix}_fg_color_sel_pressed')
		if fg_color_pressed:
			style += f'\tcolor: {fg_color_pressed};\n'

		bg_color_pressed = getattr(parent, f'{prefix}_bg_color_sel_pressed')
		if bg_color_pressed:
			style += f'\tbackground-color: {bg_color_pressed};\n'

		# border FIXME like normal
		border_type_pressed = getattr(parent, f'{prefix}_border_type_pressed').currentText()
		if border_type_pressed != 'Select':
			style += f'\tborder-style: {border_type_pressed};\n'

		border_width_pressed = getattr(parent, f'{prefix}_border_width_pressed').value()
		if border_width_pressed > 0:
			style += f'\tborder-width: {border_width_pressed}px;\n'

		border_radius_pressed = getattr(parent, f'{prefix}_border_radius_pressed').value()
		if border_radius_pressed > 0:
			style += f'\tborder-radius: {border_radius_pressed}px;\n'

		border_color_pressed = getattr(parent, f'{prefix}_border_color_sel_pressed')
		if border_color_pressed:
			style += f'\tborder-color: {border_color_pressed};\n'

		style += '}' # End of QCheckBox pressed pseudo-state

	# hover pseudo-state
	if getattr(parent, f'{prefix}_hover'):
		style += f'\n\n{widget_type}:hover' + ' {\n'

		# color
		fg_color_hover = getattr(parent, f'{prefix}_fg_color_sel_hover')
		if fg_color_hover:
			style += f'\tcolor: {fg_color_hover};\n'

		bg_color_hover = getattr(parent, f'{prefix}_bg_color_sel_hover')
		if bg_color_hover:
			style += f'\tbackground-color: {bg_color_hover};\n'

		# border FIXME like normal
		border_type_hover = getattr(parent, f'{prefix}_border_type_hover').currentText()
		if border_type_hover != 'Select':
			style += f'\tborder-style: {border_type_hover};\n'

		border_width_hover = getattr(parent, f'{prefix}_border_width_hover').value()
		if border_width_hover > 0:
			style += f'\tborder-width: {border_width_hover}px;\n'

		border_radius_hover = getattr(parent, f'{prefix}_border_radius_hover').value()
		if border_radius_hover > 0:
			style += f'\tborder-radius: {border_radius_hover}px;\n'

		border_color_hover = getattr(parent, f'{prefix}_border_color_sel_hover')
		if border_color_hover:
			style += f'\tborder-color: {border_color_hover};\n'

		style += '}' # End of hover pseudo-state

	# disabled pseudo-state
	if getattr(parent, f'{prefix}_disabled'):
		style += f'\n\n{widget_type}:disabled' + ' {\n'

		# color
		fg_color_disabled = getattr(parent, f'{prefix}_fg_color_sel_disabled')
		if fg_color_disabled:
			style += f'\tcolor: {fg_color_disabled};\n'

		bg_color_disabled = getattr(parent, f'{prefix}_bg_color_sel_disabled')
		if bg_color_disabled:
			style += f'\tbackground-color: {bg_color_disabled};\n'

		# border FIXME like normal
		border_type_disabled = getattr(parent, f'{prefix}_border_type_disabled').currentText()
		if border_type_disabled != 'Select':
			style += f'\tborder-style: {border_type_disabled};\n'

		border_width_disabled = getattr(parent, f'{prefix}_border_width_disabled').value()
		if border_width_disabled > 0:
			style += f'\tborder-width: {border_width_disabled}px;\n'

		border_radius_disabled = getattr(parent, f'{prefix}_border_radius_disabled').value()
		if border_radius_disabled > 0:
			style += f'\tborder-radius: {border_radius_disabled}px;\n'

		border_color_disabled = getattr(parent, f'{prefix}_border_color_sel_disabled')
		if border_color_disabled:
			style += f'\tborder-color: {border_color_disabled};\n'

		style += '\n}' # End of disabled pseudo-state


	# build and apply the stylesheet
	getattr(parent, f'{prefix}_stylesheet').clear()
	if style:
		lines = style.splitlines()
		for line in lines:
			getattr(parent,f'{prefix}_stylesheet').appendPlainText(line)

		if widget_type != 'QRadioButton':
			getattr(parent, widget_name).setStyleSheet(style)
		elif widget_type == 'QRadioButton':
			parent.radioButton_0.setStyleSheet(style)
			parent.radioButton_1.setStyleSheet(style)

		return
		'''
		 = getattr(parent, f'{prefix}')

	# QCheckBox indicator sub-control FIXME later...
	if getattr(parent, f'{prefix}_indicator'):
		pass

	if parent.cb_indicator:
		if style: # style is not False
			style += '\n\nQCheckBox::indicator {\n'
		else:
			style = 'QCheckBox::indicator {\n'
		if parent.cb_indicator_bg_color:
			style += f'\tbackground: {parent.cb_indicator_bg_color};\n'
		if parent.cb_indicator_width_normal.value() > 0:
			style += f'\twidth: {parent.cb_indicator_width_normal.value()}px;\n'
		if parent.cb_indicator_height_normal.value() > 0:
			style += f'\theight: {parent.cb_indicator_height_normal.value()}px;\n'
		style += '}' # End of QCheckBox::indicator

	if parent.cb_indicator_checked:
		if style: # style is not False
			style += '\n\nQCheckBox::indicator:checked {\n'
		else:
			style = 'QCheckBox::indicator:checked {\n'
		style += f'\timage: url({parent.cb_indicator_icon_checked.text()});\n'
		style += '}' # End of QCheckBox::indicator:checked

	if parent.cb_indicator_unchecked:
		if style: # style is not False
			style += '\n\nQCheckBox::indicator:unchecked {\n'
		else:
			style = 'QCheckBox::indicator:unchecked {\n'
		style += f'\timage: url({parent.cb_indicator_icon_unchecked.text()});\n'
		style += '}' # End of QCheckBox::indicator:checked
		'''


def clear_stylesheet(parent, widget_type, widget_name, prefix):
	setattr(parent, f'{prefix}_normal', False)

	# 2. Safely grab the correct list of states (default to empty list if not found)
	pseudo_states = STATES_MAP.get(widget_type, [])

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

