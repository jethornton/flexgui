
def update(parent):
	parent.status.poll()
	for key, value in parent.status_labels.items(): # update all status labels
		# get the label and set the text to the status value of the key
		getattr(parent, f'{value}').setText(f'{getattr(parent.status, f"{key}")}')
