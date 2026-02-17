HAL Pins
========
`HAL Tutorial <https://youtu.be/LU4914GyGXI>`_

Creating widgets that connect to HAL (Hardware Abstract Layer) is as simple as
adding a few Dynamic Properties. See :doc:`property` for step by step
instructions to add a Dynamic Property.

Typically the Dynamic Properties are String type with some exceptions being Bool
and Color. Connections from Flex HAL objects to other HAL objects must be done
in the file assigned to the POSTGUI_HALFILE variable in the [HAL] section
typically named `postgui.hal`.

.. code-block:: text

	[HAL]
	HALFILE = main.hal
	POSTGUI_HALFILE = postgui.hal

The property `pin_name` defines the HAL pin name that is prefixed with
`flexhal`. A pin_name of my-button would be `flexhal.my-button` in HAL.

.. note:: Dynamic Property names are case sensitive and must be all lower case.
   Hal types and directions are case sensitive and must be all caps. The
   function value must be lower case.

.. note:: Hal pin names can containe a-z, A-Z, 0-9, underscore _, or dash -. Use
   a dash to not conflict with program variables of the same name which use an
   underscore.

Options
-------

The default behavior for HAL objects that are a HAL_OUT or HAL_IO is to be
enabled when the E Stop is released. To change this behaviour add a Dynamic
Property to control when the HAL object is enabled. The `state_on` property will
enable the control when the power is on. The `all_homed` property will enable
the control when all joints are homed. They can be combined to make a HAL object
only enabled when power is on and all joints are homed.

.. csv-table:: HAL Options
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	Bool, state_on, True
	Bool, all_homed, True

HAL Button
----------

A QPushButton, QCheckBox or QRadioButton can be assigned to a HAL `bit` pin by
adding two string type Dynamic Properties. A pin_name of my-button would be
`flexhal.my-button` in HAL. HAL pins must be connected in the postgui.hal file.

The HAL direction is OUT and the HAL type is bit for a QPushButton, QCheckBox or
QRadioButton.

The option always_on will not disable the HAL Button for any state.

The option state_on will disable the HAL Button until the Power is on.

The option all_homed will disable the HAL Button until all joints are homed.

The option confirm can be used with a checkable QPushButton or QCheckBox.
When toggled a popup will ask for confirmation of the action. If Cancel is
selected the checked state will be set back to the previous state and the HAL
pin will not change.

.. csv-table:: HAL Push Button
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_pin
	String, pin_name, any unique name
	Optional
	Bool, always_on, True
	Bool, state_on, True
	Bool, all_homed, True
	Bool, confirm, True

.. image:: /images/hal-09.png
   :align: center

.. warning:: By default, no QRadioButtons are checked unless you set one checked
   in the Designer. Starting up with none checked could be a problem if you
   expect one to be selected at startup.

.. _SpinBoxTag:

HAL LED Button
--------------

A QPushButton can be a HAL LED button by adding two dynamic properties. The
`pin_name` property will be the HAL pin name you use to connect the button state
in the postgui.hal file. The button can be momentary or checkable. The default
colors are Red when Off and Green when On. The default shape is round.

The HAL direction is OUT and the HAL type is bit for a HAL LED QPushButton.

The option always_on will not disable the HAL LED Button for any state.

The option state_on will disable the HAL LED Button until the Power is on.

The option all_homed will disable the HAL LED Button until all joints are homed.

.. csv-table:: HAL LED Button Dynamic Properties
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_led_button
	String, pin_name, any unique name
	Optional
	Bool, always_on, True
	Bool, state_on, True
	Bool, all_homed, True
	String, led_shape, square

HAL Spinbox
-----------

A QSpinBox can be a HAL `number` pin by adding three string
type Dynamic Properties. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-spinbox would be in HAL `flexhal.my-spinbox`. The
spinbox is an Out type that will set the value of the HAL pin to match the
value of the spinbox.

The HAL direction is OUT for a HAL Spinbox.

.. csv-table:: HAL Spin Box
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_pin
	String, pin_name, any unique name
	String, hal_type, HAL_S32 or HAL_U32
	Optional
	Bool, state_on, True
	Bool, all_homed, True

HAL Double Spinbox
------------------

A QDoubleSpinBox can be a HAL `number` pin by adding two string
type Dynamic Properties. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-spinbox would be in HAL `flexhal.my-spinbox`. The
spinbox is an Out type that will set the value of the HAL pin to match the
value of the spinbox.

The HAL direction is OUT and the HAL type is float for a HAL Double Spinbox.

.. csv-table:: HAL Spin Box
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_pin
	String, pin_name, any unique name
	Optional
	Bool, state_on, True
	Bool, all_homed, True

