Status Labels
=============

Use the Name from the list below for the objectName for each label widget.
::

	Label                    Name
	Machine Status           status_lb
	Command State            state_lb
	G code File              file_lb
	X Axis DRO               dro_lb_x
	Y Axis DRO               dro_lb_y
	Z Axis DRO               dro_lb_z
	Current Motion Line      motion_line_lb
	Start From Line          start_line_lb
	Min Jog Velocity         min_jog_vel_lb
	Max Jog Velocity         max_jog_vel_lb
	Current Jog Velocity     jog_vel_lb
	Current G codes          g_codes_lb
	Current M codes          m_codes_lb
	Current G5x Offsets      g5x_offsets_lb
	Current G92 Offsets      g92_offsets_lb
	Interperter State        interp_state_lb
	Task State               task_state_lb
	Current Tool in Spindle  tool_lb
	Jog Units                jog_units_lb

.. note:: You don't have to use all the labels, the ones found will be
  updated to the correct status


acceleration_lb
active_queue_lb
adaptive_feed_enabled_lb
angular_units_lb
axis_mask_lb
block_delete_lb
call_level_lb
command_lb
current_line_lb
current_vel_lb
cycle_time_lb
debug_lb
delay_left_lb
distance_to_go_lb
echo_serial_number_lb
enabled_lb
estop_lb
exec_state_lb
feed_hold_enabled_lb
feed_override_enabled_lb
feedrate_lb
file_lb
flood_lb
g5x_index_lb
id_lb
ini_filename_lb
inpos_lb
input_timeout_lb
interp_state_lb
interpreter_errcode_lb
joints_lb
kinematics_type_lb
linear_units_lb
lube_lb
lube_level_lb
max_acceleration_lb
max_velocity_lb
mist_lb
motion_line_lb
motion_mode_lb
motion_type_lb
optional_stop_lb
paused_lb
pocket_prepped_lb
probe_tripped_lb
probe_val_lb
probed_position_lb
probing_lb
program_units_lb
queue_lb
queue_full_lb
rapidrate_lb
read_line_lb
rotation_xy_lb
settings_lb
spindles_lb
state_lb
task_mode_lb
task_paused_lb
task_state_lb
tool_in_spindle_lb
tool_from_pocket_lb
tool_offset_lb
velocity_lb

all active g codes
gcodes_lb

all active m codes
mcodes_lb

tuple of 64 items
ain_lb
aout_lb
din_lb
dout_lb

tuple of axes
axis_lb

tuple of joints
joint_lb

tuple of spindles
spindle_lb

tuple of tool table
 id, xoffset, yoffset, zoffset, aoffset, boffset, coffset, uoffset, voffset, woffset, diameter, frontangle, backangle, orientation
tool_table_lb
