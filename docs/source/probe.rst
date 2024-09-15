Probing
=======

For probing buttons that use subroutines if you name them probe_something_pb and
replace something with the name of your choice. They will be disabled if the
spindle block checkbox is not checked.

Add a QCheckBox named `spindle_block_cb` and if
it is checked the spindle is set to 0 and off and any push button with an object
name that starts with `probe` will be enabled.

Add a QPushButton named `probe_block_pb`
