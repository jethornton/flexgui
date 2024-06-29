Status Labels
=============

Status labels come in two forms, single status items like `Machine Status` and
multiple status labels like the `joint` dictionary which has multiple items and
displays for all joints. Multiple status labels use a number identifier to
select the axis, joint or spindle information wanted. When creating a status
label set the `objectName` to the status you want.


.. image:: /images/status-01.png
   :align: center

Precision
---------

Labels that return float values default precision is 3 for metric and 4 for
inch.

To override the default, select the label then click on the Green Plus sign in
the Property Editor and select String...

.. image:: /images/status-02.png
   :align: center

Set the Property Name to `precision`.

.. image:: /images/status-03.png
   :align: center

Set the Value to how many decimal places you want for that status label.

.. image:: /images/status-04.png
   :align: center

For more information about status labels read the LinuxCNC `Python Interface
Status Attributes <http://linuxcnc.org/docs/stable/html/config/python-interface.html#_linuxcnc_stat_attributes>`_.

Status Labels
-------------

.. csv-table:: Single Status Labels
   :width: 100%
   :align: left

	acceleration_lb, flood_lb, pocket_prepped_lb
	active_queue_lb, gcodes_lb, probe_tripped_lb
	adaptive_feed_enabled_lb, g5x_index_lb, probe_val_lb
	angular_units_lb, ini_filename_lb, probed_position_lb
	axis_mask_lb, inpos_lb, probing_lb
	block_delete_lb, input_timeout_lb, program_units_lb
	call_level_lb, interp_state_lb, queue_lb
	command_lb, interpreter_errcode_lb, queue_full_lb
	current_line_lb, joints_lb, rapidrate_lb
	current_vel_lb, kinematics_type_lb, read_line_lb
	cycle_time_lb, linear_units_lb, rotation_xy_lb
	debug_lb, lube_lb, settings_lb
	delay_left_lb, lube_level_lb, spindles_lb
	distance_to_go_lb, max_acceleration_lb, state_lb
	echo_serial_number_lb, max_velocity_lb, task_mode_lb
	enabled_lb, mcodes_lb, task_paused_lb
	estop_lb, mist_lb, task_state_lb
	exec_state_lb, motion_line_lb, tool_in_spindle_lb
	feed_hold_enabled_lb, motion_mode_lb, tool_from_pocket_lb
	 motion_type_lb, tool_offset_lb, feedrate_lb, optional_stop_lb
	file_lb, paused_lb, 

.. note:: You don't have to use all the labels, the ones found will be

Axis Status
-----------

The Axis status contains status items for 9 axes. Replace the `_n_` with the
number of the axis. Axis numbers start at 0 and go through to 8. Returns a float.

.. csv-table:: Axis Status Labels
   :width: 100%
   :align: left

	axis_n_max_position_limit_lb, axis_n_min_position_limit_lb, axis_n_velocity_lb
	axis_n_vel_per_min_lb

.. note:: The Axis velocity label only reports back jogging speed, use the
          joint velocity label for speed.

Joint Status
------------

The Joint status contains status items for 16 joints. Replace the `_n_` with the
number of the joint. Joint numbers start at 0 and go through to 15.

.. csv-table:: Joint Status Labels
   :width: 100%
   :align: left

	joint_backlash_n_lb, joint_input_n_lb, joint_min_position_limit
	joint_enabled_n_lb, joint_jointType_n_lb, joint_in_soft_limit_n_lb
	joint_fault_n_lb, joint_max_ferror_n_lb, joint_output_n_lb
	joint_ferror_current_n_lb, joint_max_hard_limit_n_lb, joint_override_limits_n_lb
	joint_ferror_highmark_n_lb, joint_max_position_limit_n_lb, joint_units_n_lb
	joint_homed_n_lb, joint_max_soft_limit_n_lb, joint_vel_sec_n_lb
	joint_vel_min_n_lb, joint_homing_n_lb, joint_min_ferror_n_lb
	joint_inpos_n_lb, joint_min_hard_limit_n_lb,

Special Labels
--------------

Run from line label

`start_line_lb`

Axis machine position labels no offsets. Returns a float.

