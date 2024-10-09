Plotter
=======

To add a live G-code plotter, add a QWidget or QFrame and name it `plot_widget`.

Controls
--------

If you're using a touch-screen, add pan, zoom, and rotate controls for the 
plotter

.. csv-table:: Display Controls
   :width: 80%
   :align: center
   :widths: 40 40 40

	Control, Widget, Object Name
	Rotate View Up, QPushButton, view_rotate_up_pb
	Rotate View Down, QPushButton, view_rotate_down_pb
	Rotate View Left, QPushButton, view_rotate_left_pb
	Rotate View Right, QPushButton, view_rotate_right_pb
	Pan View Up, QPushButton, view_pan_up_pb
	Pan View Down, QPushButton, view_pan_down_pb
	Pan View Left, QPushButton, view_pan_left_pb
	Pan View Right, QPushButton, view_pan_right_pb
	Zoom View In, QPushButton, view_zoom_in_pb
	Zoom View Out, QPushButton, view_zoom_out_pb


The following controls set-predefined views

.. csv-table:: Display Views
   :width: 80%
   :align: center
   :widths: 40 40 40

	Control, Widget, Object Name
	View Perspetive, QPushButton, view_p_pb
	View X, QPushButton, view_x_pb
	View Y, QPushButton, view_y_pb
	View Y2, QPushButton, view_y2_pb
	View Z, QPushButton, view_z_pb
	View Z2, QPushButton, view_z2_pb


To clear the Live plot

.. csv-table:: Display Functions
   :width: 80%
   :align: center
   :widths: 40 40 40

	Control, Widget, Name
	Clear Live Plot, QPushButton, view_clear_pb


Display
-------

The DRO overlaid onto the plotter can be customized by turning on or off
various features. Use either a QCheckbox or a Menu to toggle these

.. csv-table:: Display Checkbox Options
   :width: 80%
   :align: center
   :widths: 40 40 40

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

.. note:: Don't set the checked property to checked in Qt Designer as this is
   already handled in the code. Once you check an option it is remembered.


Menu
----

The following menu items can set display options. `Menu Name` is what you
type when creating the Menu, then press enter.

.. csv-table:: Display Menu Options
   :width: 80%
   :align: center
   :widths: 40 40 40

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

.. note:: Once a view selection has been set, Flex GUI remembers it.


DRO
---

The font size can be set in the ini file by adding in the [DISPLAY] section 
DRO_FONT_SIZE = n where n is an integer. The default size is 12.
