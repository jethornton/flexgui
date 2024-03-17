Status Labels
=============

Status labels come in two forms, single status items like `Machine Status` and
multiple status labels like the `joint` dictionary which has multiple items and
displays for all joints. Multiple status labels use a number identifier to
select the axis, joint or spindle information wanted. When creating a status
label set the `objectName` to the status you want.

.. image:: /images/status-01.png
   :align: center

For more information about status labels read the LinuxCNC `Python Interface
Status Attributes <http://linuxcnc.org/docs/stable/html/config/python-interface.html#_linuxcnc_stat_attributes>`_.

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
	feed_override_enabled_lb, motion_type_lb, tool_offset_lb
	feedrate_lb, optional_stop_lb, velocity_lb
	file_lb, paused_lb, 


.. note:: You don't have to use all the labels, the ones found will be
  updated to the correct status

Axis Status
-----------

The Axis status contains status items for 9 axes. Replace the `_n_` with the
number of the axis. Axis numbers start at 0 and go through to 8.

.. csv-table:: Axis Status Labels
   :width: 100%
   :align: left

	axis_max_position_limit_n_lb, axis_min_position_limit_n_lb, velocity_n_lb

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
	joint_homed_n_lb, joint_max_soft_limit_n_lb, joint_velocity_n_lb
	joint_homing_n_lb, joint_min_ferror_n_lb, joint_inpos_n_lb,
	joint_min_hard_limit_n_lb,

Special Labels
--------------

Axis machine position labels no offsets

.. csv-table:: Machine Position Status Labels
   :width: 100%
   :align: left

	actual_lb_x, actual_lb_y, actual_lb_z
	actual_lb_a, actual_lb_b, actual_lb_c
	actual_lb_u, actual_lb_v, actual_lb_w


Axis position labels including all offsets

.. csv-table:: DRO Status Labels
   :width: 100%
   :align: left

	dro_lb_x, dro_lb_y, dro_lb_z
	dro_lb_a, dro_lb_b, dro_lb_c
	dro_lb_u, dro_lb_v, dro_lb_w

Offsets for the currently active G5x coordinate system

.. csv-table:: G5x Status Labels
   :width: 100%
   :align: left

	g5x_lb_x, g5x_lb_y, g5x_lb_z
	g5x_lb_a, g5x_lb_b, g5x_lb_c
	g5x_lb_u, g5x_lb_v, g5x_lb_w

Offsets for G92

.. csv-table:: G92 Status Labels
   :width: 100%
   :align: left

	g92_lb_x, g92_lb_y, g92_lb_z
	g92_lb_a, g92_lb_b, g92_lb_c
	g92_lb_u, g92_lb_v, g92_lb_w

Current Tool Offsets

.. csv-table:: Current Tool Status Labels
   :width: 100%
   :align: left

	tool_offset_lb_0, tool_offset_lb_1, tool_offset_lb_2
	tool_offset_lb_3, tool_offset_lb_4, tool_offset_lb_5
	tool_offset_lb_6, tool_offset_lb_7, tool_offset_lb_8

.. note:: see the Controls page for axis numbering

Spindle Status
--------------

The Spindle status contains status items for 9 spindles. Replace the `_n_` with the
number of the spindle. Spindle numbers start at 0 and go through to 8.

.. csv-table:: Spindle Status Labels
   :width: 100%
   :align: left

	spindle_brake_n_lb, spindle_increasing_n_lb, spindle_override_enabled_n_lb
	spindle_direction_n_lb, spindle_orient_fault_n_lb, spindle_speed_n_lb
	spindle_enabled_n_lb, spindle_orient_state_n_lb
	spindle_homed_n_lb, spindle_override_n_lb

I/O Status
----------

The I/O status contains status items for 64 I/O's. Replace the `_n_` with the
number of the joint. Joint numbers start at 0 and go through to 63.

.. csv-table:: I/O Status Labels
   :width: 100%
   :align: left

	ain_n_lb, aout_n_lb, din_n_lb
	dout_n_lb

Tool Table Status
-----------------

The Tool Table status contains status items for all the tools in the tool table.
Replace the `_n_` with the position in the tool table.

.. csv-table:: Tool Table Status Labels
   :width: 100%
   :align: left

	tool_table_id_n_lb, tool_table_xoffset_n_lb, tool_table_yoffset_n_lb
	tool_table_zoffset_n_lb, tool_table_aoffset_n_lb, tool_table_boffset_n_lb
	tool_table_coffset_n_lb, tool_table_uoffset_n_lb, tool_table_voffset_n_lb
	tool_table_woffset_n_lb, tool_table_diameter_n_lb, tool_table_frontangle_n_lb
	tool_table_backangle_n_lb, tool_table_orientation_n_lb



