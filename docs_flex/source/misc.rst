Miscellaneous Items
===================

Line Edit
---------

A QLineEdit can trigger a click event on a QPushButton by pressing the Enter key
or if a touch screen popup keypad is used when Save is pressed. Add a String
Type Dynamic Property called `return_button` with the value being the object
name of the QPushButton.

File Selector
-------------

Add a QListWidget and name it `file_lw`, this can be used with a touch screen by
specifying the touch input. A single left-click or touch is all that's needed to
use the `File Selector`. A left-click or touch on a directory will change to
that directory. A left-click or touch on the up or down arrow will move the list
by one. A left-click or touch in between an arrow and the slider will move the
list by one page. Touch-and-hold to move the slider.

If you use the touch input, the selector looks like this

.. image:: /images/file-selector-01.png
   :align: center

.. note:: Make sure you use a QListWidget and not a QListView for the file
   selector.

`File, Error and Information Tutorial <https://youtu.be/kTFMM71VFuU>`_

Code Viewer
-----------

To add a code viewer, add a `QPlainTextEdit` from Input Widgets and name it
`gcode_pte`

.. image:: /images/gcode-viewer-01.png
   :align: center

Code Viewer Controls
--------------------

The Code Viewer allows you to edit the file in Flex GUI without using an external
text editor. You can save the current code to the current file name, save the
current code with a new file name and you can search the code.

.. csv-table:: Code Viewer Controls
   :width: 100%
   :align: center

	**Function**, **Type**, **Object Name**
	Save, QPushButton, save_pb
	Save As, QPushButton, save_as_pb
	Search, QPushButton, search_pb

MDI Viewer
----------

To add a MDI viewer, add a `QListWidget` from Item Widgets and name it
`mdi_history_lw`

.. image:: /images/mdi-viewer-01.png
   :align: center

To enter MDI commands, add a Line Edit and name it `mdi_command_le`.

Error Viewer
------------
To add an error viewer, add a `QPlainTextEdit` from Input Widgets and name it
`errors_pte`

.. image:: /images/error-viewer-01.png
   :align: center

To clear the error history, add a QPushButton and set the objectName to
`clear_errors_pb`.

To copy the errors to the clipboard, add a QPushButton and set the object name
to `copy_errors_pb`.

.. warning:: The error viewer must be a QPlainTextEdit not a QTextEdit.

Information Viewer
------------------

To add an information viewer, add a `QPlainTextEdit` from Input Widgets and name
it `info_pte`. Information messages from MSG, DEBUG and PRINT will show up in
the Information Viewer if it exists.

If `info_pte` is not found and the `errors_pte` is found, then information
messages will show up in the Error Viewer.

To clear the information viewer, add a QPushButton and name it `clear_info_pb`.

.. warning:: The information viewer must be a QPlainTextEdit not a QTextEdit.

Speed & Feed Calculators
------------------------

To add a milling Speeds and Feeds Calculator, add a `QFrame` or `QWidget` and
set the Object Name to `fsc_container`

.. image:: /images/fsc-02.png
   :align: center

To make the entry boxes touch-screen aware, add a Dynamic Property called 
`mode` and set the value to `touch`. Then when you touch an entry field, a 
numeric popup will show up to allow you to enter the value without a keyboard.
See :doc:`property`

.. image:: /images/fsc-01.png
   :align: center


To add a Drill Feed and Speed calculator, add a `QFrame` or `QWidget` and set
the Object Name to `dsf_container`.

To make the entry boxes touch-screen aware, add a Dynamic Property called 
`mode` and set the value to `touch`. Then when you touch it, a numeric popup 
will appear, allowing you to enter the numbers

.. image:: /images/dsc-01.png
   :align: center

Help System
-----------

A QPushButton can be setup to launch a Help dialog which contains text from a
file in the configuration directory. A help button can be placed on multiple
places with different file names. Only one Help dialog can be open at a time.

.. csv-table:: Help Button Dynamic Properties
   :width: 100%
   :align: left

	**Property Type**, **Property Name**, **Value**
	String, function, help
	String, file, file name
	String, topic, title of topic
	String, x_pos, x location of upper left corner
	String, y_pos, y location of upper left corner
	String, horz_size, width
	String, vert_size, height

.. note:: The x_pos is from the left edge of the screen and the y_pos is from
   the top of the screen.

Dynamic Properties

.. image:: /images/help-01.png
   :align: center

Help Dialog

.. image:: /images/help-02.png
   :align: center


