Tools
======

`Tools Tutorial <https://youtu.be/SQZ6RJj9hP8>`_

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

To add the description of the tools to the tool change combo box add a Dynamic
Property named `option` and set the value to `description`. See :doc:`property`

.. image:: /images/tools-02.png
   :align: center

The description from the tool table will be appended to the tool number.

.. image:: /images/tools-03.png
   :align: center

If you have limited space you can define the tool prefix by adding a Dynamic
Property named `prefix` and set the value to the prefix you want.

.. image:: /images/tools-04.png
   :align: center

The tool number will follow the prefix.

.. image:: /images/tools-05.png
   :align: center

.. note:: Only one option can be used, if option is found it is used and prefix
   will be ignored.

Manual Tool Change
------------------

All that is needed to add a manual tool change is to add the following to the
ini file in the [FLEX] section.
::

	[FLEX]
	MANUAL_TOOL_CHANGE = True

.. image:: /images/tools-06.png
   :align: center

.. warning:: You can't use the hal_manualtoolchange at the same time as the
   builtin Flex Manual Tool Change

Manual Tool Change requires at least the following HAL code in the main hal
file if not using the buildin Flex Manual Tool Change.
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

Optionally you can have a QLineEdit for each axis for tool touch off. Add a
Dynamic Property named `source` to the tool touch off button and set the value
to the name of the QLineEdit that is the source for that touch off button.
See :doc:`property`

.. image:: /images/tools-07.png
   :align: center

Tool touch off QLineEdit for each axis.

.. image:: /images/tools-08.png
   :align: center

Current Tool Status
-------------------

Current Tool status of the tool loaded in the spindle. All the labels can have a
Dynamic Property called `precision` with the number of digits you wish to show.
The `tool_id_lb` and the `tool_orientation_lb` are integers.

.. csv-table:: Tool Table Status Labels
   :width: 100%
   :align: center
   :widths: 40 40 40

	tool_id_lb, tool_xoffset_lb, tool_yoffset_lb
	tool_zoffset_lb, tool_aoffset_lb, tool_boffset_lb
	tool_coffset_lb, tool_uoffset_lb, tool_voffset_lb
	tool_woffset_lb, tool_diameter_lb, tool_frontangle_lb
	tool_backangle_lb, tool_orientation_lb

