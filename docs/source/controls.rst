Controls
========

Push Buttons
------------

Controls are QPushButtons that can be placed anywhere you like. Use the Name
from the list below for each control widget objectName. Replace the `(0-8)` with
the joint number or axis index. More controls are in :doc:`tools`

.. csv-table:: Control Push Buttons
   :width: 80%
   :align: center

	Control Function, Object Name
	Open a G code File, open_pb
	Edit a G code File, edit_pb
	Reload a G code File, reload_pb
	Edit Tool Table, edit_tool_table_pb
	Edit Ladder, edit_ladder_pb
	Reload Tool Table, reload_tool_table_pb
	Save As a New Name, save_as_pb
	Quit the Program, quit_pb
	E-Stop Toggle, estop_pb
	Power Toggle, power_pb
	Run a Loaded G code File, run_pb
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
	Clear Error History, clear_error_history_pb
	Show HAL, show_hal_pb
	HAL Meter, hal_meter_pb
	HAL Scope, hal_scope_pb

.. image:: /images/controls-01.png
   :align: center

.. note:: Touch Off buttons require a Double Spin Box named `touchoff_dsb`

.. note:: Tool Touch Off buttons require a Double Spin Box named `tool_touchoff_dsb`

Options
-------

These buttons are toggle type buttons press to turn on press again to turn off.
They are normal push buttons but in code they are set to checkable
::

	Flood Toggle                           flood_pb
	Mist Toggle                            mist_pb
	Optional Stop at M1                    optional_stop_pb
	Block Delete line that starts with /   block_delete_pb
	Feed Override Enable/Disable           feed_override_pb

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

Jogging requires the Jog Velocity Slider and Jog Mode Selector. If either is not
found any Jog Buttons will be disabled.

.. csv-table:: Jog Widgets
   :width: 100%
   :align: left

	Function, Widget, Name
	Jog Plus Axis (0-8), QPushButton,jog_plus_pb_(0-8)
	Jog Minus Axis (0-8), QPushButton, jog_minus_pb_(0-8)
	Jog Velocity Slider, QSlider, jog_vel_sl
	Jog Velocity Label, QLabel, jog_vel_lb
	Jog Mode Selector, QComboBox, jog_modes_cb

.. note:: Jog Plus/Minus buttons use the `Axis Index`_ Jog Y Plus is jog_plus_pb_1

.. note:: Jog Mode Selector reads the ini entry [DISPLAY] INCREMENTS and if not
   found only Continuous will show up as an option

The following settings are from the DISPLAY section of the ini file if found.
::

	Jog Velocity minimum              MIN_LINEAR_VELOCITY
	Jog Velocity maximum              MAX_LINEAR_VELOCITY
	Jog Velocity default              DEFAULT_LINEAR_VELOCITY


Overrides
---------

A QSlider is used to control the following functions and the corresponding label
shows the value of the slider.
::

	Function              QSlider                     QLabel
	Feed Override         feed_override_sl            feedrate_lb
	Rapid Override        rapid_override_sl           rapid_override_lb
	Spindle Override      spindle_override_sl         spindle_override_0_lb

The following settings are from the DISPLAY section of the ini file if found.
::

	Feed Override maximum             MAX_FEED_OVERRIDE
	Spindle Override maximum          MAX_SPINDLE_OVERRIDE

Double Spin Boxes
-----------------
::

	Touch Off Value         touchoff_dsb
	Tool Touch Off Value    tool_touchoff_dsb

.. note:: You don't have to use all the controls, the ones found will be
   connected to the correct code. Nothing is mandatory to use it's Flexible.

