HAL Buttons
===========

Any QPushButton can have a HAL pin by adding a string Dynamic Property called
`function` with the value of `hal_pin` and a string Dynamic Property called
`pin_n` where n is some non repeated number with a property of 
`pin_name, pin_type, pin_dir` seperated by comma's

Pin and Parameter Types::

	HAL_BIT
	HAL_FLOAT
	HAL_S32
	HAL_U32

Pin Directions::

	HAL_IN
	HAL_OUT
	HAL_IO


