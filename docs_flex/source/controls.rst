Controls
========
`Command Buttons Tutorial <https://youtu.be/X_SMoJ9sYbI>`_
`Home Controls Tutorial <https://youtu.be/R8Z_oCdaAXM>`_

Push Buttons
------------

Controls are QPushButtons that can be placed anywhere you like. Use the Name
from the list below for each control widget objectName. Replace the `(0-8)`
with the joint number or axis index. More controls are in :doc:`tools`.

.. csv-table:: Control Push Buttons
   :width: 100%
   :align: center

	**Control Function**, **Object Name**
	Open a G-code File, open_pb
	Edit a G-code File, edit_pb
	Reload a G-code File, reload_pb
	Edit Tool Table, edit_tool_table_pb
	Edit Ladder, edit_ladder_pb
	Reload Tool Table, reload_tool_table_pb
	Save As a New Name, save_as_pb
	Quit the Program, quit_pb
	E-Stop Toggle, estop_pb
	Power Toggle, power_pb
	Run a Loaded G-code File, run_pb
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
	Help About, about_pb
	Quick Reference, quick_reference_pb

.. note:: You don't have to use any of these controls; Flex GUI is flexible.

.. image:: /images/controls-01.png
   :align: center

.. note:: Touch-Off buttons require a Double Spin Box named `touchoff_dsb`

.. note:: Tool-Touch-Off buttons require a Double Spin Box named
   `tool_touchoff_dsb`

Touch-Off Spin Boxes
--------------------
::

	Touch Off Value         touchoff_dsb
	Tool Touch Off Value    tool_touchoff_dsb

E Stop and Power
----------------

The E Stop push button Open/Closed state text can be set by adding two string
type Dynamic Properties `open_text` and `closed_text`. The text in those two
properties will be used if found. See :doc:`property`

.. image:: /images/estop-01.png
   :align: center

The Power push button On/Off state text can be set by adding two string type
Dynamic Properties `on_text` and `off_text`. The text in those two properties
will be used if found. The default text is `Power Off` and
`Power On`.

.. image:: /images/power-01.png
   :align: center

.. note:: To have two words be above and below insert a \n between the words.

.. image:: /images/estop-02.png
   :align: center

This is how the above looks in the GUI

.. image:: /images/estop-03.png
   :align: center

.. _led_buttons:

LED Buttons
-----------

.. important:: This is a work in progress and will be fully implmented by
   version 1.2.0. Prior to that some control buttons may not change LED states.

Some push buttons can have a LED to indicate on and off states. The LED is added
to the push button with a Bool type Dynamic Property called `led_indicator`.

.. csv-table:: LED Buttons
   :width: 100%
   :align: center

	**Control Name**, **Object Name**, **Function**
	E Stop, estop_pb, E Stop Toggle Button
	Power, power_pb, Power Toggle Button
	Run, run_pb, Runs a loaded NC file
	Pause, pause_pb, Pauses a running NC file
	Manual Mode, manual_mode_pb, Puts the control into Manual Mode
	MDI Mode, mdi_mode_pb, Puts the control into MDI Mode
	Flood, flood_pb, Turns on the flood cooland
	Mist, mist_pb, Turns on the mist coolant
	Probe Enable, probing_enable_pb, Enables Probing and disables other controls

Adding the Bool type Dynamic Property `led_indicator` to one of the above
control buttons will add the default LED to that button. Each control button can
have different options.

.. csv-table:: LED Button Dynamic Properties
   :width: 100%
   :align: center

	**Property Name**, **Type**, **Function**
	led_indicator, Bool, Creates a LED
	led_diameter, Int, Sets the Diameter of the LED in pixels
	led_right_offset, Int, Sets the offset from the right edge in pixels
	led_top_offset, Int, Sets the offsset from the top edge in pixels
	led_on_color, Color, Sets the color of the LED when on
	led_off_color, Color, Sets the color of the LED when off


To change the LED default options they can be set in the INI file.
See :ref:`led_defaults`

.. tip:: A space after the button text gives more room for the LED

Coordinate System Controls
--------------------------

A QPushButton can be used to clear the curren cooridnate system by using 0 as
the index or any one of the 9 coordinate systems with (1-9).

To clear the G92 coordinate system use 10 as the index.

.. csv-table:: Coordinate System Buttons
   :width: 100%
   :align: center

	**Control Function**, **Object Name**
	Clear Current G5x, clear_coord_0
	Clear G5x Coordinate System, clear_coord_(1-9)
	Clear G92 Coordinate System, clear_coord_10

