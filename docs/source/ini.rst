INI Settings
============

To test on simulated hardware create a configuration with the Step Configuration
Wizard then modify the ini file.

.. note:: All settings are in the [DISPLAY] section of the ini file.

To use the Flex PyQt6 GUI set `DISPLAY = jet` after installing (this will be
changed to `flex` soon. If no GUI is specificed then the default GUI will be used.

To use your ui file you created with the Qt Designer add `GUI = file-name.ui`
if not entered then the default ui file will be used.

To use the built in stylesheets add `INPUT = TOUCH` or `INPUT = KEYBOARD`

To use your style sheet add `QSS = file-name.qss` and put your stylesheet in the
same directory as the configuration.

If no stylesheet is selected or entered then the default keyboard qss file will
be used.

.. note:: The user ui and qss files must be in the configuration directory.

To control the initial size of the screen add `SIZE = minimized`, `normal`,
`maximized` or `full`.

.. note:: Full size screen does not have any window controls. To close the app
  there is a button on the status page.

To exit from full screen press `Ctrl Alt x` or select `File` > `Exit` from the
menu if you added that action to the menu or press the lower right corner of the
status tab.

