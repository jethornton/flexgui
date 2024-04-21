Controls
========

Push Buttons
------------

Controls are QPushButtons that can be placed anywhere you like. Use the Name
from the list below for each control widget objectName. Replace `_n` with the
joint number or axis index.
::

	Control                      Name
	Open                         open_pb
	Edit                         edit_pb
	Reload                       reload_pb
	Save As                      save_as_pb
	Quit                         quit_pb
	E-Stop                       estop_pb
	Power                        power_pb
	Run                          run_pb
	Run From Line                run_from_line_pb
	Step                         step_pb
	Pause                        pause_pb
	Resume                       resume_pb
	Stop                         stop_pb
	Home All                     home_all_pb
	Home Joint (1-9)             home_pb_(1-9)
	Unhome All                   unhome_all_pb
	Unhome Joint (1-9)           unhome_pb_(1-9)
	Manual Mode                  manual_mode_pb
	Run MDI                      run_mdi_pb
	Touch Off Axis               touchoff_pb_(axis letter)
	Tool Touch Off               tool_touchoff_(axis letter)
	Jog Plus Axis (1-9)          jog_plus_pb_(1-9)
	Jog Minus Axis (1-9)         jog_minus_pb_(1-9)
	Tool Change                  tool_change_pb
	Spindle Forward              spindle_fwd_pb
	Spindle Reverse              spindle_rev_pb
	Spindle Stop                 spindle_stop_pb
	Spindle Faster               spindle_plus_pb
	Spindle Slower               spindle_minus_pb
	Flood Toggle                 flood_pb
	Mist Toggle                  mist_pb
	Change Coordinate System     change_cs_(1-9)
	Clear Error History          clear_error_history_pb
	Change Coordinate System     change_cs_(1-9) 

.. image:: /images/controls-01.png
   :align: center

.. note:: Touch Off buttons require a Double Spin Box named `touchoff_dsb`
.. note:: Tool Touch Off buttons require a Double Spin Box named `tool_touchoff_dsb`

The following QPushButton controls need checkable set to true.
::

	Flood Toggle                           flood_pb
	Mist Toggle                            mist_pb
	Optional Stop at M1                    optional_stop_pb
	Block Delete line that starts with /   block_delete_pb
	Feed Hold                              feed_hold_pb
	Feed Override Enable/Disable           feed_override_pb

.. image:: /images/checkable-pb.png
   :align: center


Axis Index
----------
::

	X 0
	Y 1
	Z 2 
	A 3
	B 4
	C 5
	U 6
	V 7
	W 8

Sliders
-------

A QSlider is used to control the following functions.
::

	Function              Slider                      Status Label
	Jog Velocity          jog_vel_sl                  jog_vel_lb
	Feed Override         feed_override_sl            feedrate_lb
	Rapid Override        rapid_override_sl           rapid_override_lb
	Spindle Override      spindle_override_sl         spindle_override_0_lb

Spin Boxes
----------
::

	Spindle Speed           spindle_speed_sb

Double Spin Boxes
-----------------
::

	Touch Off Value         touchoff_dsb
	Tool Touch Off Value    tool_touchoff_dsb

.. note:: You don't have to use all the controls, the ones found will be
   connected to the correct code. Some controls might be mandatory.

