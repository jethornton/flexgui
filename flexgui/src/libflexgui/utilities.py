
def is_float(string):
	try:
		float(string)
		return True
	except ValueError:
		return False

def is_int(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def all_homed(parent):
	parent.status.poll()
	num_joints = parent.status.joints
	for i, h in enumerate(parent.status.homed):
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

def home_all_check(parent):
	parent.status.poll()
	for i in range(parent.status.joints):
		if parent.inifile.find(f'JOINT_{i}', 'HOME_SEQUENCE') is None:
			return False
	return True

def update_jog_lb(parent):
	parent.jog_vel_lb.setText(f'{parent.jog_vel_s.value()} {parent.units}/min')

def add_mdi(parent):
	parent.mdi_command_le.setText(f'{parent.mdi_history_lw.currentItem().text()}')

def spindle_speed(parent):
	parent.spindle_speed = parent.spindle_speed_sb.value()


