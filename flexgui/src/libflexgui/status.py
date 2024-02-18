

# motion_mode (returns integer) - This is the mode of the Motion controller.
# One of TRAJ_MODE_COORD, TRAJ_MODE_FREE, TRAJ_MODE_TELEOP

#print(stat_dict['motion_mode'][getattr(parent.status, 'motion_mode')])


def update(parent):
	parent.status.poll()
	stat_dict = {'motion_mode': {1: 'TRAJ_MODE_FREE', 2: 'TRAJ_MODE_COORD', 3: 'TRAJ_MODE_TELEOP'} }

	for key, value in parent.status_labels.items(): # update all status labels
		# get the label and set the text to the status value of the key
		if key in stat_dict:
			getattr(parent, f'{value}').setText(f'{stat_dict[key][getattr(parent.status, f"{key}")]}')
		else:
			getattr(parent, f'{value}').setText(f'{getattr(parent.status, f"{key}")}')

	for key, value in parent.axis_labels.items():
		if key == 'velocity':
			vel = abs(round(getattr(parent, 'status').axis[int(value[5])][key] * 60, 1))
			getattr(parent, f'{value}').setText(f'{vel}')
		else:
			getattr(parent, f'{value}').setText(f'{getattr(parent, "status").axis[int(value[5])][key]}')

	for key, value in parent.joint_labels.items():
		getattr(parent, f'{value}').setText(f'{getattr(parent, "status").joint[int(value[6])][key]}')



