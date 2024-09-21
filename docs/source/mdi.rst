Manual Data Input (MDI)
=======================

MDI Interface
-------------

The MDI Interface uses a QLineEdit to enter commands. Three different ways can
but used to enter the commands. Using the Keyboard, using a popup G code in a
touch screen which can handle all G code entries and last a full popup Keyboard
which can enter any valid command including DEBUG prints.

.. csv-table:: MDI Command Entry
   :width: 80%
   :align: center

	Function, Input, Widget, Name
	Enter MDI, Keyboard, QLineEdit, mdi_command_le
	Enter MDI, G code Popup, QLineEdit, mdi_command_gc_le
	Enter MDI, Keyboard Popup, QLineEdit, mdi_command_kb_le

G code popup window

.. image:: /images/gcode-popup.png
   :align: center

Keyboard popup window

.. image:: /images/keyboard-popup.png
   :align: center


MDI history uses a QListWidget named `mdi_history_lw` to display the MDI
history. You can click on a line in the history display to copy the command to
the MDI Interface

MDI Controls
------------

The following QPushButtons can be used to execute MDI commands, copy or clear
MDI history

.. csv-table:: MDI Push Buttons
   :width: 80%
   :align: center

	Run MDI Command,run_mdi_pb
	Copy the MDI History to the Clipboard,copy_mdi_history_pb
	Clear the MDI History,clear_mdi_history_pb

The MDI history is kept in a file named 'mdi_history.txt` in the configuration
directory.

MDI Buttons
-----------

MDI buttons execute a MDI command when the button it pressed and are created by
adding two dynamic properties called `function` and `command` to a QPushButton.

.. note:: If the `command` property is not found the button will not be enabled

Select the button then create a dynamic property by pressing on the green plus
sign in the Property Editor.

.. image:: /images/mdi-01.png
   :align: center

Then select `string`

.. image:: /images/mdi-02.png
   :align: center

Name the property `function` and click on OK

.. image:: /images/mdi-03.png
   :align: center

Set the value of the property to `mdi`

.. image:: /images/mdi-04.png
   :align: center

Add a property called `command`

.. image:: /images/mdi-05.png
   :align: center

Set the value of the property to your valid MDI command

.. image:: /images/mdi-06.png
   :align: center


