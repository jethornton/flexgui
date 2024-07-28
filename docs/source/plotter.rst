Plotter
=======

To add a live plotter add a QWidget or QFrame and name it `plot_widget`

Controls
--------

If you're using a touch screen add pan, zoom and rotate controls.
::

	Control           Widget            Name
	Zoom In           QPushButton       view_zoom_in_pb
	Zoom Out          QPushButton       view_zoom_out_pb
	Pan Up            QPushButton       view_pan_up_pb
	Pan Down          QPushButton       view_pan_down_pb
	Pan Left          QPushButton       view_pan_left_pb
	Pan Right         QPushButton       view_pan_right_pb
	Rotate Up         QPushButton       view_rotate_up_pb
	Rotate Down       QPushButton       view_rotate_down_pb
	Rotate Left       QPushButton       view_rotate_left_pb
	Rotate Right      QPushButton       view_rotate_right_pb
	Clear Plot        QPushButton       view_clear_pb


.. note:: P and X presets do not function at this time... not figured them out yet.

Display
-------

Some items in the plot can be turned on or off and note the program limits default
to metric for now.
::

	Function                 Widget         Name
	Use Inch                 QCheckBox      view_inches_cb
	Show Machine Limits      QCheckBox      show_limits_cb



