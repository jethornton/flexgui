StyleSheet
==========

You can use your own qss style sheet by creating a valid qss file in the
configuration directory and setting it in the INI file.

The `Qt6 Stylesheet Reference <https://doc.qt.io/qt-6/stylesheet-reference.html>`_
is a good place to start when creating your own stylesheet.

.. note:: If there is a error in the stylesheet syntax no warning is issued, 
   it's just ignored. So don't forget the ; at the end or each setting.

Some short examples:

.. code-block:: html

	/*Set the background color for all QPushButtons*/
	QPushButton{
		background-color: rgba(224, 224, 224, 50%);
	}
	
	/*Set the background color and style for all QPushButtons when Pressed*/
	QPushButton:pressed{
		background-color: rgba(192, 192, 192, 100%);
		border-style: inset;
	}

	/*Set settings for a QPushButton named exit_pb*/
	QPushButton#exit_pb{
	border: none;
	background-color: rgba(0, 0, 0, 0);
	}

	/*Using sub controls*/
	QAbstractSpinBox::up-button {
		min-width: 30px;
	}

	/*Combining sub controls and state*/
	QTabBar::tab:selected {
		background: lightgray;
	}

