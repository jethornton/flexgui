Miscellaneous Items
===================

File Selector
-------------

Add a QListWidget and name it `file_lw`, this can be used with a touch screen by
specifying the touch input. A single left click or touch is all that's needed to
use the `File Selector`. A left click or touch on a directory will change to
that directory. A left click or touch on the up or down arrow will move the list
by one. A left click or touch in between an arrow and the slider will move the
list by one page. Touch and hold to move the slider.

If you use the touch input the selector looks like this.

.. image:: /images/file-selector-01.png
   :align: center

.. note:: Make sure you use a QListWidget and not a QListView for the file selector 

Plotter
-------

To add a path plotter add a QWidget or QFrame and name it `plot_widget`

.. note:: The plot widget is under construction and not working at this point.

G code Viewer
-------------

To add a G code viewer add a Plain Text Edit from Input Widgets and name it
`gcode_pte`.

MDI Viewer
----------

To add a MDI viewer add a List Widget from Item Widgets and name it
`mdi_history_lw`

To enter MDI commands add a Line Edit and name it `mdi_command_le`

Error Viewer
------------

To add an error viewer add a Plain Text Edit from Input Widgets and name it
`errors_pte`.

