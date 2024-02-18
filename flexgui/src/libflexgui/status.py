
def update(parent):
	parent.status.poll()
	for key, value in parent.status_labels.items(): # update all status labels
		# get the label and set the text to the status value of the key
		getattr(parent, f'{value}').setText(f'{getattr(parent, "status").key}')

	for key, value in parent.axis_labels.items():
		if key == 'velocity':
			vel = abs(round(getattr(parent, 'status').axis[int(value[5])][key] * 60, 1))
			getattr(parent, f'{value}').setText(f'{vel}')
		else:
			getattr(parent, f'{value}').setText(f'{getattr(parent, "status").axis[int(value[5])][key]}')

	for key, value in parent.joint_labels.items():
		getattr(parent, f'{value}').setText(f'{getattr(parent, "status").joint[int(value[6])][key]}')



