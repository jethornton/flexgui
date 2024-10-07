Touch Screens
=============

Some entry widgets like MDI and Touch-Off have a touch-screen popup available to make it easier for those users to enter the data.


Tool Bar
--------

To add a button to the tool bar without having a menu item that creates an action, you just have to create the action yourself:

.. image:: /images/new-action-01.png
   :align: center

The action creating window, when you type in the Text name, the Object name is created for you:

.. image:: /images/new-action-02.png
   :align: center

.. warning:: Make sure the Object name matches the Action Name created when you create a menu item - see the :doc:`menu` section for the ful list of Action Names.

Now you just drag the action into the tool bar to create a new tool bar button:

.. image:: /images/new-action-03.png
   :align: center

Another option is to just use QPushButtons in a QFrame, as every menu action has a QPushButton as well that executes the same function.


MDI
---

To enable the GCODE popup for the MDI entry, the QLineEdit object name must be either `mdi_command_gc_le` for the GCODE popup or `mdi_command_kb_le` for the keyboard popup:

.. image:: /images/touch-01.png
   :align: center

The GCODE Dialog will appear when you touch the MDI entry box:

.. image:: /images/touch-02.png
   :align: center

The Arrow Buttons change the bottom section to different letters:

.. image:: /images/touch-03.png
   :align: center


Touch Off
---------

The Coordinate System Touch-Off offset is a QLineEdit named `touchoff_le`.  To enable the number pad popup for the offset entry, add a Dynamic Property named `input` and set the value to `number`:

.. image:: /images/touch-04.png
   :align: center

Touch-Off:

.. image:: /images/touch-05.png
   :align: center


Tool Touch-Off:
--------------

The Tool Touch-Off offset is a QLineEdit named `tool_touchoff_le`.  To enable the number pad popup for the offset entry, add a Dynamic Property named `input` and set the value to `number`.


Spin Boxes
----------

QDoubleSpinBox and QSpinBox can use the popup numbers keypad by adding a Dynamic Property named `input` and seting the value to `number`. If you enter a float value for a QSpinBox the value will get converted to an integer.


Line Edits
----------

A QLineEdit can have a popup entry for numbers, GCODE, or a full keyboard.  Add a Dynamic Property named `input` and set the value to one of these `number`, `gcode`, or `keyboard`.


File Navigator
--------------

If a QListWidget with an objectName of `file_lw` is found, a touch-friendly file selector is added. A Parent Directory and possibly a directory name with an ellipsis can be used to change directories. Touch a file name and it is loaded into the GUI.

If PROGRAM_PREFIX is specified, that will be the starting directory:

.. image:: /images/touch-06.png
   :align: center
