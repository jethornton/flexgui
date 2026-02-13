INI Settings
============

`Video Tutorial <https://youtu.be/JQXG9I7fwSo>`_

.. _using_flexgui:

[EMC]
-----

The optional DEBUG key in the [EMC] section can be used to show various levels
of debug information when running in a terminal. The DEBUG key is not required.
::

	DEBUG = option number

Debug Options

.. code-block:: text

	EMC_DEBUG_CONFIG               2
	EMC_DEBUG_VERSIONS             8
	EMC_DEBUG_TASK_ISSUE          10
	EMC_DEBUG_NML                 40
	EMC_DEBUG_MOTION_TIME         80
	EMC_DEBUG_INTERP             100
	EMC_DEBUG_RCS                200
	EMC_DEBUG_INTERP_LIST        800
	EMC_DEBUG_IOCONTROL         1000
	EMC_DEBUG_OWORD             2000
	EMC_DEBUG_REMAP             4000
	EMC_DEBUG_PYTHON            8000
	EMC_DEBUG_NAMEDPARAM       10000
	EMC_DEBUG_GDBONSIGNAL      20000
	EMC_DEBUG_STATE_TAGS       80000
	EMC_DEBUG_UNCONDITIONAL 40000000
	EMC_DEBUG_ALL           7FFFFFFF

[DISPLAY]
---------

Flex GUI
--------

To use the Flex GUI (as opposed to Axis or others), change the DISPLAY value to

.. code-block:: text

	DISPLAY = flexgui

If no GUI is specified then the default GUI will be used.

.. note:: Any Flex GUI .ui and .qss files must be in the same LinuxCNC
   configuration directory as the .ini file.

To use your .ui file (created with Qt Designer), add a GUI key to the .ini
with its `filename`:

.. code-block:: text

	GUI = my-file-name.ui

Jog Increments
--------------

The following settings can be used in the [DISPLAY] section of the ini file to
preset jog items. While you can mix units usually machine units are used. Units
can be mm, cm, um, in, inch, mil or left out. A space can be between the
distance and the units for better readability. Fractions are are in inch units
and can be a whole number with a space then the fraction.

.. code-block:: text

	INCREMENTS = 1/2, 0.100, 0.010, 0.001
	or
	INCREMENTS = 1 1/2, 1 inch, 0.5 in, 1 cm, 1 mm
	MIN_LINEAR_VELOCITY = 0.1
	MAX_LINEAR_VELOCITY = 1.0
	DEFAULT_LINEAR_VELOCITY = 0.2

.. warning:: [DISPLAY] INCREMENTS must be a comma seperated list or it will be
   ignored.

.. note:: Jog incremnts can have unit labels, the following are valid unit
   labels cm, mm, um, inch, in or mil. If no unit labels are found the the
   configuration units are used.

Startup File
------------

To automatically open a NC file on startup, add the OPEN_FILE key with any
valid path. Use ~/ as a shortcut to the users home directory. Use ./ to indicate
that the file is in the configuration directory
::

	Full Path to the file
	OPEN_FILE = /home/john/linuxcnc/configs/myconfig/welcome.ngc
	or use the ~ for the users home directory
	OPEN_FILE = ~/linuxcnc/configs/flex_examples/probe_sim/square.ngc
	or use the ./ to use the current configuration directory
	OPEN_FILE = ./welcome.ngc
	or use the ../ to use the parent directory of the configuration
	OPEN_FILE = ../welcome.ngc

File Location
-------------

Likewise, to specify a default location for NC files, add the PROGRAM_PREFIX
item.

.. code-block:: text

	PROGRAM_PREFIX = /home/john/linuxcnc/configs/myconfig
	or
	PROGRAM_PREFIX = ~/linuxcnc/configs/flex_examples/probe_sim
	or
	PROGRAM_PREFIX = ./
	or
	PROGRAM_PREFIX = ../

Tool Table Editor
-----------------

To specify a different tool table editor add an entry to the [DISPLAY] section.
If no entry is found then the default tool editor is used

.. code-block:: text

	TOOL_EDITOR = tooledit

To control the columns displayed by the default tool editor add any of the valid
column specifiers separated by a space. 

.. code-block:: text

	TOOL_EDITOR = tooledit x y z a b c u v w diam front back orien

If no entry is found then the axes in the configuration and diameter are shown.
Tool, Pocket and Comment are always shown.

File Extensions
---------------

The keyboard file dialog defaults to `*.ngc` and this ignores case. To
specify the file extensions you want the file dialog to show, add an
EXTENSIONS key with the desired extensions separated by a comma. The
extensions must be in the format `*.ext` with the asterisk and dot

.. code-block:: text

	EXTENSIONS = `*.nc`, `*.G-code`, `*.ngc`, `*.txt`

[FLEXGUI]
---------

Splash Screen
-------------

You can add a splash screen with custom title and time to flex. The image file
name is the only required item. If title and time are not specified then the
default `Flex Dragon Slayer` and 5 seconds are used. The image file must be in
the configuration directory. If the image is a jpg you might have to open it in
GIMP and save it as png if it does not show up. If the font is not an exact
match the nearest font will be used. Some fixed width fonts are Monospace and
Courier. Some variable width fonts are Cantarell and Serif. Font colors are
simple base colors only.

.. code-block:: text

	SPLASH_IMAGE = name.png
	SPLASH_TITLE = Flex
	SPLASH_TIME = 10
	SPLASH_FONT = Name of Font
	SPLASH_FONT_SIZE = 12
	SPLASH_FONT_BOLD = True or False
	SPLASH_FONT_COLOR = black

