INI Settings
============

.. note:: The following Flex GUI settings are all located in the [DISPLAY]
   section of your LinuxCNC .ini file.

To use the Flex GUI (as opposed to Axis or others), change the DISPLAY value to
::

	DISPLAY = flexgui

If no GUI is specificed then the default GUI will be used.

.. note:: Any Flex GUI .ui and .qss files must be in the same LinuxCNC
   configuration directory as the .ini file.

To use your .ui file (created with Qt Designer), add a GUI key to the .ini
with its `filename`:
::

	GUI = my-file-name.ui

Stylesheets
-----------

To use a built-in input stylesheet, add either
::

	INPUT = TOUCH
	or
	INPUT = KEYBOARD

.. note:: If no INPUT nor QSS is specified, then no stylesheet will be used.

To use a custom .qss style sheet you created named `lightflex.qss`
::

	QSS = lightflex.qss

.. note:: If a QSS file is specified, `INPUT` and `THEME` are ignored.

Startup File
------------

To automatically open a NC file on startup, add the OPEN_FILE key with any
valid path. Use ~/ as a shortcut to the users home directory. Use ./ to indicate
that the file is in the configuration directory
::

	OPEN_FILE = /home/john/linuxcnc/configs/myconfig/welcome.ngc
	or
	OPEN_FILE = ~/linuxcnc/configs/flex_examples/probe_sim/square.ngc
	or
	OPEN_FILE = ./welcome.ngc

File Location
-------------

Likewise, to specify a default loction for NC files, add the PROGRAM_PREFIX
item.
::

	PROGRAM_PREFIX = /home/john/linuxcnc/configs/myconfig
	or
	PROGRAM_PREFIX = ~/linuxcnc/configs/flex_examples/probe_sim
	or
	PROGRAM_PREFIX = ./

Resource File
-------------

To use a .py resource file (to add images to buttons with your qss stylesheet)
place the .py resource file in the configuration directory and add the
following line to the .ini file
::

	RESOURCES = resources.py

See the section on Resources for more info.


File Extensions
---------------

The keyboard file dialog defaults to `*.ngc` and this ignores case. To
specify the file extensions you want the file dialog to show, add an
EXTENSIONS key with the desired extensions seperated by a comma. The
extensions must be in the format `*.ext` with the asterisk and dot
::

	EXTENSIONS = *.nc, *.G-code, *.ngc, *.txt

To control the initial size of the screen, add either:
::

	SIZE = minimized
	SIZE = normal
	SIZE = maximized
	SIZE = full

.. warning:: Full size screen does not have any window controls. Make sure
   there is a way to close the GUI like an Exit button or you may not be able to
   close the application. As a last-resort, pressing ALT-F4 will close it.

Colors
------

The E-Stop and Power Buttons can have a static color for Open and Closed. The
Power Button can have a static color for Off and On.

Create a key in the ini file called FLEX_COLORS and use the following to 
control the static color of these items. The value can be any valid color 
specification; it's suggested to use RGB or Hex colors:
::

	[FLEX_COLORS]
	ESTOP_OPEN = rgb(128, 255, 128)
	ESTOP_CLOSED = rgb(255, 77, 77)
	POWER_OFF = rgb(255, 128, 128)
	POWER_ON = #00FF00

Another way to achieve this is is via adding and editing a .qss stylesheet
file. See the :doc:`style` section for more info.
