GUI Tips
========

To group items together use a container like a QFrame, QGroupBox or a QTabWidget.

If the contents of a container are rows and columns after adding at least one
widget right click and select Layout > Lay Out in a Grid. Now you can drag and
drop widgets into the container. The blue line or red box indicate where it will
be placed.

.. image:: /images/tips-01.png
   :align: center

When using a grid layout for items that may change like Dro labels change the
text to represent the longest number including a minus sign if it could be
displayed. Next in the property editor look at the Width and select (I usually
use the column title) a widget and set the minimum width a tad bigger than the
widest widget in that column. This will prevent the column from resizing as the
values change.

For example the numbers in the Actual column can contain up to 8 characters like
-23.4567. In the next image no mininum width has been set

.. image:: /images/tips-02.png
   :align: center

All the cells in the colum will have the same width here you can see it has a
width of 44

.. image:: /images/tips-03.png
   :align: center

If we double click in the label and add -23.4567 the width changes to 61.

.. image:: /images/tips-04.png
   :align: center

I usually set the title of a column width to be a bit wider than the widest
widget in the column.

.. image:: /images/tips-05.png
   :align: center

