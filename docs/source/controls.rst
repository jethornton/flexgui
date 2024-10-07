Controls
========

Push Buttons
------------

Controls are QPushButtons that can be placed anywhere you like. Use the Name from the list below for each control widget objectName. Replace the `(0-8)` with the joint number or axis index. More controls are in :doc:`tools`.

.. csv-table:: Control Push Buttons
   :width: 80%
   :align: center

	Control Function, Object Name
	Open a GCODE File, open_pb
	Edit a GCODE File, edit_pb
	Reload a GCODE File, reload_pb
	Edit Tool Table, edit_tool_table_pb
	Edit Ladder, edit_ladder_pb
	Reload Tool Table, reload_tool_table_pb
	Save As a New Name, save_as_pb
	Quit the Program, quit_pb
	E-Stop Toggle, estop_pb
	Power Toggle, power_pb
	Run a Loaded GCODE File, run_pb
	Run From Line, run_from_line_pb
	Step one Logical Line, step_pb
	Pause a Running Program, pause_pb
	Resume a Paused Program, resume_pb
	Stop a Running Program, stop_pb
	Home All Joints, home_all_pb
	Home a Joint (0-8), home_pb_(0-8)
	Unhome All Joints, unhome_all_pb
	Unhome a Joint (0-8), unhome_pb_(0-8)
	Zero an Axis, zero_(axis letter)_pb
	Manual Mode, manual_mode_pb
	Flood Toggle, flood_pb
	Mist Toggle, mist_pb
	Clear Error History, clear_errors_pb
	Copy Error History, copy_errors_pb
	Clear Information History, clear_info_pb
	Show HAL, show_hal_pb
	HAL Meter, hal_meter_pb
	HAL Scope, hal_scope_pb

.. image:: /images/controls-01.png
   :align: center

.. note:: Touch-Off buttons require a Double Spin Box named `touchoff_dsb`

.. note:: Tool-Touch-Off buttons require a Double Spin Box named `tool_touchoff_dsb`


Options
-------

The QPushButton options are toggle-type buttons; press to turn on, press again to turn off.  They are normal push buttons but in code they are set to `checkable`.

.. csv-table:: Options
   :width: 100%
   :align: left

	Function, Widget, Name
	Flood Toggle, QPushButton, flood_pb
	Mist Toggle, QPushButton, mist_pb
	Optional Stop at M1, QPushButton, optional_stop_pb
	Block Delete line that starts with /, QPushButton, block_delete_pb
	Feed Override Enable/Disable, QPushButton, feed_override_pb


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


Jog Controls
------------

Jogging requires a `Jog Velocity Slider` and `Jog Mode Selector`.  If either is not found, Jog Buttons will be disabled.

.. csv-table:: Jog Widgets
   :width: 100%
   :align: left

	Function, Widget, Name
	Jog Plus Axis (0-8), QPushButton,jog_plus_pb_(0-8)
	Jog Minus Axis (0-8), QPushButton, jog_minus_pb_(0-8)
	Jog Velocity Slider, QSlider, jog_vel_sl
	Jog Velocity Label, QLabel, jog_vel_lb
	Jog Mode Selector, QComboBox, jog_modes_cb

.. note:: Jog Plus/Minus buttons use the `Axis Index`_. So `Jog Y Plus` is `jog_plus_pb_1`.

.. note:: `Jog Mode Selector` reads the ini entry [DISPLAY] INCREMENTS and if not found, only `Continuous` will be an option.

.. warning:: [DISPLAY] INCREMENTS must be a comma seperated list or it will be ignored.  

The following settings can be used in the DISPLAY section of the ini file:
::

	Jog Velocity minimum              MIN_LINEAR_VELOCITY
	Jog Velocity maximum              MAX_LINEAR_VELOCITY
	Jog Velocity default              DEFAULT_LINEAR_VELOCITY


Overrides
---------

A QSlider is used to control the following functions and the corresponding label shows the value of the slider:

.. csv-table:: Overrides
   :width: 100%
   :align: left

	Function, Widget, Object Name
	Feed Override Slider, QSlider, feed_override_sl
	Feed Override Percent, QLabel, feedrate_lb
	Rapid Override Slider, QSlider, rapid_override_sl
	Rapid Override Percent, QLabel, rapid_override_lb
	Spindle Override Slider, QSlider, spindle_override_sl
	Spindle Override Percent, QLabel, spindle_override_0_lb
	Override Limits, QCheckBox, override_limits_cb

The following settings can be used in the DISPLAY section of the ini file:
::

	Feed Override maximum             MAX_FEED_OVERRIDE
	Spindle Override maximum          MAX_SPINDLE_OVERRIDE


Double Spin Boxes
-----------------
::

	Touch Off Value         touchoff_dsb
	Tool Touch Off Value    tool_touchoff_dsb

.. note:: You don't have to use any of these controls; Flex GUI is flexible.

