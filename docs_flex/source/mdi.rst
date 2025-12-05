Manual Data Input (MDI)
=======================
`MDI Tutorial <https://youtu.be/fHkyWxfZiKs>`_

MDI Interface
-------------

The MDI Interface uses a QLineEdit named `mdi_command_le` to enter commands.

For touch screens there are two options a `NC Popup` is a touch screen that has
G and M words and a number keypad or a `Keyboard Popup` has a full keyboard.

To enable a popup add a Dynamic string type Property to the `mdi_command_le`
QLineEdit and name it `input` and set the value to either `nccode` or
`keyboard`.

Note, QLineEdit widgets with object names that begin with 'mdi' do not respond
to the `return_button` dynamic property as the keyboard and mouse behavior
of these objects are handled internally by FlexGUI.

Dynamic Property

.. image:: /images/dynamic-property-01.png
   :align: center

Setting the value

.. image:: /images/dynamic-property-02.png
   :align: center

NC code popup window

.. image:: /images/nccode-popup.png
   :align: center

Keyboard popup window

.. image:: /images/keyboard-popup.png
   :align: center

MDI History
-----------

MDI history uses a QListWidget named `mdi_history_lw` to display the MDI
history. You can click on a line in the history display to copy the command to
the MDI Interface, ready for running.

.. image:: /images/mdi-history.png
   :align: center


The MDI history is kept in a file named `mdi_history.txt` in the configuration
directory.

MDI Controls
------------

The following QPushButtons can be used to execute, copy, and clear MDI command
history

.. csv-table:: MDI Push Buttons
   :width: 100%
   :align: center

	**Function**, **Widget**, **Object Name**
	Run MDI Command, QPushButton, run_mdi_pb
	Copy the MDI History to the Clipboard, QPushButton, copy_mdi_history_pb
	Save the MDI History to a file, QPushButton, save_mdi_history_pb
	Clear the MDI History, QPushButton, clear_mdi_history_pb

.. _MdiButtonTag:

MDI Button
----------

MDI buttons execute a MDI command when the button is pressed. These are
created by adding two dynamic properties called `function` and `command` to a
QPushButton.

.. csv-table:: MDI Command Button
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, mdi
	String, command, MDI command to execute


.. note:: If the `command` property is not found, the button will not be
   enabled!

Select the button then create a dynamic property by pressing the green plus
sign in the Property Editor

.. image:: /images/mdi-01.png
   :align: center

Then select `string`:

.. image:: /images/mdi-02.png
   :align: center

Name the property `function` and click OK

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

