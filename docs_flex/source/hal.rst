HAL Pins
========
`HAL Tutorial <https://youtu.be/LU4914GyGXI>`_


.. note:: Dynamic Property names are case sensitive and must be all lower case.
   Hal types and directions are case sensitive and must be all caps. The
   function value must be lower case.

.. note:: Hal pin names can containe a-z, A-Z, 0-9, underscore _, or dash -.

Button
------

Any QPushButton, QCheckBox or QRadioButton can be assigned to a HAL `bit` pin by
adding four string type Dynamic Properties.  The pin_name used will create a HAL
pin prefixed with `flexhal.` A pin_name of my-button would be in HAL
`flexhal.my-button`. See :doc:`property`

.. csv-table:: HAL Push Button
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_BIT
	hal_dir, HAL_OUT

Optionally the button can be disabled when the power is off by adding one more
property.

.. csv-table:: HAL Option
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	state_off, disabled


.. _SpinBoxTag:

Spinbox
-------

Any QSpinBox or QDoubleSpinBox can be a HAL `number` pin by adding four string
type Dynamic Properties. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-spinbox would be in HAL `flexhal.my-spinbox`.


.. csv-table:: HAL Spin Box
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_FLOAT or HAL_S32 or HAL_U32
	hal_dir, HAL_OUT

.. note:: A QSpinBox can only be HAL_S32 or HAL_U32 data type. A QDoubleSpinBox
   can only be HAL_FLOAT data type.

Slider
------

A QSlider can be a HAL pin by adding these four string type Dynamic Properties.
The pin_name used will create a HAL pin prefixed with `flexhal.` A pin_name of
my-slider would be in HAL `flexhal.my-slider`. See :doc:`property`

.. csv-table:: HAL Slider
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_S32 or HAL_U32
	hal_dir, HAL_OUT

HAL I/O
-------

A HAL I/O object has an input and output on the same pin. The pin can set an
input pin of another HAL object and the pin can be set by another HAL object
output pin. The HAL I/O will stay synchronized with the pin it's connected to.

.. NOTE The connected pins must be of the same HAL type.

A QPushButton (set to checkable), QCheckBox, QSpinBox, QDoubleSpinBox or a
QSlider can be a HAL I/O object.

.. csv-table:: HAL I/O
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_io
	pin_name, any unique name
	hal_type, HAL_BIT for a QCheckBox or QPushButton
	hal_type, HAL_FLOAT for a QDoubleSpinBox
	hal_type, HAL_S32 or HAL_U32 for a QSpinBox or QSlider
	hal_dir, HAL_IO

Label
-----

A QLabel can be used to monitor HAL pins. HAL connections must be made in the
post gui HAL file. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-reader would be in HAL `flexhal.my-reader`.

.. csv-table:: HAL Label
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_BIT or HAL_FLOAT or HAL_S32 or HAL_U32
	hal_dir, HAL_IN

.. note:: A HAL_FLOAT QLabel can have a string Dynamic Property called
   `precision` with a value of the number of decimal digits.

Bool Label
----------

A QLabel of hal_type HAL_BIT can have True and False text by adding two
additional Dynamic Properties. See :doc:`property`

.. csv-table:: HAL Bool Label
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_BIT
	hal_dir, HAL_IN
	true_text, text to display when True
	false_text, text to display when False

.. image:: /images/hal-bool-label-01.png
   :align: center

Multi-State Label
-----------------

A QLabel of hal_type HAL_U32 can have multiple text by adding as many Dynamic
Properties as needed. The `text_n` starts at 0 for example text_0, text_1 etc.

.. csv-table:: HAL Multi-State Label
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_msl
	pin_name, any unique name
	hal_type, HAL_U32
	hal_dir, HAL_IN
	text_n, text to display when value is equal to n

.. note:: The text values must start at 0 and be sequencial.

.. image:: /images/hal-msl.png
   :align: center

LED
---
A QLabel can be used as a HAL LED indicator by adding the following properties
to a blank label. Colors are optional, if not supplied red for off and green
for on will be used.

.. csv-table:: HAL LED
   :width: 100%
   :align: center

	**Property Type**, **Property Name**, **Pin Value**
	Bool, hal_led, True
	String, function, hal_led
	String, pin_name, any unique name
	String, hal_type, HAL_BIT
	String, hal_dir, HAL_IN
	Color, on_color, color of your choice
	Color, off_color, color of your choice

.. NOTE:: Select Other to get the list and select Color. You can copy and paste
   the hex color value into the color picker. 

LCD
---

A QLCDNumber can be used to monitor HAL pins. HAL connections must be made in
the post gui HAL file. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-reader would be in HAL `flexhal.my-reader`.

.. csv-table:: HAL LCD
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_FLOAT or HAL_S32 or HAL_U32
	hal_dir, HAL_IN

.. note:: A HAL_FLOAT QLCDNumber can have a string Dynamic Property called
   `precision` with a value of the number of decimal digits.

Pin Types::

	HAL_BIT
	HAL_FLOAT
	HAL_S32
	HAL_U32

Pin Directions::

	HAL_IN
	HAL_OUT
	HAL_IO

Currently only `HAL_BIT` with `HAL_OUT` have been tested.

.. warning:: By default, no QRadioButtons are checked unless you set one checked
   in the Designer. Starting up with none checked could be a problem if you
   expect one to be selected at startup.

Progress Bar
------------

A QProgressBar can be used to monitor HAL pins. HAL connections must be made in
the post gui HAL file. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-bar would be in HAL `flexhal.my-bar`.

.. csv-table:: HAL Progressbar
   :width: 100%
   :align: center

	**Property Name**, **Pin Value**
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_S32 or HAL_U32
	hal_dir, HAL_IN

Step by Step
------------

.. note:: This example is for a QPushButton

You can use a QPushButton as a momentary output, or with `checkable` selected
for a toggle type output, or QCheckBox or QRadioButton for a HAL output control.

Drag the widget into the GUI and the widget can have any name you like; names
are not used by HAL controls in Flex GUI - it is the following that matters.

Click on the widget to select it then click on the green plus sign in the
Property Editor for that widget to add a Dynamic Property and select String.
See :doc:`property`

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

Add another Dynamic Property named `hal_type` and set the value to HAL_BIT

.. image:: /images/hal-05.png
   :align: center

Add another Dynamic Property named `hal_dir` and set the value to HAL_OUT

.. image:: /images/hal-06.png
   :align: center

If you added Show HAL to your menu, you can open up the `Halshow` program and
view the pin names

.. image:: /images/hal-07.png
   :align: center

The pin names will all start with `flexhal` plus the unique name you gave them

.. image:: /images/hal-08.png
   :align: center

Now you can connect the Flex HAL pin in the postgui.hal file like normal
::

	net some-signal-name flexhal.hal-test-01 => some-other-pin-in

After installing Flex GUI, from the CNC menu, you can copy the Flex GUI examples
and look at the hal-btn example.


Homed Required
--------------

If the HAL button requires all joints to be homed before being enabled, you can
specify that by adding a Dynamic Property named `required` and set the value to
`homed`.

.. image:: /images/hal-09.png
   :align: center