HAL Slider
----------

A QSlider can be a HAL pin by adding these three string type Dynamic Properties.
The pin_name used will create a HAL pin prefixed with `flexhal.` A pin_name of
my-slider would be in HAL `flexhal.my-slider`. A QSlider supports only integers
so to connect it to a float HAL pin use conv_s32_float or conv_u32_float.

The HAL direction is OUT for a HAL Slider.

See :doc:`property` for step by step instructions to add a Dynamic Property

.. csv-table:: HAL Slider
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_pin
	String, pin_name, any unique name
	String, hal_type, HAL_S32 or HAL_U32
	Optional
	Bool, state_on, True
	Bool, all_homed, True

HAL I/O
-------

A HAL I/O object has an input and output on the same pin. The pin can set an
input pin of another HAL object and the pin can be set by another HAL object
output pin. The HAL I/O will stay synchronized with the pin it's connected to.

.. NOTE:: The connected pins must be of the same HAL type.

A QPushButton (set to checkable), QCheckBox, QRadioButton, QSpinBox,
QDoubleSpinBox or a QSlider can be a HAL I/O object.

The HAL direction is I/O and the HAL type is bit for QPushButton, QCheckBox or
QRadioButton.

The HAL direction is I/O for a HAL I/O QSpinBox.

The HAL direction is I/O and the HAL type is float for a HAL I/O QDoubleSpinBox.


.. NOTE:: The hal_type for QSpindBox and QSlider must be specified.

.. csv-table:: HAL I/O
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_io
	String, pin_name, any unique name
	For a QSpinBox or QSlider
	String, hal_type, HAL_S32 or HAL_U32
	Optional
	Bool, state_on, True
	Bool, all_homed, True

.. NOTE:: The hal_type is required for QSpinBox, QSlider or QDoubleSpinBox

HAL Label
---------

A QLabel can be used to monitor HAL pins. HAL connections must be made in the
post gui HAL file. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-reader would be `flexhal.my-reader` in HAL.

The HAL direction is IN for a HAL Label.

.. csv-table:: HAL Label
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_pin
	String, pin_name, any unique name
	String, hal_type, HAL_BIT or HAL_FLOAT or HAL_S32 or HAL_U32
	Optional
	String, precision, Number of decimal digits for HAL_FLOAT type
	String, integer_digits, Number of left pad zeros for HAL_S32 or HAL_U32

HAL Average Float Label
-----------------------

A QLabel can be used to monitor HAL float number pins and display an average of
the number of samples. The sample stack is LIFO so a new value pushes the oldest
value out of the stack. This could be useful to display RPM from a spindle
encoder or any numeric value that changes.

The `samples` option can change the number of samples that are averaged out to
help smooth the display output.

The `rounding` option can be used to round the number. Use 1 to round to the
nearest tenth and 2 to round to the nearest hundred, etc.

The `precision` option is used to set the number of decimal places. Set to 0
to not have any decimal places.

HAL connections must be made in the post gui HAL file. The pin_name used will
create a HAL pin prefixed with `flexhal.` A pin_name of my-reader would be
`flexhal.my-reader` in HAL.

The HAL direction is IN and the hal_type is float for a HAL Average Float Label.

.. csv-table:: HAL Average Float Label
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_avr_f
	String, pin_name, any unique name
	Optional
	Int, samples, The number of samples to use default is 10
	Int, rounding, number of digits to the left of the decimal to round
	Int, precision, Number of decimal digits

HAL Bool Label
--------------

A QLabel can have True and False text by adding two additional Dynamic
Properties. Both true_text and false_text must be set and can not be blank.

The HAL direction is IN and the hal_type is bit for a HAL Bool Label

See :doc:`property` for step by step instructions to add a Dynamic Property

.. csv-table:: HAL Bool Label
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_pin
	String, pin_name, any unique name
	String, true_text, text to display when True
	String, false_text, text to display when False

.. image:: /images/hal-bool-label-01.png
   :align: center

HAL Multi-State Label
---------------------

A QLabel can have multiple text by adding as many Dynamic Properties as needed
for each text. The `text_n` starts at 0 for example text_0, text_1 etc.

The HAL direction is IN and the hal_type is u32 for a HAL Multi-State Label.

If the HAL value is greater than the number of states the last state will be
displayed.

.. csv-table:: HAL Multi-State Label
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_msl
	String, pin_name, any unique name
	String, text_n, text to display when value is equal to n

.. note:: The text values must start at 0 and be sequencial.

.. image:: /images/hal-msl.png
   :align: center

