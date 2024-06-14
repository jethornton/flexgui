Tools and Coordinate Systems
============================

Tool Change
-----------

.. image:: /images/tools-01.png
   :align: center

A tool change QPushButton with a QSpinBox to select the tool number to change
to is done with QPushButton named `tool_change_pb` and a QSpinBox named
`next_tool_sb`. It is an error if the tool selected is not in the tool table.
::

	Tool Change                  tool_change_pb

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

To touch off an axis use a touch off pushbutton
::

	Touch Off Axis               touchoff_pb_(axis letter)


Change Coordinate System
------------------------

To change the coordinate system with a button use a change_cs_n pushbutton where
`n` is 1-9.
::

	Change Coordinate System            change_cs_n

