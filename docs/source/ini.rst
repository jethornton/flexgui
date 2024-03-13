INI Settings
============

.. note:: All settings are in the [DISPLAY] section of the ini file.

To use the Flex GUI change the DISPLAY value to:
::

	DISPLAY = flexgui

If no GUI is specificed then the default GUI will be used.

To use your ui file you created with the Qt Designer add the GUI key
::

	GUI = file-name.ui

To use the built in stylesheets add either
::

	INPUT = TOUCH
	INPUT = KEYBOARD

To use your style sheet put your stylesheet in the same directory as the
LinuxCNC configuration and add 
::

	QSS = file-name.qss

If no stylesheet is selected or entered then the default keyboard qss file will
be used.

.. note:: The user ui and qss files must be in the same LinuxCNC configuration
   directory as the ini file.

To control the initial size of the screen add either
::

	SIZE = minimized
	SIZE = normal
	SIZE = maximized
	SIZE = full

.. note:: Full size screen does not have any window controls. To close the app
  press `Ctrl Alt x` or select `File` > `Exit` from the menu if you added that
  action to the menu or make sure you add a Quit button somewhere before trying full.


