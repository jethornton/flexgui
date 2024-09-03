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

G code Viewer
-------------

To add a G code viewer add a Plain Text Edit from Input Widgets and name it
`gcode_pte`.

.. image:: /images/gcode-viewer-01.png
   :align: center

MDI Viewer
----------

To add a MDI viewer add a List Widget from Item Widgets and name it
`mdi_history_lw`

.. image:: /images/mdi-viewer-01.png
   :align: center

To enter MDI commands add a Line Edit and name it `mdi_command_le`

Error Viewer
------------

To add an error viewer add a QPlainTextEdit from Input Widgets and name it
`errors_pte`.

.. image:: /images/error-viewer-01.png
   :align: center

.. note:: See the :doc:`controls` section for buttons that pertain to the Error
   Viewer

Speed & Feed Calculators
------------------------

To add a milling Speed and Feed Calculator add a QFrame or QWidget and set the
Object Name to `fsc_container`

To make the entry boxes touch screen aware add a Dynamic Property called `mode`
and set the value to `touch`.

.. image:: /images/fsc-01.png
   :align: center

SFC calculator

.. image:: /images/fsc-02.png
   :align: center

To add a Drill Feed and Speed calculator add a QFrame or QWidget and set the
Object Name to `dsc_container`

.. image:: /images/dsc-01.png
   :align: center



