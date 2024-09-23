import linuxcnc as emc

def toggle(parent):
	if parent.sender().isChecked():
		for child in parent.children:
			if child.startswith('probe_'):
				getattr(parent, child).setEnabled(True)
		for key, value in parent.program_running.items():
			getattr(parent, key).setEnabled(False)
		parent.spindle_speed = 0
		if 'spindle_speed_lb' in parent.children:
			parent.spindle_speed_lb.setText(f'{parent.spindle_speed}')
		parent.command.spindle(emc.SPINDLE_OFF)

	else:
		for child in parent.children:
			if child.startswith('probe_'):
				getattr(parent, child).setEnabled(False)
		for key, value in parent.program_running.items():
			getattr(parent, key).setEnabled(True)



