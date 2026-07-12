import linuxcnc as emc

from libflexgui import utilities
from libflexgui import dialogs

def toggle(parent):
	parent.status.poll()
	for i in range(parent.status.spindles):
		if parent.status.spindle[i]['enabled'] == 1: # verified
			title = 'Error'
			msg = (f'Spindle "{i}" is enabled, probing is not possible.')
			info = f'Turn off Spindle "{i}" to enable probing.'
			dialogs.error_msg_ok(parent, title, msg, info)
			parent.probing_enable_pb.blockSignals(True)
			parent.probing_enable_pb.setChecked(False)
			parent.probing_enable_pb.blockSignals(False)
			return

	btn = parent.sender()
	on_text = btn.property('on_text')
	off_text = btn.property('off_text')

	if parent.probing_enable_pb.isChecked():
		parent.probing = True

		if None not in [on_text, off_text]:
			btn.setText(on_text)

		if 'probing_enable_pb' in parent.child_names and hasattr(parent.probing_enable_pb, 'led'):
			parent.probing_enable_pb.led = True

		#if parent.probe_enable_on_color:
		#	parent.probing_enable_pb.setStyleSheet(parent.probe_enable_on_color)

	else: # probing is disabled
		parent.probing = False

		if None not in [on_text, off_text]:
			btn.setText(off_text)

		if 'probing_enable_pb' in parent.child_names and hasattr(parent.probing_enable_pb, 'led'):
			parent.probing_enable_pb.led = False

		#if parent.probe_enable_off_color:
		#	parent.probing_enable_pb.setStyleSheet(parent.probe_enable_off_color)

	utilities.update_home_controls(parent)
	utilities.update_controls(parent)


