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
spindle it is spindle 0. Replace the `s` in the Object Name with the spindle
number you want to monitor.

.. csv-table:: **Spindle Status Labels**
   :width: 100%
   :align: center
   :widths: 35 30 35

	**Control Function**, **Object Type**, **Object Name**
	Spindle Brake, QLabel, spindle_brake_s_lb
	Spindle Direction, QLabel, spindle_direction_s_lb
	Spindle Enabled, QLabel, spindle_enabled_s_lb
	Spindle Override Enabled, QLabel, spindle_override_enabled_s_lb
	Spindle Speed, QLabel, spindle_speed_s_lb
	Spindle Speed LCD, QLCDNumber, spindle_speed_s_lcd
	Spindle Commanded Speed, QLabel, spindle_cmd_speed_s_lb
	Spindle Override Percent, QLabel, spindle_override_s_lb
	Spindle Orient State, QLabel, spindle_orient_state_s_lb
	Spindle Orient Fault, QLabel, spindle_orient_fault_s_lb

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

The following items control the spindle on/off direction and speed for a single
spindle configuration. There are two ways to control the spindle speed, using a
QSpinBox or a QSlider. You can have both the QSpinBox and the QSlider and
changing one will update the other. The QSpinBox up/down arrow keys will change
the value by the `INCREMENT` setting in the [SPINDLE_0] section down to the
`MIN_RPM` and up to the `MAX_RPM`.

.. csv-table:: **Single Spindle Controls**
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
	Spindle Speed, QSlider, spindle_speed_sl

.. note:: The spindle can not be started with a spindle speed of zero.

The following items are manual spindle control each spindle up to 8 spindles.
The spindles are numbered 0-7 with the default spindle being 0. Replace the `s`
in the Object Name with the spindle number you want to control.

.. csv-table:: **Multiple Spindle Controls**
   :width: 100%
   :align: center
   :widths: 30 30 40

	**Control Function**, **Object Type**, **Object Name**
	Spindle Forward, QPushButton, spindle_fwd_s_pb
	Spindle Reverse, QPushButton, spindle_rev_s_pb
	Spindle Stop, QPushButton, spindle_stop_s_pb
	Spindle Faster, QPushButton, spindle_plus_s_pb
	Spindle Slower, QPushButton, spindle_minus_s_pb
	Spindle Speed, QSpinBox, spindle_speed_s_sb
	Spindle Speed, QSlider, spindle_speed_s_sl

Set S Word
----------

To set the `S` word to the current spindle RPM use the following button with the
object name and the spindle number. Replace the `s` in the Object Name with the
spindle number you want to set the `S` word for.

.. csv-table:: **Set the S Word**
   :width: 100%
   :align: center
   :widths: 30 30 40

	**Control Function**, **Object Type**, **Object Name**
	Set S Word, QPushButton, set_speed_s_pb

.. note:: The Set S Word button uses MDI so all axes must be homed before it's
   enabled.

Spindle Overrides
-----------------

If you just have one spindle you can use either the Multiple Spindle Override
with n being 0 or the Single Spindle Override.

.. csv-table:: **Single Spindle Override**
   :width: 100%
   :align: center
   :widths: 30 30 40

	**Control Function**, **Object Type**, **Object Name**
	Spindle Override, QSlider, spindle_override_sl

The spindle speed override is set using a QSlider. The Multiple Spindle Override
is the preferred spindle override to use. The spindles are numbered 0-7 so
replace the `s` in the Object Name with the number of the spindle you want to override.


.. csv-table:: **Multiple Spindle Override**
   :width: 100%
   :align: center
   :widths: 30 30 40

	**Control Function**, **Object Type**, **Object Name**
	Spindle Override, QSlider, spindle_override_s_sl

See the Status Labels above for spindle override status labels.

Spindle Speed Presets
---------------------

Each spindle can have QPushButtons configured to set a speed. Replace `s` in the
Object Name with the spindle number and the `nnn` with the speed you want the
spindle to change to when you press the button. The default spindle is `0`.

.. csv-table:: **Spindle Speed Presets**
   :width: 100%
   :align: left
   :widths: 40 20 40

	**Function**, **Widget**, **Object Name**
	Spindle Speed Preset, QPushButton, spindle_set_s_nnn

.. _spindle_override_presets:

Spindle Override Presets
------------------------

A QPushButton can be used to set the spindle override to a set value. The value
must be within the range of the override slider.

.. csv-table:: **Single Spindle Override Presets**
   :width: 100%
   :align: left
   :widths: 40 20 40

	**Function**, **Widget**, **Object Name**
	Spindle Override Preset, QPushButton, spindle_percent_nnn

For multiple spindles you need to add the spindle number to the object name.
Replace the `s` in the Object Name with the spindle number and the `nnn` with
the override percentage. For example for spindle 2 a preset of 75% the
QPushbutton name would be `spindle_percent_2_75`.

.. csv-table:: **Multiple Spindle Override Presets**
   :width: 100%
   :align: left
   :widths: 40 20 40

	**Function**, **Widget**, **Object Name**
	Spindle Override Preset, QPushButton, spindle_percent_s_nnn


