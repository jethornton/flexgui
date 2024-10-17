HAL Pins
========

Button
------

Any QPushButton, QCheckBox or QRadioButton can be assigned to a HAL `bit` pin by
adding four string type Dynamic Properties.  The pin_name used will create a HAL
pin prefixed with `flexhal.` A pin_name of my-button would be in HAL
`flexhal.my-button`.

.. csv-table:: HAL Push Button
   :width: 100%
   :align: center

	Property Name, Pin Value
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_BIT
	hal_dir, HAL_OUT

.. _SpinBoxTag:

Spinbox
-------

Any QSpinBox or QDoubleSpinBox can be a HAL `number` pin by adding four string
type Dynamic Properties. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-spinbox would be in HAL `flexhal.my-spinbox`.


.. csv-table:: HAL Spin Box
   :width: 100%
   :align: center

	Property Name, Pin Value
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
my-slider would be in HAL `flexhal.my-slider`.

.. csv-table:: HAL Slider
   :width: 100%
   :align: center

	Property Name, Pin Value
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_S32 or HAL_U32
	hal_dir, HAL_OUT

Label
-----

A QLabel can be used to monitor HAL pins. HAL connections must be made in the
post gui HAL file. The pin_name used will create a HAL pin prefixed with
`flexhal.` A pin_name of my-reader would be in HAL `flexhal.my-reader`.

.. csv-table:: HAL Label
   :width: 100%
   :align: center

	Property Name, Pin Value
	function, hal_pin
	pin_name, any unique name
	hal_type, HAL_BIT or HAL_FLOAT or HAL_S32 or HAL_U32
	hal_dir, HAL_IN


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

Step by Step
------------

.. note:: This example is for a QPushButton

You can use a QPushButton as a momentary output, or with `checkable` selected
for a toggle type output, or QCheckBox or QRadioButton for a HAL output control.

Drag the widget into the GUI and the widget can have any name you like; names
are not used by HAL controls in Flex GUI - it is the following that matters.

Click on the widget to select it then click on the green plus sign in the
Property Editor for that widget to add a Dynamic Property and select String

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
specifiy that by adding a Dynamic Property named `required` and set the value to
`homed`.

.. image:: /images/hal-09.png
   :align: center
