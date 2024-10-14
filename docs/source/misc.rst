Miscellaneous Items
===================

File Selector
-------------

Add a QListWidget and name it `file_lw`, this can be used with a touch screen by
specifying the touch input. A single left-click or touch is all that's needed to
use the `File Selector`. A left-click or touch on a directory will change to
that directory. A left-click or touch on the up or down arrow will move the list
by one. A left-click or touch inbetween an arrow and the slider will move the
list by one page. Touch-and-hold to move the slider.

If you use the touch input, the selector looks like this

.. image:: /images/file-selector-01.png
   :align: center

.. note:: Make sure you use a QListWidget and not a QListView for the file
   selector.

G-code Viewer
-------------

To add a G-code viewer, add a Plain Text Edit from Input Widgets and name it
`G-code_pte`

.. image:: /images/gcode-viewer-01.png
   :align: center

MDI Viewer
----------

To add a MDI viewer, add a List Widget from Item Widgets and name it
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

To add a milling Speeds and Feeds Calculator, add a QFrame or QWidget and set 
the Object Name to `fsc_container`

.. image:: /images/fsc-02.png
   :align: center

To make the entry boxes touch-screen aware, add a Dynamic Property called 
`mode` and set the value to `touch`. Then when you touch an entry field, a 
numeric popup will show up to allow you to enter the value without a keyboard.

.. image:: /images/fsc-01.png
   :align: center


To add a Drill Feed and Speed calculator, add a QFrame or QWidget and set the 
Object Name to `dsf_container`.

To make the entry boxes touch-screen aware, add a Dynamic Property called 
`mode` and set the value to `touch`. Then when you touch it, a numeric popup 
will appear, allowing you to enter the numbers

.. image:: /images/dsc-01.png
   :align: center

