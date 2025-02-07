GUI Tips
========

To group items together, use a container like a QFrame, QGroupBox or a
QTabWidget.

If the contents of a container are rows and columns after adding at least one
widget, right click and select `Layout` then `Lay Out in a Grid`. Now you can
drag and drop widgets into the container. The blue line or red box indicate
where it will be placed in the grid.

.. image:: /images/tips-01.png
   :align: center

When using a grid layout for items that may change like Dro labels, change the
text to represent the longest number including a minus sign. Next, in the
property editor look at the Width and select (I usually use the column title) a
widget and set the minimum width a tad bigger than the widest widget in that
column. This will prevent the column from resizing as the values change.

For example, the numbers in the Actual column can contain up to 8 characters
like -23.4567. In the next image no mininum width has been set

.. image:: /images/tips-02.png
   :align: center

All the cells in the column will have the same width - here you can see it has a
width of 44

.. image:: /images/tips-03.png
   :align: center

If we double-click in the label and add -23.4567 the width changes to 61

.. image:: /images/tips-04.png
   :align: center

I usually set the title of a column width to be a bit wider than the widest
widget in the column

.. image:: /images/tips-05.png
   :align: center

If you drag a container into another container that has a layout and it's real
short, just set the minimum height to make it larger and easier to drag and drop
into.

Ctrl + left click to select several widgets at once to change all their
properties.

The Monospace font is good for numbers that need a fixed width like DRO values.
