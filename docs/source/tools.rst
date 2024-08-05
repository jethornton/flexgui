Tools and Coordinate Systems
============================

Tool Change
-----------

.. image:: /images/tools-01.png
   :align: center

A tool change QPushButton with a QComboBox to select the tool number to change
to is done with QPushButton named `tool_change_pb` and a QComboBox named
`tool_change_cb`. The tool change combobox will be populated with all the tools
found in the tool table.
::

	Tool Change                  tool_change_pb
	Tools Combo Box              tool_change_cb

Tool Change Button
------------------

Tool change QPushButtons can be used to change tools without a spinbox by adding
up to 99 QPushButtons named `tool_change_pb_n` with `n` being the number of the
tool you wish to change with that button.
::

	Tool Change Button                  tool_change_pb_n


Tool Touchoff
-------------

To touch off a tool to an axis use a tool touch off pushbutton
::

	Tool Touch Off               tool_touchoff_(axis letter)


Coordinate System Touchoff
--------------------------

To touch off an axis use a QPushButton and QLineEdit to set the touch off value

.. csv-table:: Touch Off Controls
   :width: 80%
   :align: center

	Function, Widget, Object Name
	Touch Off Axis, QPushButton, touchoff_pb_(axis letter)
	Touch Off Value, QLineEdit, touchoff_le


Change Coordinate System
------------------------

To change the coordinate system with a button use a change_cs_n pushbutton where
`n` is 1-9.
::

	Change Coordinate System            change_cs_n

