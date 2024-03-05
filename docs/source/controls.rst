Controls
========

Controls are QPushButtons that can be placed anywhere you like. Use the Name
from the list below for each control widget objectName.
::

	Control  Name
	E-Stop            estop_pb
	Power             power_pb
	Run               run_pb
	Step              step_pb
	Pause             pause_pb
	Resume            resume_pb
	Stop              stop_pb
	Home All          home_all_pb
	Home Joint n      home_pb_n
	Unhome All        unhome_all_pb
	Unhome Joint n    unhome_pb_n
	Manual Mode       manual_mode_pb
	Run MDI           run_mdi_pb
	Touch Off Axis    touchoff_pb_(axis letter)
	Tool Touch Off    tool_touchoff_(axis letter)
	Jog Plus Axis     jog_plus_pb_(axis letter)
	Jog Minus Axis    jog_minus_pb_(axis letter)
	Tool Change       tool_change_pb
	Spindle Start     start_spindle_pb
	Spindle Stop      stop_spindle_pb
	Spindle Faster    spindle_plus_pb
	Spindle Slower    spindle_minus_pb
	Flood Toggle      flood_pb
	Mist Toggle       mist_pb
	Clear MDI History clear_mdi_history_pb

.. image:: /images/controls-01.png
   :align: center


.. note:: You don't have to use all the controls, the ones found will be
   connected to the correct code. Some controls will be mandatory.

