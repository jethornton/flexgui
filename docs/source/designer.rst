Qt Designer
===========

Installing the Qt Designer
--------------------------

In a terminal install the Qt Designer with:
::

	sudo apt install qttools5-dev-tools

.. note:: The Qt6 Designer is not needed, the Qt5 Designer works fine.

Building a GUI
--------------

Run the Qt Designer from the Applications > Programming menu and create a new
Main Window.

.. image:: /images/designer-01.png
   :align: center

To add a Tool Bar right click and select Tool Bar

.. image:: /images/designer-02.png
   :align: center

To add a Menu type in the menu area and press enter.

To add a Menu item type in the menu and press enter.

.. image:: /images/designer-03.png
   :align: center

When you create a Menu item it creates and action, the action can be dragged to
the Tool Bar to create a tool bar button.

.. image:: /images/designer-04.png
   :align: center


Adding items from the Widget Box is drag and drop. To create a basic layout from
Containers add two Frames and a Tab Widget.

.. image:: /images/designer-05.png
   :align: center

Right click in the QMainWindow and select Lay out > Lay out Vertically.

.. image:: /images/designer-06.png
   :align: center

.. image:: /images/designer-07.png
   :align: center

Add a Push Button to the QFrame then right click on the frame or the QFrame in
the Object Inspector and set the lay out to grid.

.. image:: /images/designer-08.png
   :align: center

.. image:: /images/designer-09.png
   :align: center


After dragging a widget into the window make sure you use the correct
objectName for that widget. For example the E Stop button is called estop_pb.

Save the GUI in the configuration directory where you launch LinuxCNC.
