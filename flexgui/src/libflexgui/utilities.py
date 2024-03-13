


def all_homed(parent):
	parent.status.poll()
	num_joints = parent.status.joints
	for i,h in enumerate(parent.status.homed):
		if i >= num_joints: break
		if h == 0:
			all_homed = False
			break
		elif h == 1: all_homed = True
	return all_homed

def all_unhomed(parent):
	parent.status.poll()
	num_joints = parent.status.joints
	for i,h in enumerate(parent.status.homed):
		if i >= num_joints: break
		if h == 1:
			all_unhomed = False
			break
		elif h == 0: all_unhomed = True
	return all_unhomed

