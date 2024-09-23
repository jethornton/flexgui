Probing
=======

Add a QPushButton named `probing_enable_pb` and if it is found it will be set as
a toggle button. The button will only be enabled when the machine is homed and
not running a program.

When the `probing_enable_pb` is toggled `OFF` any widget with an object name
that starts with `probe_` will be disabled.

When the `probing_enable_pb` is toggled `ON` the widgets that start with
`probe_` will be enabled. In addition spindle controls will disabled, spindle
speed set to 0, run controls will be disabled, MDI controls will be disabled.

You can create a HAL QDoubleSpinBox to use in your probing subroutine. If you're
using a touch screen add a Dynamic Property name `input` and set the value to
`touch`.
