

def toggle(parent):
	if parent.sender().isChecked():
		for child in parent.children:
			if child.startswith('probe_'):
				getattr(parent, child).setEnabled(True)
		for key, value in parent.program_running.items():
			getattr(parent, key).setEnabled(False)

	else:
		for child in parent.children:
			if child.startswith('probe_'):
				getattr(parent, child).setEnabled(False)
		for key, value in parent.program_running.items():
			getattr(parent, key).setEnabled(True)



