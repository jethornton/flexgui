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
Property named `option` and set the value to `description`.

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


