Tools and Coordinate Systems
============================

Tool Change
-----------

.. image:: /images/tools-01.png
   :align: center

A tool change QPushButton, with a QComboBox to select the tool number to change
to, is done with QPushButton named `tool_change_pb` and a QComboBox named
`tool_change_cb`. The tool change combobox will automatically be populated with
all the tools found in the tool table.

.. csv-table:: Tool Change Controls
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Tool Change, QPushButton, tool_change_pb
	Tool Selector, QComboBox, tool_change_cb

Manual Tool Change requires at least the following HAL code in the main hal
file if the hal connections are not done in another manner.
::
	# manual tool change
	loadusr -W hal_manualtoolchange
	net tool-change iocontrol.0.tool-change => hal_manualtoolchange.change
	net tool-changed iocontrol.0.tool-changed <= hal_manualtoolchange.changed
	net tool-number iocontrol.0.tool-prep-number => hal_manualtoolchange.number
	net tool-prepare-loopback iocontrol.0.tool-prepare => iocontrol.0.tool-prepared

Tool Change Button
------------------

Tool change QPushButtons can be used to change tools without a spinbox by adding
up to 99 QPushButtons named `tool_change_pb_n`. With `n` being the number of
the tool you wish to change to using that button

.. csv-table:: Tool Change Buttons
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Tool Change Button, QPushButton, tool_change_pb_(n)

Tool Touchoff
-------------

To touch-off a tool to an axis, use a tool-touch-off QPushButton and a QLineEdit
to enter the value of the touch off.

.. csv-table:: Tool Touchoff Controls
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Tool Touch Off Value, QLineEdit, tool_touchoff_le
	Tool Touch Off, QPushButton, tool_touchoff_(axis letter)

Coordinate System Touchoff
--------------------------

To touch-off an axis, use a QPushButton and QLineEdit to set the touch-off value

.. csv-table:: Coordinate System Touch Off Controls
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Touch Off Axis, QPushButton, touchoff_pb_(axis letter)
	Touch Off Value, QLineEdit, touchoff_le

Change Coordinate System
------------------------

To change the coordinate system via a button, use a change_cs_`n` QPushButton
where `n` is 1-9 for G54 through G59.3

.. csv-table:: Coordinate System Change Buttons
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Change Coordinate System, QPushButton, change_cs_(n)
