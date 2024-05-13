StyleSheet
==========

You can use your own qss style sheet by creating a valid qss file in the
configuration directory and setting it in the INI file.

The Qt `Style Sheets Reference <https://doc.qt.io/qt-6/stylesheet-reference.html>`_
and the `Style Sheet Syntax <https://doc.qt.io/qt-6/stylesheet-syntax.html>`_
are good references to use when creating your own stylesheet.

.. note:: If there is a error in the stylesheet syntax no warning is issued, 
   it's just ignored. So don't forget the ; at the end or each setting.

Colors
------

Most colors can be specified using either the RGB color model or the RGBA color
model. RGB is Red, Green, Blue and RGBA is Red, Green, Blue, Alpha.

.. code-block:: bash

	rgb(0, 0, 255) Blue
	rgba(0, 0, 255, 25%) Light Blue

Examples
--------

.. code-block:: html

	/*Set the background color for all QPushButtons*/
	QPushButton{
		background-color: rgba(224, 224, 224, 50%);
	}
	
	/*Set the background color and style for all QPushButtons when Pressed*/
	QPushButton:pressed{
		background-color: rgba(192, 192, 192, 100%);
		border-style: inset;
	}

	/*Set settings for a QPushButton named exit_pb*/
	QPushButton#exit_pb{
	border: none;
	background-color: rgba(0, 0, 0, 0);
	}

	/*Using sub controls*/
	QAbstractSpinBox::up-button {
		min-width: 30px;
	}

	/*Combining sub controls and state*/
	QTabBar::tab:selected {
		background: lightgray;
	}

Tool Bar Buttons
----------------

A tool bar button created from a menu action can be styled by using the
`QToolButton` selector.
::

	QToolButton:hover {
		background-color: rgba(255, 0, 0, 75%);
	}

To set the style of a single tool bar button you need to use the widget name for
that action. The tool bar button has to exist in the tool bar

.. csv-table:: Tool Button Names
   :width: 100%
   :align: left

	Menu Item, Action Name, Widget Name
	Open, actionOpen, flex_Open
	Edit, actionEdit, flex_Edit
	Reload, actionReload, flex_Reload
	Save As, actionSave_As, flex_Save_As
	Edit Tool Table, actionEdit_Tool_Table, flex_Edit_Tool_Table
	Reload Tool Table, actionReload_Tool_Table, flex_Reload_Tool_Table
	Ladder Editor, actionLadder_Editor, flex_Ladder_Editor
	Quit, actionQuit, flex_Quit
	E Stop, actionE_Stop, flex_E_Stop
	Power, action_Power, flex_Power
	Run, actionRun, flex_Run
	Run From Line, actionRun_From_Line, flex_Run_From_Line
	Step, actionStep, flex_Step
	Pause, actionPause, flex_Pause
	Resume, actionResume, flex_Resume
	Stop, actionStop, flex_Stop
	Clear MDI History, actionClear_MDI_History, flex_Clear_MDI_History
	Copy MDI History, actionCopy_MDI_History, flex_Copy_MDI_History
	Show HAL, actionShow_HAL, flex_Show_HAL
	HAL Meter, actionHAL_Meter, flex_HAL_Meter
	HAL Scope, actionHAL_Scope, flex_HAL_Scope
	About, actionAbout, flex_About
	Quick Reference, actionQuick_Reference, flex_Quick_Reference

The syntax to select a tool bar button by name is:

.. code-block:: bash

	QToolButton#flex_Quit:hover {
		background-color: rgba(255, 0, 0, 75%);
	}






