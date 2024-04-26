Miscellaneous Items
===================

Plotter
-------

To add a path plotter add a QWidget or QFrame and name it `plot_widget`

G code Viewer
-------------

To add a G code viewer add a Plain Text Edit from Input Widgets and name it
`gcode_pte`.

MDI Viewer
----------

To add a MDI viewer add a List Widget from Item Widgets and name it
`mdi_history_lw`

To enter MDI commands add a Line Edit and name it `mdi_command_le`

Error Viewer
------------

To add an error viewer add a Plain Text Edit from Input Widgets and name it
`errors_pte`.



Print States
------------

For trouble shooting you can add a QCheckBox named `print_states_cb` and if it
is checked any state changes will print out in the terminal.
