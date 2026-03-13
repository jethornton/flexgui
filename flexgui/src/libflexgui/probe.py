import linuxcnc as emc

def toggle(parent):
	btn = parent.sender()
	on_text = btn.property('on_text')
	off_text = btn.property('off_text')

	if parent.probing_enable_pb.isChecked():
		parent.probing = True
		for item in parent.run_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.file_load_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.mdi_controls:
			getattr(parent, item).setEnabled(False)
		for item in parent.probe_controls:
			getattr(parent, item).setEnabled(True)

		if None not in [on_text, off_text]:
			btn.setText(on_text)

		if 'probing_enable_pb' in parent.child_names and hasattr(parent.probing_enable_pb, 'led'):
			parent.probing_enable_pb.led = True

		if parent.probe_enable_on_color:
			parent.probing_enable_pb.setStyleSheet(parent.probe_enable_on_color)

	else: # probing is disabled
		parent.probing = False
		for item in parent.run_controls:
			getattr(parent, item).setEnabled(True)
		for item in parent.file_load_controls:
			getattr(parent, item).setEnabled(True)
		for item in parent.mdi_controls:
			getattr(parent, item).setEnabled(True)
		for item in parent.probe_controls:
			getattr(parent, item).setEnabled(False)

		if None not in [on_text, off_text]:
			btn.setText(off_text)

		if 'probing_enable_pb' in parent.child_names and hasattr(parent.probing_enable_pb, 'led'):
			parent.probing_enable_pb.led = False

		if parent.probe_enable_off_color:
			parent.probing_enable_pb.setStyleSheet(parent.probe_enable_off_color)

