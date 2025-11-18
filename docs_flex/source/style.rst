StyleSheet
==========

You can use your own .qss style sheet by creating a valid .qss file in the
configuration directory and setting it in the :doc:`ini`.
::

	[DISPLAY]
	QSS = name_of_file.qss

.. Note:: If a THEME is found in the ini file the QSS entry is ignored

The Qt `Style Sheets Reference <https://doc.qt.io/qt-6/stylesheet-reference.html>`_
and the `Style Sheet Syntax <https://doc.qt.io/qt-6/stylesheet-syntax.html>`_
and the `Style Sheet Examples <https://doc.qt.io/qt-6.2/stylesheet-examples.html>`_
are good references to use when creating your own stylesheets.

.. note:: If there is an error in the stylesheet syntax, no warning is issued,
   it is just ignored. So don't forget the ; at the end of each setting. And do
   not accidentally use any backslashes it will break the whole file.

.. warning:: If you only set a background-color on a QPushButton, the background
   may not appear unless you set the border property to some value, even if
   border is set to none.

Rules
-----

When multiple rules apply, QSS follows specificity rules similar to CSS. More
specific selectors (e.g., those with pseudo-states or object names) take
precedence. If specificity is equal, the last rule defined in the stylesheet
takes precedence. In this example if a QPushButton state is hover or pressed or
disabled the background-color will change.
::

	QPushButton {
		background-color: lightgray;
		color: black;
		border: 1px solid gray;
		padding: 5px;
	}
	QPushButton:hover {
		background-color: lightblue;
		color: white;
	}
	QPushButton:pressed {
		background-color: darkblue;
		border-style: inset;
	}
	QPushButton:disabled {
		background-color: #cccccc;
		color: #666666;
	}

Colors
------

Most colors can be specified using Hex, RGB or RGBA color model. RGB is
Red, Green, Blue and A means Alpha or transparency. The alpha parameter is a
number between 0.0 (fully transparent) and 1.0 (not transparent at all). Hex is
red, green blue in hexadecimal number pairs from 00 to ff.

.. code-block:: html

	#0000ff
	rgb(0, 0, 255) Blue
	rgba(0, 0, 255, 25%) Light Blue

Controls
--------

The style can be set in the qss stylesheet for an individual QPushButton by
using the QPushButton object name. For example to target the E Stop button use
`#estop_pb` to target the Power button use `#power_pb`.

.. code-block:: html

	QPushButton#estop_pb {
		font-size: 24px;
		font-weight: 700;
		background-color: yellow;
		border-style: outset;
		border-width: 5;
		border-color: red;
		border-radius: 10;
	}
	QPushButton#estop_pb:checked {
		color: white;
		background-color: red;
		border-style: inset;
		border-color: yellow;
	}

	QPushButton#power_pb {
		font-size: 24px;
		font-weight: 800;
		background-color: red;
		border-style: outset;
		border-width: 5;
		border-color: green;
		border-radius: 10;
	}
	QPushButton#power_pb:checked {
		color: white;
		background-color: green;
		border-style: inset;
		border-color: black;
	}

To make a font bold use the font-weight, 400 is normal and 700 is bold.

.. WARNING:: Any errors like forgetting a ; will make the rest of the stylesheet
   not apply.

Flashing
--------

Checkable buttons, like estop_pb, power_pb, or hal_buttons that are checkable
can flash when either checked or not checked. To add flashing add one String
type Dynamic Property to the QPushButton.

.. csv-table:: Flashing Push Button
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, flash_state, checked or unchecked

When the button checked state matches the `flash_state` value, the button will
flash between the normal background-color and the checked or !checked (not
checked) background-color. The `[flashing="True"]` must be added to the state
that matches the `flash_state` value.

To make the E Stop QPushButton flash when not checked the flash_state Dynamic
Property must be set to `unchecked` and following example could be used.

.. code-block:: html

	QPushButton#estop_pb {
		font-size: 12px;
		font-weight: 700;
		background-color: yellow;
		border-style: outset;
		border-width: 2;
		border-color: red;
		border-radius: 5;
	}

	QPushButton#estop_pb:checked {
		color: white;
		background-color: red;
		border-style: inset;
		border-color: yellow;
	}

	QPushButton#estop_pb:!checked[flashing="True"] {
		background-color: red;
	}

In the above example the E Stop push button will flash if not checked.

To make the Power QPushButton flash if not checked and enabledthe flash_state
Dynamic Property must be set to `unchecked` and following example could be used.

.. code-block:: html

	QPushButton#power_pb {
		font-size: 12px;
		font-weight: 700;
		background-color: yellow;
		border-style: outset;
		border-width: 2;
		border-color: red;
		border-radius: 5;
	}

	QPushButton#power_pb:checked {
		color: white;
		background-color: red;
		border-style: inset;
		border-color: yellow;
	}

	QPushButton#power_pb:!checked:enabled[flashing="True"] {
		background-color: red;
	}

Examples
--------

.. code-block:: html

	/* Set the background color for all QPushButtons, border is required * /
	QPushButton {
		background-color: rgba(224, 224, 224, 50%);
		border: 1px;
	}
	
	/* Set the background color and style for all QPushButtons when Pressed * /
	QPushButton:pressed {
		background-color: rgba(192, 192, 192, 100%);
		border-style: inset;
	}

	/* Set settings for a QPushButton named exit_pb * /
	QPushButton#exit_pb {
		border: none;
		background-color: rgba(0, 0, 0, 0);
	}

	/* Using sub controls * /
	QAbstractSpinBox::up-button {
		min-width: 30px;
	}

	/* Combining sub controls and state * /
	QTabBar::tab:selected {
		background: lightgray;
	}

	/* Target by Object Name starts with something common*/
	QLabel[objectName*="dro"] {
		font-family: Courier;
		font-size: 14pt;
		font-weight: 700;
	}

Tool Bar Buttons
----------------

A tool bar button created from a menu action can be styled by using the 
QToolButton` selector:

.. code-block:: html

	QToolButton:hover {
		background-color: rgba(255, 0, 0, 75%);
	}

To set the style of a single tool bar button, you need to use the widget name
for that action. The tool bar button must exist in the tool bar.

.. csv-table:: Tool Button Names
   :width: 100%
   :align: left

	**Menu Item**, **Action Name**, **Widget Name**
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

The syntax to select a tool bar button by name (here the flex_Quit button) is:

.. code-block:: html

	QToolButton#flex_Quit:hover {
		background-color: rgba(255, 0, 0, 75%);
	}
