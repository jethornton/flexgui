=======
Spindle
=======

`Video Tutorial <https://youtu.be/37Sh-lieq9Y>`_

Multiple Spindles
-----------------

Flex GUI can control and display status information for all 8 spindles in
LinuxCNC. To configure more than one spindle you must add SPINDLES = 1 to 8 to
the [TRAJ] section of the INI file.

In addition to the above you must add num_spindles=1 to 8 to the loadrt motmod
line in your main hal file.

Optionally to control the spindle minimum RPM, maximum RPM, plus/minus
increments and default RPM add a [SPINDLE_n] section to the ini file where `n`
is the spindle number 0-7.

For more information see :ref:`Spindle INI Section <spindle_n>`

See the LinuxCNC documents for more information about multiple spindles.

Spindle Status
--------------

Spindle status labels show the current status of the item. Linuxcnc can have up
to 8 spindles. The spindles are numbered 0 through 7. If you have a single
spindle it is spindle 0.

.. csv-table:: **Spindle Status Labels**
   :width: 100%
   :align: center
   :widths: 35 30 35

	**Control Function**, **Object Type**, **Object Name**
	Spindle Brake, QLabel, spindle_brake_n_lb
	Spindle Direction, QLabel, spindle_direction_n_lb
	Spindle Enabled, QLabel, spindle_enabled_n_lb
	Spindle Override Enabled, QLabel, spindle_override_enabled_n_lb
	Spindle Speed, QLabel, spindle_speed_n_lb
	Spindle Speed LCD, QLCDNumber, spindle_speed_n_lcd
	Spindle Commanded Speed, QLabel, spindle_cmd_speed_n_lb
	Spindle Override Percent, QLabel, spindle_override_n_lb
	Spindle Orient State, QLabel, spindle_orient_state_n_lb
	Spindle Orient Fault, QLabel, spindle_orient_fault_n_lb

.. NOTE:: Replace the `n` with 0 - 7 to indicate which spindle to monitor

.. NOTE:: Spindle Speed does not show override. Spindle Commanded Speed is
   commanded speed including override.

.. NOTE:: The digitCount property of the LCD must be large enough to display the
   whole number.

.. NOTE:: To get actual spindle speed you need to connect the spindle encoder to
   an encoder component and use the encoder.n.velocity-rpm float out connected
   to a HAL float label.

Spindle Controls
----------------

The following items control the spindle on/off direction and speed

.. csv-table:: **Spindle Status Labels**
   :width: 100%
   :align: center
   :widths: 30 30 40

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

.. csv-table:: **Multi Spindle Override**
   :width: 100%
   :align: center
   :widths: 30 30 40

	**Control Function**, **Object Type**, **Object Name**
	Spindle Override, QSlider, spindle_override_n_sl

The spindle speed override is set using a QSlider. The spindles are numbered
0-7 so replace the `n` with the number of the spindle you want to override.

See the Status Labels above for spindle override status labels.