Options
-------

The QPushButton options are toggle-type buttons; press to turn on, press again
to turn off. They are normal push buttons but Flex automatically makes them
`checkable`.

.. csv-table:: Options
   :width: 100%
   :align: left

	**Function**, **Widget**, **Name**
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
`Jog Controls Tutorial <https://youtu.be/ReVeEB5tEYM>`_

Jogging requires a `Jog Velocity Slider` and `Jog Mode Selector`. If either
is not found, Jog Buttons will be disabled.

.. csv-table:: Jog Widgets
   :width: 100%
   :align: left

	**Function**, **Widget**, **Name**
	Jog Plus Axis (0-8), QPushButton,jog_plus_pb_(0-8)
	Jog Minus Axis (0-8), QPushButton, jog_minus_pb_(0-8)
	Jog Velocity Slider, QSlider, jog_vel_sl
	Jog Velocity Label, QLabel, jog_vel_lb
	Jog Mode Selector, QComboBox, jog_modes_cb

.. note:: Jog Plus/Minus buttons use the `Axis Index`_. So `Jog Y Plus` is
   `jog_plus_pb_1`.

.. note:: `Jog Mode Selector` reads the ini entry [DISPLAY] INCREMENTS and if
   not found, only `Continuous` will be an option.

.. warning:: [DISPLAY] INCREMENTS must be a comma seperated list or it will be
   ignored.

The following settings can be used in the DISPLAY section of the ini file:
::

	INCREMENTS = 0.100, 0.010, 0.001
	INCREMENTS = 1 inch, 0.5 in, 1 cm, 1 mm
	MIN_LINEAR_VELOCITY = 0.1
	MAX_LINEAR_VELOCITY = 1.0
	DEFAULT_LINEAR_VELOCITY = 0.2

.. note:: Jog incremnts can have unit lables, the following are valid unit
   labels cm, mm, um, inch, in or mil. If no unit labels are found the the
   configuration units are used.

Overrides
---------
`Overrides Tutorial <https://youtu.be/taAtYf3ebDE>`_

A QSlider is used to control the following functions and the corresponding 
label shows the value of the slider:

.. csv-table:: Overrides
   :width: 100%
   :align: left

	**Function**, **Widget**, **Object Name**
	Feed Override Slider, QSlider, feed_override_sl
	Feed Override Percent, QLabel, feed_override_lb
	Rapid Override Slider, QSlider, rapid_override_sl
	Rapid Override Percent, QLabel, rapid_override_lb
	Spindle Override Slider, QSlider, spindle_override_sl
	Spindle Override Percent, QLabel, spindle_override_0_lb
	Override Limits, QCheckBox, override_limits_cb

The following settings can be used in the DISPLAY section of the ini file:
::

	Feed Override maximum             MAX_FEED_OVERRIDE
	Spindle Override maximum          MAX_SPINDLE_OVERRIDE

Override Presets
----------------

Feed, Rapid and Spindle overrides can have a preset button(s) for different
preset amounts. Replace the nnn with the percent of override you want that
button to use.

.. csv-table:: Override Presets
   :width: 100%
   :align: left

	**Function**, **Widget**, **Object Name**
	Feed Override Preset, QPushButton, feed_percent_nnn
	Rapid Override Preset, QPushButton, rapid_percent_nnn
	Spindle Override Preset, QPushButton, spindle_percent_nnn

.. note:: The maximum override for Rapid is 100

Stacked Widget
--------------

To change to a specific page on a QStackedWidget add a QPushButton on each page
and set a couple of Dynamic Properties. See :doc:`property`

.. csv-table:: Stacked Widget Change Page
   :width: 100%
   :align: left

	**Dynamic Property Name**, **Value**
	change_page, QStackedWidget Object Name
	index, index of page to change to

.. image:: /images/stacked-01.png
   :align: center

To create a Next Page and Previous Page buttons for a QStackedWidget add two
QPushButtons with the following Dynamic Properties. See :doc:`property`

.. csv-table:: Stacked Widget Next/Previous Page
   :width: 100%
   :align: left

	**Button Function**, **Dynamic Property Name**, **Value**
	Next Page, next_page, QStackedWidget Object Name
	Previous Page, previous_page, QStackedWidget Object Name

.. note:: The Forward and Backward Buttons should not be in the QStackedWidget


