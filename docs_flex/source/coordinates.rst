Coordinate Systems
==================

`Coordinate System Tutorial <https://youtu.be/Bsk7_Ij7tVc/>`_

Coordinate System Touchoff
--------------------------

To touch-off an axis, use a QPushButton and QLineEdit to set the touch-off value

.. csv-table:: Coordinate System Touch Off Controls
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Touch Off Axis, QPushButton, touchoff_pb_(axis letter)
	Touch Off Value, QLineEdit, touchoff_le

Optionally you can have a QLineEdit for any axis by adding a string type Dynamic
Property named `source` and the value contains the object name of the QLineEdit
that you want to use. See :doc:`property`

.. image:: /images/coordinate-01.png
   :align: center

As you can see you can have a QLineEdit for each axis.

.. image:: /images/coordinate-02.png
   :align: center

Change Coordinate System
------------------------

To change the coordinate system via a button, use a change_cs_`n` QPushButton
where `n` is 1-9 for G54 through G59.3

.. csv-table:: Coordinate System Change Buttons
   :width: 100%
   :align: center

	**Control Function**, **Object Type**, **Object Name**
	Change Coordinate System, QPushButton, change_cs_(n)
