Controls
========

Push Buttons
------------

Controls are QPushButtons that can be placed anywhere you like. Use the Name
from the list below for each control widget objectName. Replace `_n` with the
joint number or axis index.
::

	Control              Name
	Open                 open_pb
	Edit                 edit_pb
	Reload               reload_pb
	Save As              save_as_pb
	Quit                 quit_pb
	E-Stop               estop_pb
	Power                power_pb
	Run                  run_pb
	Run From Line        run_from_line_pb
	Step                 step_pb
	Pause                pause_pb
	Resume               resume_pb
	Stop                 stop_pb
	Home All             home_all_pb
	Home Joint n         home_pb_n
	Unhome All           unhome_all_pb
	Unhome Joint n       unhome_pb_n
	Manual Mode          manual_mode_pb
	Run MDI              run_mdi_pb
	Touch Off Axis       touchoff_pb_(axis letter)
	Tool Touch Off       tool_touchoff_(axis letter)
	Jog Plus Axis n      jog_plus_pb_n
	Jog Minus Axis n     jog_minus_pb_n
	Tool Change          tool_change_pb
	Spindle Forward      spindle_fwd_pb
	Spindle Reverse      spindle_rev_pb
	Spindle Stop         spindle_stop_pb
	Spindle Faster       spindle_plus_pb
	Spindle Slower       spindle_minus_pb
	Flood Toggle         flood_pb
	Mist Toggle          mist_pb
	Clear MDI History    clear_mdi_history_pb
	Copy MDI History     copy_mdi_history_pb
	Clear Error History  clear_error_history_pb

.. image:: /images/controls-01.png
   :align: center

.. note:: Touch Off buttons require a Double Spin Box named `touchoff_dsb`
.. note:: Tool Touch Off buttons require a Double Spin Box named `tool_touchoff_dsb`

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

	Jog Velocity          jog_vel_sl
	Feed Override         feed_override_sl
	Rapid Override        rapid_override_sl
	Spindle Override      spindle_override_sl
	Jog Speed             jog_speed_sl

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

