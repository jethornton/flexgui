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
	Save, save_pb
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
	Clear an Axis Offset, clear_(axis letter)_pb
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

.. note:: To have two words be above and below insert a backslasgh and n between the words.

.. image:: /images/estop-02.png
   :align: center

This is how the above looks in the GUI

.. image:: /images/estop-03.png
   :align: center

.. _led_buttons:

LED Buttons
-----------

.. important:: This is implmented in version 1.2.0.

Some push buttons can have a LED to indicate on and off states. The LED is added
to the push button with a Bool type Dynamic Property called `led_indicator`. All
other properties are optional.

.. csv-table:: LED Buttons
   :width: 100%
   :align: center

	**Control Name**, **Object Name**, **Function**
	Save, save_pb, NC Code Save Button
	Reload, reload_pb, Reload NC Code from current file
	E Stop, estop_pb, E Stop Toggle Button
	Power, power_pb, Power Toggle Button
	Run, run_pb, Runs a loaded NC file
	Pause, pause_pb, Pauses a running NC file
	Manual Mode, manual_mode_pb, Puts the control into Manual Mode
	MDI Mode, mdi_mode_pb, Puts the control into MDI Mode
	Flood, flood_pb, Turns on the flood coolant
	Mist, mist_pb, Turns on the mist coolant
	Probe Enable, probing_enable_pb, Enables Probing and disables other controls

Adding the Bool type Dynamic Property `led_indicator` to one of the above
control buttons will add the default LED to that button. Each control button can
have different options. If On/Off colors are not specified then Red will be Off
and Green will be On.

.. csv-table:: LED Button Dynamic Properties
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Function**
	Bool, led_indicator, Creates a LED
	Int, led_diameter, Sets the Diameter of the LED in pixels
	Int, led_right_offset, Sets the offset from the right edge in pixels
	Int, led_top_offset, Sets the offset from the top edge in pixels
	Color, led_on_color, Sets the color of the LED when on
	Color, led_off_color, Sets the color of the LED when off

To change the LED default options they can be set in the INI file.
See :ref:`led_defaults`

.. tip:: A space after the button text gives more room for the LED

Coordinate System Controls
--------------------------

A QPushButton can be used to clear the current coordinate system by using 0 as
the index or any one of the 9 coordinate systems with (1-9).

To clear the G92 coordinate system use 10 as the index.

To clear the current G54x coordinate system rotation use 11 as the index.

.. csv-table:: Clear Coordinate System Offsets
   :width: 100%
   :align: center

	**Control Function**, **Object Name**
	Clear Current G5x, clear_coord_0
	Clear G5x Coordinate System, clear_coord_(1-9)
	Clear G92 Coordinate System, clear_coord_10
	Clear Current G5x Rotation clear_coord_11

To clear an axis offset in the current G5x coordinate system use the following.

.. csv-table:: Clear Axis Offsets
   :width: 100%
   :align: center

	**Control Function**, **Object Name**
	Clear Current G5x X axis, clear_(axis letter)_pb

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

Jogging
=======

Jogging requires a `Jog Velocity Slider` and `Jog Mode Selector`. If either
is not found, Jogging will be disabled.

Jogging increments are from the ini entry `INCREMENTS` in the [DISPLAY] section.
See :ref:`Jog Increments <jog-increments>` for more information.

.. csv-table:: Required Jog Widgets
   :width: 100%
   :align: left

	**Function**, **Widget**, **Name**
	Jog Velocity Slider, QSlider, jog_vel_sl
	Jog Mode Selector, QComboBox, jog_modes_cb

The Jog Velocity Label shows the current jog velocity setting from the Jog
Velocity Slider

.. csv-table:: Optional Jog Widgets
   :width: 100%
   :align: left

	**Function**, **Widget**, **Name**
	Jog Velocity Label, QLabel, jog_vel_lb

Keyboard Jogging
----------------

To enable keyboard jogging a QCheckbox is used. When checked the right/left
arrow keys jog the X axis and the up/down arrow keys jog the Y axis and the
page up/down keys jog the Z axis. When not checked the keys function as normal
keys.

.. csv-table:: Keyboard Jogging
   :width: 100%
   :align: left

	**Function**, **Widget**, **Name**
	Jog Enable, QCheckBox, keyboard_jog_cb


Jog Button Controls
-------------------
`Jog Controls Tutorial <https://youtu.be/ReVeEB5tEYM>`_


This type of jog controls provides a button for each axis and jog direction.

.. csv-table:: Jog Button Widgets
   :width: 100%
   :align: left

	**Function**, **Widget**, **Name**
	Jog Plus Axis (0-8), QPushButton, jog_plus_pb_(0-8)
	Jog Minus Axis (0-8), QPushButton, jog_minus_pb_(0-8)

.. note:: Jog Plus/Minus buttons use the `Axis Index`_. So `Jog Y Plus` is
   `jog_plus_pb_1`.

.. note:: `Jog Mode Selector` reads the ini entry [DISPLAY] INCREMENTS and if
   not found, only `Continuous` will be an option.

Jog Selected Axis Controls
--------------------------

To add Axis style jog controls where you select an axis then the plus/minus
buttons jog the selected axis add a QRadioButton for each axis and a QPushButton
for Plus and Minus. Axes are 0-8 for X, Y, Z, A, B, C, U, V, W.

.. csv-table:: Jog Selected Widgets
   :width: 100%
   :align: left

	**Function**, **Widget**, **Name**
	Axis Select (0-8), QRadioButton, axis_select_(0-8)
	Jog Plus, QPushButton, jog_selected_plus
	Jog Minus, QPushButton, jog_selected_minus

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
	Maximum Velocity, QSlider, max_vel_sl
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

File Load Buttons
-----------------
To create a QPushButton to load a specific file add two Dynamic Properties.

.. csv-table:: File Load Buttons
   :width: 100%
   :align: left

	**Dynamic Property Name**, **Value**
	function, load_file
	filename, file to load

File Name in the PROGRAM_PREFIX path.

.. image:: /images/controls-02.png
   :align: center

File Name with Full Path

.. image:: /images/controls-03.png
   :align: center

File Name in the Configuration Directory

.. image:: /images/controls-04.png
   :align: center

File Name relative to the Users Home Directory

.. image:: /images/controls-05.png
   :align: center


The file name can be just the name and extension if it's in the PROGRAM_PREFIX
path. Or it can be any valid path and file name.

File Name Examples
::

	A file in the PROGRAM_PREFIX path
	somefile.ngc

	A file in the configuration directory
	./anotherfile.ngc

	A file up one directory from the configuration directory
	../up_one.ngc

	A file relative to the users home directory
	/home/fred/linuxcnc/my_files/afile.ngc
	could be 
	~/linuxcnc/my_files/afile.ngc

.. warning:: The file must be in the directory specified by the INI entry
   PROGRAM_PREFIX in the [DISPLAY] section or have a valid path.

This is useful for probe routine buttons to load the nc code so the
path can be viewed in the plotter and for programs that are ran frequently.

.. note:: The file is not added to the Recent Files list.
