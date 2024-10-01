Resources
=========

To create a resources.py file with images to use with the qss stylesheet start
by placing all the images in one directory.

Add the following library if not installed.
::

	sudo apt install qtbase5-dev-tools

Open up the Qt Designer and select the Resource Browser then Edit Resourses

.. image:: /images/resources-01.png
   :align: center

Create a New Resourses file and name it `resources.qrc`

.. image:: /images/resources-02.png
   :align: center

Add a prefix of `/`

.. image:: /images/resources-03.png
   :align: center

Add the image files

.. image:: /images/resources-04.png
   :align: center

Click on the first image then use shift and click on the last image to select
all the image files.

.. image:: /images/resources-05.png
   :align: center

Click on OK and you can close the Qt Designer.

.. image:: /images/resources-06.png
   :align: center


A second option is to just create a text file and name it `resources.qrc` and
add the following with a line for each file.
::

	<RCC>
	  <qresource prefix="/">
	    <file>name_of_image.png</file>
	    <file>inX+.png</file>
	  </qresource>
	</RCC>

.. note:: The name of the file between <file> and </file> must match exactly in
   the qss file plus a leading colon to use the internal resourses.py.

Example
::

	# resources.qrc file
	<file>inX+.png</file>

	/* your qss file */
	background-image: url(:inX+.png);

.. note:: The file name must start with : to use the internal resources.

Open a terminal in the directory where the images and the resourses.qrc file is
and use the following command to create the resourses.py file that is needed
to import the images into the GUI.
::

	rcc -g python -o resources.py resources.qrc

Edit the resourses.py file and replace 
::

	from PySide6 import QtCore

with
::

	from PyQt6 import QtCore

.. warning:: The resources file must be named resources.py in order to be imported

Now place the resources.py file in the configuration directory and edit the ini
file and add
::

	RESOURCES = resources.py

