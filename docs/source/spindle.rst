Spindle
=======

On start up Flex will see if the following items are in the `SPINDLE_0`
section of the ini file.
::

	INCREMENT
	MIN_FORWARD_VELOCITY
	MAX_FORWARD_VELOCITY

If `INCREMENT` is not found Flex will look in the `DISPLAY` section for
`SPINDLE_INCREMENT` and if not found will set the increment at 100 for spindle
faster/slower control buttons.

Spindle Controls
----------------

The following QPushButtons control the spindle on/off direction and speed.
::

	Description       Object Name
	Spindle Forward   spindle_fwd_pb
	Spindle Reverse   spindle_rev_pb
	Spindle Stop      spindle_stop_pb
	Spindle Faster    spindle_plus_pb
	Spindle Slower    spindle_minus_pb

A QSpinBox with the object name `spindle_speed_sb` controls the spindle speed.

If `MIN_FORWARD_VELOCITY` is found it will be used to set the QSpinBox minimum
setting. If not found the minimum setting will be 0

If `MAX_FORWARD_VELOCITY` is found it will set the QSpinBox maximum setting. If
not found the maximum setting will be 1000

`INCREMENT` will set the QSpinBox single step.

If a QLCDNumber named `spindle_speed_0_lcd` is found it will display the
commanded spindle speed without any offsets.
