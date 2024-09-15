

def enable(parent):
	if parent.sender().isChecked():
		for child in parent.children:
			if child.startswith('probe'):
				getattr(parent, child).setEnabled(True)
	else:
		for child in parent.children:
			if child.startswith('probe'):
				getattr(parent, child).setEnabled(False)



