INI Settings
============

.. note:: All settings are in the [DISPLAY] section of the ini file.

To use the Flex GUI change the DISPLAY value to:
::

	DISPLAY = flexgui

If no GUI is specificed then the default GUI will be used.

.. note:: The user ui and qss files must be in the same LinuxCNC configuration
   directory as the ini file.

To use your ui file you created with the Qt Designer add the GUI key with
`file-name` being the name of your .ui file.
::

	GUI = file-name.ui

To use your style sheet add with `file-name` being the name of your .qss file.
::

	QSS = file-name.qss

To use the built in stylesheets add either
::

	INPUT = TOUCH
	INPUT = KEYBOARD

If no stylesheet is selected or entered then the default keyboard qss file will
be used.

To control the initial size of the screen add either
::

	SIZE = minimized
	SIZE = normal
	SIZE = maximized
	SIZE = full

.. warning:: Full size screen does not have any window controls. To close the app
  press `Ctrl Alt x` or select `File` > `Exit` from the menu if you added that
  action to the menu or make sure you add a Quit button somewhere before trying full.


