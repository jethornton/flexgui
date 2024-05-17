Tools and Coordinate Systems
============================

Tool Change
-----------

.. image:: /images/tools-01.png
   :align: center

A tool change QPushButton with a QSpinBox to select the tool number to change
to is done with QPushButton named `tool_change_pb` and a QSpinBox named
`next_tool_sb`. It is an error if the tool selected is not in the tool table.

Tool change QPushButtons can be used to change tools without a spinbox by adding
up to 99 QPushButtons named `tool_change_pb_n` with `n` being the number of the
tool you wish to change with that button.

Tool Touchoff
-------------



Coordinate System Touchoff
--------------------------

Change Coordinate System
------------------------


	Touch Off Axis               touchoff_pb_(axis letter)
	Tool Touch Off               tool_touchoff_(axis letter)
	Tool Change                  tool_change_pb

