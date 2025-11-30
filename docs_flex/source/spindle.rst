Spindle
=======

`Video Tutorial <https://youtu.be/37Sh-lieq9Y>`_

Spindle Status
--------------

Spindle status labels show the current status of the item.

.. csv-table:: Spindle Status Labels
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Spindle Brake, QLabel, spindle_brake_0_lb
	Spindle Direction, QLabel, spindle_direction_0_lb
	Spindle Enabled, QLabel, spindle_enabled_0_lb
	Spindle Override Enabled, QLabel, spindle_override_enabled_0_lb
	Spindle Commanded Speed, QLabel, spindle_speed_0_lb
	Spindle Speed LCD, QLCDNumber, spindle_speed_0_lcd
	Spindle Override Percent, QLabel, spindle_override_0_lb
	Spindle Homed, QLabel, spindle_homed_0_lb
	Spindle Orient State, QLabel, spindle_orient_state_0_lb
	Spindle Orient Fault, QLabel, spindle_orient_fault_0_lb
	Current S word Setting, QLabel, settings_speed_lb
	Spindle Actual Speed, QLabel, spindle_actual_speed_lb
	Spindle Speed Setting, QLabel, spindle_speed_setting_lb

.. note:: Spindle Commanded Speed does not show override. Spindle Actual Speed
   is actual commanded speed including override.

.. note:: The digitCount property of the LCD must be large enough to display the
   whole number.

.. NOTE:: To get actual spindle speed you need to connect the spindle encoder to
   an encoder component and use the encoder.N.velocity-rpm float out connected
   to a HAL float label.

On start-up, Flex will check for the following items in the [SPINDLE_0] section
of the .ini file

If `INCREMENT` is not found, Flex will look in the .ini [DISPLAY] section for
`SPINDLE_INCREMENT` and if not there will default the increment to 10 for
spindle faster/slower control buttons and spindle step for the QSpinBox.

If `MIN_FORWARD_VELOCITY` is found, it will be used to set the QSpinBox minimum
setting. If not found, the minimum setting will be 0.

If `MAX_FORWARD_VELOCITY` is found, it will set the QSpinBox maximum setting.
If not found, the maximum setting will be 1000.

`INCREMENT` will also set the QSpinBox single step when using the up/down
arrows.

Spindle Controls
----------------

The following items control the spindle on/off direction and speed

.. csv-table:: Spindle Status Labels
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Spindle Forward, QPushButton, spindle_fwd_pb
	Spindle Reverse, QPushButton, spindle_rev_pb
	Spindle Stop, QPushButton, spindle_stop_pb
	Spindle Faster, QPushButton, spindle_plus_pb
	Spindle Slower, QPushButton, spindle_minus_pb
	Spindle Speed, QSpinBox, spindle_speed_sb

.. note:: The spindle can not be started with a spindle speed of zero.

Spindle Overrides
-----------------

The spindle speed override is set using a QSlider. See the Status Labels above
for spindle override status labels.

.. csv-table:: Spindle Override
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Spindle Override, QSlider, spindle_override_sl

