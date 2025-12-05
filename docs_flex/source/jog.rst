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

Keyboard jogging uses the following keys to jog the X, Y and Z axes.

* Right Arrow jogs the X axis in the positive direction
* Left Arrow jogs the X axis in the negative direction
* Up Arrow jogs the Y axis in the positive direction
* Down Arrow jogs the Y axis in the negative direction
* Page Up jogs the Z axis in the positive direction
* Page Down jogs the Z axis in the negative direction

Keyboard jogging can jog more than one axis at the same time.

There are three ways to enable keyboard jogging, the recommended way is to add the
following to the ini file.

.. code-block:: text

	[FLEXGUI]
	KEYBOARD_JOG = True

When keyboard jogging is enabled in this manner either Ctrl key must be pressed
before pressing one of the jog keys. If you release the Ctrl key all axes will
stop jogging.

.. note:: This method is recommended because keyboard jogging is kept separate
   from keyboard navigation of the GUI by use of the CTRL key.

The second way to enable keyboard jogging is to add a QCheckBox to turn keyboard
jog on and off. Currently the jog keys work all the time when the QCheckBox is
checked.

.. csv-table:: Keyboard Jogging
   :width: 100%
   :align: left

	**Function**, **Widget**, **Name**
	Jog Enable, QCheckBox, keyboard_jog_cb

.. note:: In this mode, the jog controls will respond to the use of the arrow 
   keys, even when navigating within text entry controls.  Care must be taken
   to prevent inadvertent jogging by accedentially using the arrow keys with 
   the intent of moving the text cursor. 

The third way to enable jeyboard jogging is similar to the previous case.  This
mode, however, attempts to manage the keyboard focus in the GUI to prevent
conflicts between jogging and text manipulation.

.. code html::

	[FLEXGUI]
	KEYBOARD_JOG = Auto

.. note:: This jog mode will temporarily disable keyboard jogging when a
   text entry widget has focus, and will re-enable keyboard jogging when 
   focus leaves the control.  Qt5 has various "focus policies" and options
   for navigating the GUI using the keyboard.  Be sure that you understand
   how these options interact with one another and test your GUI's 
   configuration appropriately. 

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

Axis Index
----------

.. code-block:: text

	X 0
	Y 1
	Z 2 
	A 3
	B 4
	C 5
	U 6
	V 7
	W 8

