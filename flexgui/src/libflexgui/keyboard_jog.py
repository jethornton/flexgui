import linuxcnc as emc

def jog(parent, action, axis, direction=None):
	vel = parent.jog_vel_sl.value() / 60
	if direction == 'neg':
		vel = -vel
	if parent.status.motion_mode == emc.TRAJ_MODE_FREE:
		teleop_mode = 0
		joint_jog = True
	else: # all axes are homed
		teleop_mode = 1
		joint_jog = False

	if parent.status.task_mode == emc.MODE_MANUAL and action:

		# set teleop mode
		parent.command.teleop_enable(teleop_mode)
		parent.command.wait_complete()

		# set distance if jog_modes_cb.currenData() is not false
		distance = parent.jog_modes_cb.currentData()
		if distance:
			parent.command.jog(emc.JOG_INCREMENT, joint_jog, axis, vel, distance)
		else:
			parent.command.jog(emc.JOG_CONTINUOUS, joint_jog, axis, vel)
	else:
		parent.command.jog(emc.JOG_STOP, joint_jog, axis)