.. csv-table:: Machine Position Status Labels
   :width: 100%
   :align: left

	actual_lb_x, actual_lb_y, actual_lb_z
	actual_lb_a, actual_lb_b, actual_lb_c
	actual_lb_u, actual_lb_v, actual_lb_w


Axis position labels including all offsets. Returns a float.

.. csv-table:: DRO Status Labels
   :width: 100%
   :align: left

	dro_lb_x, dro_lb_y, dro_lb_z
	dro_lb_a, dro_lb_b, dro_lb_c
	dro_lb_u, dro_lb_v, dro_lb_w

Axis homed labels

.. csv-table:: Axis Homed Labels
   :width: 100%
   :align: left

	home_lb_0, home_lb_1, home_lb_2
	home_lb_3, home_lb_4, home_lb_5
	home_lb_6, home_lb_7, home_lb_8


Offsets for the currently active G5x coordinate system. Returns a float.

.. csv-table:: G5x Status Labels
   :width: 100%
   :align: left

	g5x_lb_x, g5x_lb_y, g5x_lb_z
	g5x_lb_a, g5x_lb_b, g5x_lb_c
	g5x_lb_u, g5x_lb_v, g5x_lb_w

Offsets for G92.  Returns a float.

.. csv-table:: G92 Status Labels
   :width: 100%
   :align: left

	g92_lb_x, g92_lb_y, g92_lb_z
	g92_lb_a, g92_lb_b, g92_lb_c
	g92_lb_u, g92_lb_v, g92_lb_w

Velocity Labels
---------------

Tool velocity using two perpendicular joint velocities.

Name the label `two_vel_lb` and add two int type Dynamic Properties called
`joint_0` and `joint_1` and set the values to the perpendicular joint numbers
you want to calculate. Typically this would be for the X and Y axes.

To select an int type of Dynamic Property select `Other` after clicking on the
green plus sign.

.. image:: /images/status-05.png
   :align: center

Then select the Property Type of `int`

.. image:: /images/status-06.png
   :align: center

The two Dynamic Properties should look like this

.. image:: /images/status-07.png
   :align: center

Tool velocity using three perpendicular joint velocities.

Name the label `three_vel_lb` and add three int type Dynamic Properties called
`joint_0`, `joint_1` and `joint_2` and set the values to the perpendicular joint
numbers you want to calculate. Typically this would be for the X, Y and Z axes.

Comming soon:
Tool teeth label and Feed per Tooth label... stay tuned.

Spindle Status
--------------

The Spindle status contains status items for 9 spindles. Replace the `_n_` with the
number of the spindle. Spindle numbers start at 0 and go through to 8.

.. csv-table:: Spindle Status Labels
   :width: 100%
   :align: left

	spindle_brake_n_lb, spindle_direction_n_lb, spindle_enabled_n_lb
	spindle_override_enabled_n_lb, spindle_speed_n_lb, spindle_override_n_lb
	spindle_homed_n_lb, spindle_orient_state_n_lb, spindle_orient_fault_n_lb
	spindle_actual_speed_lb

.. note:: Spindle speed is the commanded speed not the actual speed if an
   override is in effect.

Spindle speed setting label `spindle_speed_lb` shows the current spindle
speed setting even if the spindle is not running.

I/O Status
----------

The I/O status contains status items for 64 I/O's. Replace the `_n_` with the
number of the joint. Joint numbers start at 0 and go through to 63. Analog
I/O returns a float.

.. csv-table:: I/O Status Labels
   :width: 100%
   :align: left

	ain_n_lb, aout_n_lb, din_n_lb
	dout_n_lb

Current Tool Status
-------------------

Current Tool status of the tool loaded in the spindle

.. csv-table:: Tool Table Status Labels
   :width: 100%
   :align: left

	tool_id_lb, tool_xoffset_lb, tool_yoffset_lb
	tool_zoffset_lb, tool_aoffset_lb, tool_boffset_lb
	tool_coffset_lb, tool_uoffset_lb, tool_voffset_lb
	tool_woffset_lb, tool_diameter_lb, tool_frontangle_lb
	tool_backangle_lb, tool_orientation_lb

	settings_feed_lb, settings_speed_lb
