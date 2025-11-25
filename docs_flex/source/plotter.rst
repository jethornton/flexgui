Plotter
=======
`Plotter Tutorial <https://youtu.be/_f9sQWPe_XI>`_

To add a live G-code plotter, add a QWidget or QFrame and name it `plot_widget`.

Controls
--------

If you're using a touch-screen, add pan, zoom, and rotate controls for the 
plotter

.. csv-table:: Display Controls
   :width: 100%
   :align: center
   :widths: 40 40 40

	**Control**, **Widget**, **Object Name**
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
   :width: 100%
   :align: center
   :widths: 40 40 40

	**Control**, **Widget**, **Object Name**
	View Perspective, QPushButton, view_p_pb
	View X, QPushButton, view_x_pb
	View Y, QPushButton, view_y_pb
	View Y2, QPushButton, view_y2_pb
	View Z, QPushButton, view_z_pb
	View Z2, QPushButton, view_z2_pb

To clear the Live plot

.. csv-table:: Display Functions
   :width: 100%
   :align: center
   :widths: 40 40 40

	Control, Widget, Name
	Clear Live Plot, QPushButton, view_clear_pb

Display
-------

The DRO overlaid onto the plotter can be customized by turning on or off
various features. Use either a QCheckbox or a QPushButton to toggle these

.. csv-table:: Display Checkbox Options
   :width: 100%
   :align: center
   :widths: 40 40 40

	**Function**, **Widget**, **Object Name**
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

.. csv-table:: Display PushButton Options
   :width: 100%
   :align: center
   :widths: 40 40 40

	**Function**, **Widget**, **Object Name**
	View DRO, QPushButton, view_dro_pb
	View Machine Limits, QPushButton, view_limits_pb
	View Extents Option, QPushButton, view_extents_option_pb
	View Live Plot, QPushButton, view_live_plot_pb
	View Velocity, QPushButton, view_velocity_pb
	Use Metric Units, QPushButton, view_metric_units_pb
	View Program, QPushButton, view_program_pb
	View Rapids, QPushButton, view_rapids_pb
	View Tool, QPushButton, view_tool_pb
	View Lathe Radius, QPushButton, view_lathe_radius_pb
	View Distance to Go, QPushButton, view_dtg_pb
	View Offsets, QPushButton, view_offsets_pb
	View Overlay, QPushButton, view_overlay_pb

.. note:: Don't set the checked property to checked in Qt Designer as this is
   already handled in the code. Once you check an option it is remembered.

Menu
----

The following menu items can set display options. `Menu Name` is what you
type when creating the Menu, then press enter. All the items are checkbox type
menu items that stay coordinated with the checkbox of the same option.

.. csv-table:: Plot Menu Options
   :width: 100%
   :align: center
   :widths: 40 40 40

	**Function**, **Menu Name**, **Object Name**
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

The live plot can be cleared from the menu with this menu item.

.. csv-table:: Clear Live Plot Menu
   :width: 100%
   :align: center
   :widths: 40 40 40

	**Function**, **Menu Name**, **Object Name**
	Clear Live Plot, Clear Live Plot, actionClear_Live_Plot

Grids
^^^^^

The plotter can optionally display a grid when in orthogonal views. To add the
option of grids add a menu item named `Grids`. The grid size selection will be
added to the `Grids` menu item. The default grid sizes are based on the machine
units.

.. csv-table:: Plot Menu Grids
   :width: 100%
   :align: center
   :widths: 40 40 40

	**Function**, **Menu Name**, **Object Name**
	Plotter Grid, Grids, actionGrids

To configure the size options of the grid, add a `GRIDS` item to the `[DISPLAY]`
section of the INI file.

The values are a comma separated list of values. The units if left out will be
machine units. While you can mix units usually machine units are used. Units can
be `in` or `mm` or left out.
::

	[DISPLAY]
	GRIDS = 1/2, 1in, 2in, 4in, 8in
	or
	GRIDS = 10mm, 20mm, 50mm, 100mm

The first item in the list will be considered the default and set when FlexGUI starts.
If you wish disable grid by default, add a `0` item to the beginning of the list.

The `Grids` menu can be part of the main menu bar, or added to a submenu.

DRO
---

The font size can be set in the ini file by adding in the [FLEXGUI] section 
DRO_FONT_SIZE = n where n is an integer. The default size is 12.
