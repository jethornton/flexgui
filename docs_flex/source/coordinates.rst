==================
Coordinate Systems
==================

`Coordinate System Tutorial <https://youtu.be/Bsk7_Ij7tVc/>`_

Coordinate System Touchoff
--------------------------

To touch-off an axis, use a QPushButton and QLineEdit to set the touch-off value.
Optionally you can have a QComboBox to select the Coordinate System to touch off
to.

.. csv-table:: **Coordinate System Touch Off Controls**
   :width: 100%
   :align: center
   :widths: 33 33 33

	**Control Function**, **Object Type**, **Object Name**
	Touch Off Axis, QPushButton, touchoff_pb_(axis letter)
	Touch Off Value, QLineEdit, touchoff_le
	Optional
	Coordinate System, QComboBox, touchoff_system_cb

Optionally you can have a QLineEdit for any axis by adding a string type Dynamic
Property named `source` to the QPushButton and the value contains the object
name of the QLineEdit that you want to use. See :doc:`property`

.. image:: /images/coordinate-01.png
   :align: center

As you can see you can have a QLineEdit for each axis.

.. image:: /images/coordinate-02.png
   :align: center

Zero Axis Buttons
-----------------

Zero axis buttons set the active work coordinate offset (`G54–G59.3`) for
the specified axis to `0.0` at the current tool position. Unlike the standard
touch-off buttons, these do not require a `touchoff_le` line edit widget.

To add a zero axis button, add a `QPushButton` and set the `objectName` to one
of the following:

.. csv-table:: **Zero Axis Buttons**
   :width: 100%
   :align: center
   :widths: 33 33 33

	**Control Function**, **Object Type**, **Object Name**
	Zero All Configured Axes, QPushButton, zero_pb_all
	Zero X Axis, QPushButton, zero_pb_x
	Zero Y Axis, QPushButton, zero_pb_y
	Zero Z Axis, QPushButton, zero_pb_z
	Zero A Axis, QPushButton, zero_pb_a
	Zero B Axis, QPushButton, zero_pb_b
	Zero C Axis, QPushButton, zero_pb_c
	Zero U Axis, QPushButton, zero_pb_u
	Zero V Axis, QPushButton, zero_pb_v
	Zero W Axis, QPushButton, zero_pb_w

.. note:: Zero axis buttons execute `G10 L20 P0 <Axis>0` in MDI mode and are
   automatically disabled when the machine is off, unhomed, or running a program.


Change Coordinate System
------------------------

To change the coordinate system via a button, use a change_cs_`n` QPushButton
where `n` is 1-9 for G54 through G59.3

.. csv-table:: **Coordinate System Change Buttons**
   :width: 100%
   :align: center
   :widths: 33 33 33

	**Control Function**, **Object Type**, **Object Name**
	Change Coordinate System, QPushButton, change_cs_(n)
