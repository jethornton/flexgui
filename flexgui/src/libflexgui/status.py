
def update(parent):
	parent.status.poll()
	for key, value in parent.status_labels.items(): # update all status labels
		getattr(parent, f'{value}').setText(f'{getattr(parent.status, f"{key}")}')
