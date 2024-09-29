INI Settings
============

.. note:: All settings are in the [DISPLAY] section of the ini file.

Display Settings
----------------

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

Open File
---------

To open a file on startup add the OPEN_FILE item with either the full path to
the G code file or you can use ~/ for the user home direcory or ./ if the file
is in the configuration directory.
::

	OPEN_FILE = /home/john/linuxcnc/configs/flex_examples/probe_sim/square.ngc
	or
	OPEN_FILE = ~/linuxcnc/configs/flex_examples/probe_sim/square.ngc
	or
	OPEN_FILE = ./square.ngc

Resource File
-------------

To use a resources file to add images to buttons with your qss stylesheet place
the resource file in the configuration directory and add the following line to
the ini file.
::

	RESOURCES = resources.py

Stylesheets
-----------

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

Colors
------

The E-Stop and Power Buttons can have a static color for E-Stop Open and or
Closed and the Power Button can have a static color for Power Off and or On.

Create a section in the ini file called FLEX_COLORS and use the following to
control the static color of these items. The value can be any valid color
specification, it's suggested you use the RGB or Hex colors.
::

	[FLEX_COLORS]
	ESTOP_OPEN = rgb(128, 255, 128)
	ESTOP_CLOSED = rgb(255, 77, 77)
	POWER_OFF = rgb(255, 128, 128)
	POWER_ON = rgb(0, 255, 0)

