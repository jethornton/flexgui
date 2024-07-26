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

.. note:: If a qss file is specified then input and theme are not used

To use the built in input stylesheets add either
::

	INPUT = TOUCH
	INPUT = KEYBOARD

.. note:: If no INPUT or QSS is specified then no qss file will be used.

To use the built in dark theme an INPUT must be specified.
::

	THEME = DARK

The ile selector defaults to `.ngc` (any case) to add more extensions add
EXTENSIONS with other g code extensions seperated by a comma. The extensions
must be in the form `.ext` with the leading dot.
::

	EXTENSIONS = .nc, .gcode, .xt

To control the initial size of the screen add either
::

	SIZE = minimized
	SIZE = normal
	SIZE = maximized
	SIZE = full

.. warning:: Full size screen does not have any window controls. Make sure there
   is a way to close the GUI like an Exit button or you will not be able to
   close the application.


