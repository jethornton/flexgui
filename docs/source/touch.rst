Touch Screens
=============

Some entry widgets like MDI and Touch Off have a touch screen popup available to
make it easier to use a Touch Screen.

Tool Bar
--------

To add a button to the tool bar without having a menu item that creates an
action you just have to create an action yourself.

.. image:: /images/new-action-01.png
   :align: center

The action creating window, when you type in the Text name the Object name is
created for you.

.. image:: /images/new-action-02.png
   :align: center

.. warning:: Make sure the Object name matches the Action Name created when you
   create a menu item see the :doc:`menu` section for the Action Names.

Now you just drag the action into the tool bar to create a new tool bar button.

.. image:: /images/new-action-03.png
   :align: center

MDI
---

To enable the G code popup for the MDI entry add a Dynamic Property called
`input` to the and set the value to `touch`.

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

The Coordinate System Touch Off offset is a QLineEdit named `touchoff_le`.
To enable the number pad popup for the offset entry add a Dynamic Property
called `input` to the and set the value to `touch`.

.. image:: /images/touch-04.png
   :align: center

Touch Off

.. image:: /images/touch-05.png
   :align: center

Tool Touch Off
--------------

The Tool Touch Off offset is a QLineEdit named `tool_touchoff_le`.
To enable the number pad popup for the offset entry add a Dynamic Property
called `input` to the and set the value to `touch`.

Spin Boxes
----------
QDoubleSpinBox and QSpinBox can use the popup numbers keypad by adding a Dynamic
Property called `input` to the and seting the value to `touch`.

