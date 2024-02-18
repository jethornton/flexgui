
def update(parent):
	parent.status.poll()
	for key, value in parent.status_labels.items(): # update all status labels
		# get the label and set the text to the status value of the key
		getattr(parent, f'{value}').setText(f'{getattr(parent.status, f"{key}")}')

	for key, value in parent.axis_labels.items():
		getattr(parent, f'{value}').setText(f'{getattr(parent.status, "axis")[int(value[5])][key]}')

	# axis_{i}_{item}_lb
	# axis_0_velocity_lb
