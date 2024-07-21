Touch Screens
=============

Some entry widgets like MDI and Touch Off have a touch screen popup available to
make it easier to use a Touch Screen.

MDI
---

To enable the G code popup for the MDI entry add a Dynamic Property called
`mode` and set the value to `touch`.

.. image:: /images/touch-01.png
   :align: center

The G code Dialog will appear when you touch the MDI entry box.

.. image:: /images/touch-02.png
   :align: center

The Arrow Buttons change the bottom section to different letters.

.. image:: /images/touch-03.png
   :align: center

Touch Off
---------

The Coordinate System Touch Off can have either a QDoubleSpinBox or a QLineEdit.
A QLineEdit named `touchoff_le` is used when you have a Touch Screen and you
want the Number Popup when you touch it.

.. image:: /images/touch-04.png
   :align: center

Touch Off

.. image:: /images/touch-05.png
   :align: center

Tool Touch Off
--------------

Working on this...

File Selector
-------------

Add a QListWidget and name it `file_lw`, this is typicly used with a touch
screen. A single left click or touch is all that's needed to use the `File
Selector`. A left click or touch on a directory will change to that directory.
A left click or touch on the up or down arrow will move the list by one. A left
click or touch inbetween an arrow and the slider will move the list by one page.
Touch and hold to move the slider.

.. image:: /images/file-selector-01.png
   :align: center

.. note:: Make sure you use a QListWidget and not a QListView for the file selector 