.. _installed_themes:

Themes
------

Themes are just style sheets that get applied to the widgets. The theme files
are in the themes directory of the example files if you want to copy and
customize one of the themes.

.. code-block:: text

	blue.qss
	blue-touch.qss
	dark.qss
	dark-touch.qss
	keyboard.qss
	touch.qss

To use a built-in theme with no color changes add one of the following to the
[FLEXGUI] section of the ini file.

.. code-block:: text

	THEME = touch
	THEME = keyboard

To use a built in theme with coloring add one of the following to the
[FLEXGUI] section of the ini file.

.. code-block:: text

	THEME = blue
	THEME = blue-touch
	THEME = dark
	THEME = dark-touch

.. note:: Touch themes use tabs set to South for rounding and non touch use tabs
   set to North.

.. note:: THEME is checked first then QSS so the first entry found is used.

To use a custom .qss style sheet you created add the name of the stylesheet to
the QSS option in [FLEXGUI] section of the ini file.

.. code-block:: text

	QSS = name_of_stylesheet.qss

For more information on style sheets see :doc:`style`

.. _jog-increments:


Resource File
-------------

To use a .py resource file (to add images to buttons with your qss stylesheet)
place the .py resource file in the configuration directory and add the
following line to the .ini file
::

	RESOURCES = resources.py

See the section on Resources for more info.

Screen Size
-----------

To control the initial size of the screen, add of the following values.

.. code-block:: text

	SIZE = minimized
	SIZE = normal
	SIZE = maximized
	SIZE = full
	SIZE = rpi_full

.. NOTE:: the values are case sensitive

.. NOTE:: The Raspberry Pi 5 with Wayland needs to use the rpi_full value

.. warning:: Full size screen does not have any window controls. Make sure
   there is a way to close the GUI like an Exit button or you may not be able to
   close the application. As a last-resort, pressing ALT-F4 will close it.

.. _plotter:

Plotter
-------

The plotter background color can be set in the [FLEXGUI] section of the ini. The
value is the Red,Green,Blue color numbers from 0 to 1 with no space. So an entry
of 0.0,0.0,0.0 is black and 1.0,1.0,1.0 is white. Use a RGB 0-1 Color Picker to
select the RGB values.

.. code-block:: text

	[FLEXGUI]
	PLOT_BACKGROUND_COLOR = 0.0,0.0,0.0

The plotter orientation can be set to one of the following x, x2, y, y2, z, or p.

.. code-block:: text

	[FLEXGUI]
	PLOT_VIEW = x

The font size for the plotter can be set in the ini by adding the following to
the FLEXGUI section. The font size must be an integer.

.. code-block:: text

	[FLEXGUI]
	DRO_FONT_SIZE = 12

The plotter DRO can be set to automatically change units when the program units
G20/G21 change. Setting to `True` disables the manual unit change controls.

.. code-block:: text

	PLOT_UNITS = True

The plot grid sizes are set in the ini file. Fraction and decimal numbers are
valid. Fractions are always in Inch units. Valid suffixes are `mm`, `cm`, `um`,
`in`, `inch`, `mil`. If fraction does not have a suffix then `inch` will be
added as the suffix. If no suffix is found the the machine units suffix will be
added. If the size does not have a valid suffix or is not a number it will be
skipped and a warning will appear.

.. code-block:: text

	PLOT_GRID = 1/2, 1 in, 1 1/2, 2 inch
	or for metric
	PLOT_GRID = 10mm, 20mm, 50mm, 100mm

The first item in the list will be considered the default and set when FlexGUI
starts. If you wish disable grid by default, add a `0` item to the beginning of
the list.

DRO
---

To set the DRO labels to follow the program units add the following

.. code-block:: text

	DRO_UNITS = True

.. _led_defaults:

LED Defaults
------------

LED buttons can have defaults set in the ini file. This makes it easier to have
consistent LED size, position and colors. These options go in the [FLEXGUI]
section.

The color options can be specified using HEX, RGB or RGBA.

Valid RGB(A) Red, Green, Blue (Alpha) values are 0 to 255.

Valid HEX values are #000000 to #ffffff

In PyQt6 the Alpha channel is 0 to 255. 0 represents a fully transparent color,
while 255 represents a fully opaque color. If Alpha is ommitted then it's set to
fully opaque or 255.

The Diameter and Offset values are whole numbers only.

.. code-block:: text

	[FLEXGUI]
	LED_DIAMETER = 15
	LED_RIGHT_OFFSET = 5
	LED_TOP_OFFSET = 5
	LED_ON_COLOR = 0, 255, 0
	LED_OFF_COLOR= 125, 0, 0, 255

For more information on LED buttons see :ref:`LedButtons`

.. _touch_ini:

Touch Screens
-------------

Options for touch screen users.

To set the style sheet used by the popup number pad, NC code pad and popup
keyboard add the following to the FLEXGUI section with the name of the QSS
stylesheet to use.

.. code-block:: text

	[FLEXGUI]
	POPUP_QSS = somefile.qss

Set the touch screen file chooser to automatically adjust the width by adding the
following to the FLEXGUI section.

.. code-block:: text

	[FLEXGUI]
	TOUCH_FILE_WIDTH = True

Add popup keypad to all spin boxes.

.. code-block:: text

	[FLEXGUI]
	TOUCH_SPINBOX = True


To add a manual tool change popup to add the following to the ini file in the
[FLEXGUI] section.

.. code-block:: text

	[FLEXGUI]
	MANUAL_TOOL_CHANGE = True


