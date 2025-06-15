Building a GUI
==============

If you have not copied the examples from the CNC menu select Copy Flex Examples.
This will put the Flex examples in linuxcnc/configs/flex_examples.

The starters have all the files needed to run a simulation without complicated
code. The starters have a very simple GUI to start, just enough to show you that
they work.

Copy a Starter
--------------

From the linuxcnc/configs/flex_examples/starters copy one of the starter types
to the linuxcnc/configs directory.

* Rename the directory to the name of your choice.
* Rename the .ui and .ini files to the name of your choice.
* Edit the .ini file and change the GUI to the name of your .ui file.
* Edit the MIN_LIMIT and MAX_LIMIT for each axis and joint to match your machine
* From the CNC menu select LinuxCNC and pick your configuration, check Create
  Desktop Shortcut then clidk OK to run your configuration.

.. figure:: /images/build-01.png
   :align: center

   Mill Starter Example

