Spindle
=======

`Video Tutorial <https://youtu.be/37Sh-lieq9Y>`_

Multiple Spindles
-----------------

Flex GUI can control and display status information about all 8 possible
spindles in LinuxCNC. To configure more than one spindle you must add
SPINDLES = number of spindles to the [TRAJ] section of the INI file.

In addition to the above you must add num_spindles=number of spindles to the
loadrt motmod line in your main hal file.

Optionally to control the spindle minimum, maximum and increments add a
[SPINDLE_n] section to the ini file where `n` is the spindle number 0-7.
for more information see :ref:`SpindleINI`

See the LinuxCNC documents for more information.

Spindle Status
--------------

Spindle status labels show the current status of the item. Linuxcnc can have up
to 8 spindles. The spindles are numbered 0 through 7.

.. csv-table:: Spindle Status Labels
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Spindle Brake, QLabel, spindle_brake_n_lb
	Spindle Direction, QLabel, spindle_direction_n_lb
	Spindle Enabled, QLabel, spindle_enabled_n_lb
	Spindle Override Enabled, QLabel, spindle_override_enabled_n_lb
	Spindle Speed, QLabel, spindle_speed_n_lb
	Spindle Speed LCD, QLCDNumber, spindle_speed_0_lcd
	Spindle Commanded Speed, QLabel, spindle_cmd_speed_n_lb
	Spindle Override Percent, QLabel, spindle_override_n_lb
	Spindle Orient State, QLabel, spindle_orient_state_n_lb
	Spindle Orient Fault, QLabel, spindle_orient_fault_n_lb
	Spindle Speed + Override, QLabel, spindle_speed_n_lb

.. NOTE:: if the object name has _n_ then you can use 0 - 7 to indicate which
   spindle to monitor

.. NOTE:: Spindle Speed does not show override. Spindle Speed + Override
   is commanded speed including override.

.. NOTE:: The digitCount property of the LCD must be large enough to display the
   whole number.

.. NOTE:: To get actual spindle speed you need to connect the spindle encoder to
   an encoder component and use the encoder.N.velocity-rpm float out connected
   to a HAL float label.

On start-up, Flex will check for the following items in the [SPINDLE_n] sections
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

If `MIN_OVERRIDE` is found, it will be used to set the QSlider minimum
setting. If not found, the minimum setting will be 0%.

If `MAX_OVERRIDE` is found, it will set the QSlider maximum setting.
If not found, the maximum setting will be 100%.


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

.. WARNING:: The spindle_override_sl will be replaced by spindle_override_n_sl
   in the next release.

The spindle speed override is set using a QSlider. The spindles are numbered
0-7 so replace the `n` with the number of the spindle you want to override.

See the Status Labels above for spindle override status labels.

.. csv-table:: Multi Spindle Override
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Spindle Override, QSlider, spindle_override_n_sl



