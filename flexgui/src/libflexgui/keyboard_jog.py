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

	#print(f'jog mode text {parent.jog_modes_cb.currentText()}')
	#print(f'jog mode data {parent.jog_modes_cb.currentData()}')

	if parent.status.task_mode == emc.MODE_MANUAL and action:
		#print(f'jog {action} axis {axis} direction {direction} vel {vel}')

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

	# jog_modes_cb

		#print(f'parent.status.kinematics_type {parent.status.kinematics_type}')
		#print(f'emc.KINEMATICS_IDENTITY {emc.KINEMATICS_IDENTITY}')
		#print(f'parent.status.motion_mode {parent.status.motion_mode}')
		#print(f'emc.TRAJ_MODE_FREE {emc.TRAJ_MODE_FREE}')
		#print(f'emc.TRAJ_MODE_TELEOP {emc.TRAJ_MODE_TELEOP}')
		#print(f'{}')

	#if parent.status.kinematics_type == emc.KINEMATICS_IDENTITY:
	#	print('KINEMATICS_IDENTITY')
	#else:
	#	print('Unknown Kinematics')



'''
 teleop_enable(int)

    Enable/disable teleop mode (disable for joint jogging).


 jog(command-constant, bool, int[, float[, float]])

    Syntax

        jog(command, jjogmode, joint_num_or_axis_index, velocity[, distance])
        jog(linuxcnc.JOG_STOP, jjogmode, joint_num_or_axis_index)
        jog(linuxcnc.JOG_CONTINUOUS, jjogmode, joint_num_or_axis_index, velocity)
        jog(linuxcnc.JOG_INCREMENT, jjogmode, joint_num_or_axis_index, velocity, distance)
    Command Constants

        linuxcnc.JOG_STOP
        linuxcnc.JOG_CONTINUOUS
        linuxcnc.JOG_INCREMENT
    jjogmode

        True

            request individual joint jog (requires teleop_enable(0))
        False

            request axis Cartesian coordinate jog (requires teleop_enable(1))

    joint_num_or_axis_index

        For joint jog (jjogmode=1)

            joint_number
        For axis Cartesian coordinate jog (jjogmode=0)

            zero-based index of the axis coordinate with respect to the known coordinate letters XYZABCUVW (x=>0,y=>1,z=>2,a=>3,b=>4,c=>5,u=>6,v=>7,w=>8)



		if increment:
			parent.command.jog(emc.JOG_INCREMENT, jjogmode, joint, vel, increment)
		else:
			parent.command.jog(emc.JOG_CONTINUOUS, jjogmode, joint, vel)
	else:
		parent.command.jog(emc.JOG_STOP, jjogmode, joint)


def get_jog_mode(parent):
	parent.status.poll()
	if parent.status.kinematics_type == emc.KINEMATICS_IDENTITY and utilities.all_homed(parent):
		teleop_mode = 1
		jjogmode = False
	else:
		# check motion_mode since other guis (halui) could alter it
		if parent.status.motion_mode == emc.TRAJ_MODE_FREE:
			teleop_mode = 0
			jjogmode = True
		else:
			teleop_mode = 1
			jjogmode = False

	if ((jjogmode and parent.status.motion_mode != emc.TRAJ_MODE_FREE)
		or (not jjogmode and parent.status.motion_mode != emc.TRAJ_MODE_TELEOP) ):
		set_motion_teleop(parent, teleop_mode)
	return jjogmode

def set_motion_teleop(parent, value):
	# 1:teleop, 0: joint
	parent.command.teleop_enable(value)
	parent.command.wait_complete()
	parent.status.poll()

def jog(parent):
	vel = parent.jog_vel_sl.value() / 60
	jog_command = parent.sender().objectName().split('_')

	if 'minus' in jog_command:
		vel = -vel

	joint = int(jog_command[-1])
	increment = parent.jog_modes_cb.currentData()

	jjogmode = get_jog_mode(parent)
	print(f'jjogmode {jjogmode}')
	if parent.sender().isDown():
		if increment:
			parent.command.jog(emc.JOG_INCREMENT, jjogmode, joint, vel, increment)
		else:
			parent.command.jog(emc.JOG_CONTINUOUS, jjogmode, joint, vel)
	else:
		parent.command.jog(emc.JOG_STOP, jjogmode, joint)
		if 'override_limits_cb' in parent.children:
			parent.override_limits_cb.setChecked(False)
			parent.override_limits_cb.setEnabled(False)


'''
