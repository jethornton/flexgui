Plotter
=======

To add a live plotter add a QWidget or QFrame and name it `plot_widget`

Controls
--------

If you're using a touch screen add pan, zoom and rotate controls.

.. csv-table:: Display Controls
   :width: 80%
   :align: center

	Control, Widget, Object Name
	Rotate Up, QPushButton, view_rotate_up_pb
	Rotate Down, QPushButton, view_rotate_down_pb
	Rotate Left, QPushButton, view_rotate_left_pb
	Rotate Right, QPushButton, view_rotate_right_pb
	Pan Up, QPushButton, view_pan_up_pb
	Pan Down, QPushButton, view_pan_down_pb
	Pan Left, QPushButton, view_pan_left_pb
	Pan Right, QPushButton, view_pan_right_pb
	Zoom In, QPushButton, view_zoom_in_pb
	Zoom Out, QPushButton, view_zoom_out_pb

The following controls set predefined views

.. csv-table:: Display Views
   :width: 80%
   :align: center

	Control, Widget, Object Name
	View Perspetive, QPushButton, view_p_pb
	View X, QPushButton, view_x_pb
	View Y, QPushButton, view_y_pb
	View Y2, QPushButton, view_y2_pb
	View Z, QPushButton, view_z_pb
	View Z2, QPushButton, view_z2_pb

.. note:: P and X presets do not function at this time... not figured them out yet.

To clear the Live plot use:

.. csv-table:: Display Functions
   :width: 80%
   :align: center

	Control, Widget, Name
	Clear Live Plot, QPushButton, view_clear_pb

Display
-------

Some items in the plot can be turned on or off and note the program limits default
to metric for now.

.. csv-table:: Display Control Options
   :width: 80%
   :align: center

	Function, Widget, Object Name
	View DRO, QCheckBox, view_dro_cb
	View Machine Limits, QCheckBox, view_limits_cb
	View Extents Option, QCheckBox, view_extents_option_cb
	View Live Plot, QCheckBox, view_live_plot_cb
	View Velocity, QCheckBox, view_velocity_cb
	Use Metric Units, QCheckBox, view_metric_units_cb
	View Program, QCheckBox, view_program_cb
	View Rapids, QCheckBox, view_rapids_cb
	View Tool, QCheckBox, view_tool_cb
	View Lathe Radius, QCheckBox, view_lathe_radius_cb
	View Distance to Go, QCheckBox, view_dtg_cb
	View Offsets, QCheckBox, view_offsets_cb
	View Overlay, QCheckBox, view_overlay_cb

Menu
----

The following menu items can set display options. `Menu Name` is what you type
when creating the Menu then press enter.

.. csv-table:: Display Menu Options
   :width: 80%
   :align: center

	Function, Menu Name, Object Name
	View DRO, DRO, actionDRO
	View Machine Limits, Limits, actionLimits
	View Extents Option, Extents Option, actionExtents_Option
	View Live Plot, Live Plot, actionLive_Plot
	View Velocity, Velocity, actionVelocity
	Use Metric Units, Metric Units, actionMetric_Units
	View Program, Program, actionProgram
	View Rapids, Rapids, actionRapids
	View Tool, Tool, actionTool
	View Lathe Radius, Lathe Radius, actionLathe_Radius
	View Distance to Go, DTG, actionDTG
	View Offsets, Offsets, actionOffsets
	View Overlay, Overlay, actionOverlay

.. note:: Once a veiw selection has been set Flex GUI remembers that the next
   time you start the configuration.


