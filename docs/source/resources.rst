Resources
=========

To create a resources.py file with images to use with the .qss stylesheet, start
by placing all the images in a different directory than the configuration files.
A subdirectory in the configuration directory is fine
::

	└── configs
	   └── my_mill
	       └── images

Add the following library if not installed
::

	sudo apt install qtbase5-dev-tools

After installing Flex GUI on the CNC menu run `Flex Resources`

.. image:: /images/resources-00.png
   :align: center

Startup

.. image:: /images/resources-01.png
   :align: center

Next Select Images Directory

.. image:: /images/resources-02.png
   :align: center

The selected directory is shown in the label

.. image:: /images/resources-03.png
   :align: center

Next Select Image Files. To select all the images left click on the first one
and hold down the shift key and left click on the last one. To pick several
images but not all hold down the ctrl key while you left click on each one.

.. image:: /images/resources-04.png
   :align: center

The images selected are shown below

.. image:: /images/resources-05.png
   :align: center

Next Build QRC File

.. image:: /images/resources-06.png
   :align: center

Next Select Config Directory

.. image:: /images/resources-07.png
   :align: center

.. note:: The Image directory and the configuration directory must be different

Next Build Resources File

.. image:: /images/resources-08.png
   :align: center

The Flex Resourse Builder can be closed now. In the configuration directory you
will have a resources.py file that contains the images used by the stylesheet.

Next edit the ini file and in the [FLEX] section add the following line
::

	RESOURCES = resources.py

In the [DISPLAY] section add the style sheet
::

	QSS = xyz.qss

To add an image named my-image.png to a QPushButton with an object name of
my_pb add the following to the qss file
::

	QPushButton#my_pb {
		min-height: 80px;
		min-width: 80px;
		margin: 2px;
		background-position: center;
		background-origin: content;
		background-clip: padding;
		background-repeat: no-repeat;
		background-image: url(:my-image.png);
	}

Now when you run the configuration the image will be on the QPushButton

.. image:: /images/resources-09.png
   :align: center

.. note:: Delete any text in the QPushButton or it will be on top of the image