HAL LED
-------
A QLabel can be used as a HAL LED indicator by adding the following properties
to a blank label. The default colors are Red when Off and Green when On. The
pin_name is the hal name the LED will have. The default shape is round.

The HAL LED needs to be connected in the postgui.hal file and can only be
connected to a HAL pin of type bit with a HAL direction of OUT or a signal that
is connected to a HAL pin of type bit with a HAL direction of OUT. Only one OUT
direction can be connected to a signal while multiple IN directions can be
connected to a signal.

The HAL direction is IN and the hal_type is bit for a HAL LED

.. csv-table:: HAL LED
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	Bool, hal_led, True
	String, function, hal_led
	String, pin_name, any unique name
	Optional
	Color, on_color, color of your choice
	Color, off_color, color of your choice
	Int, edge_margin, space between circle and edge of the label
	String, led_shape, square

Choosing 'rectangular' for LED shape will fill the entire control as one giant
indicator.

.. NOTE:: Select Other to get the list and select Color. You can copy and paste
   the hex color value into the color picker.

HAL LED Label
-------------

Similar to the HAL LED except the LED is in the upper right corner so the label
can have text. The default colors are Red when Off and Green when On. The
default shape is round.

The HAL direction is IN and the hal_type is bit for a HAL LED Label.


.. csv-table:: HAL LED Label
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_led_label
	String, pin_name, any unique name
	Optional
	Color, led_on_color, color of your choice
	Color, led_off_color, color of your choice
	Int, led_diameter, diameter of led
	Int, led_right_offset, offset from right edge
	Int, led_top_offset, offset from top edge
	String, led_shape, square

HAL LCD
-------

A QLCDNumber can be used to monitor HAL pins. HAL connections must be made in
the post gui HAL file. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-reader would be in HAL `flexhal.my-reader`.

The HAL direction is IN for a HAL LCD

.. csv-table:: HAL LCD
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_pin
	String, pin_name, any unique name
	String, hal_type, HAL_FLOAT or HAL_S32 or HAL_U32
	Optional
	String, integer_digits, Number of left pad zeros for HAL_S32 or HAL_U32

.. note:: A HAL_FLOAT QLCDNumber can have a string Dynamic Property called
   `precision` with a value of the number of decimal digits.

HAL Progress Bar
----------------

A QProgressBar can be used to monitor HAL pins. HAL connections must be made in
the post gui HAL file. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-bar would be in HAL `flexhal.my-bar`. Typically the
minimum value is 0 and the maximum value is 100. If the HAL value exceeds the
maximum value 0 is displayed.

The HAL direction is IN and the hal_type is u32 for a HAL Progress Bar.

.. csv-table:: HAL Progressbar
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	String, function, hal_pin
	String, pin_name, any unique name

Step by Step
------------

.. note:: This example is for a QPushButton

You can use a QPushButton as a momentary output, or with `checkable` selected
for a toggle type output, or QCheckBox or QRadioButton for a HAL output control.

Drag the widget into the GUI and the widget can have any name you like; names
are not used by HAL controls in Flex GUI - it is the following that matters.

Click on the widget to select it then click on the green plus sign in the
Property Editor for that widget to add a Dynamic Property and select String.

See :doc:`property` for step by step instructions to add a Dynamic Property

.. image:: /images/hal-01.png
   :align: center

Set the Property Name to `function` and click Ok

.. image:: /images/hal-02.png
   :align: center

Set the Value to `hal_pin`; this tells Flex GUI that this widget is going to be
for a HAL pin

.. image:: /images/hal-03.png
   :align: center

Add another string Dynamic Property named `pin_name` and set the value to any
unique name

.. image:: /images/hal-04.png
   :align: center

If you added Show HAL to your menu, you can open up the `Halshow` program and
view the pin names

.. image:: /images/hal-07.png
   :align: center

The pin names will all start with `flexhal` plus the unique name you gave them

.. image:: /images/hal-08.png
   :align: center

Now you can connect the Flex HAL pin in the postgui.hal file like normal

.. code-block:: text

	net some-signal-name flexhal.hal-test-01 => some-other-pin-in

You can also preset a numeric HAL value by using `setp` in this example the HAL
object is a QSpinBox which uses integer values.

.. code-block:: text

	setp flexhal.launch-velocity 10

After installing Flex GUI, from the CNC menu, you can copy the Flex GUI examples
and look at the hal-btn example.

HAL Pin Types

.. code-block:: text

	HAL_BIT
	HAL_FLOAT
	HAL_S32
	HAL_U32

HAL Pin Directions

.. code-block:: text

	HAL_IN
	HAL_OUT
	HAL_IO


