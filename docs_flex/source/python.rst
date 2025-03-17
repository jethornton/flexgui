Python Module
=============

`Python Import Tutorial <https://youtu.be/QC4K_8VMc6Y>`_

To import a python module add the following to the INI [FLEX] section using the
name of the python file without the.py extension. The file name must be unique
and can not be any python module name. You can have as many imports as you need
to simplify your code.
::

	[FLEX]
	IMPORT = testpy

.. note:: The module requires the .py extension to be able to import so the
   above module would be named testpy.py.

In each python file you import you must have a `startup` function where you make
any connections from objects in the ui file to code in your module. The parent
is passed to the startup function to give you access to all the objects in the
GUI.
::

	from functools import partial

	def startup(parent):
		# connect a pushbutton without passing parent
		parent.my_test_pb.clicked.connect(test_1)
		parent.get_names_pb.clicked.connect(partial(get_names, parent))

		# connect a pushbutton and pass parent to fhe function
		parent.another_test_pb.clicked.connect(partial(test_2, parent))

	def test_1():
		print('test 1')

	def test_2(parent):
		# in this function you have access to all the objects in parent
		print(f'test 2 {parent.another_test_pb.text()}')

	def get_names(parent):
		# get all the object names from the parent
		print(dir(parent))


Timer
-----

A user timer is provided for use in the user python module.
::

	from functools import partial

	def startup(parent):
		parent.user_timer.timeout.connect(testit)
		parent.conn_pb.setEnabled(False) # prevent another connection
		parent.disc_pb.clicked.connect(partial(disc, parent))
		parent.conn_pb.clicked.connect(partial(conn, parent))
		parent.start_pb.clicked.connect(partial(start, parent))
		parent.stop_pb.clicked.connect(partial(stop, parent))

	def testit():
		print('testing')

	def disc(parent):
		parent.user_timer.timeout.disconnect(testit)
		parent.conn_pb.setEnabled(True) # allow a connection
		parent.disc_pb.setEnabled(False) # prevent trying to disconnect

	def conn(parent):
		parent.user_timer.timeout.connect(testit)
		parent.conn_pb.setEnabled(False) # prevent trying to connect
		parent.disc_pb.setEnabled(True) # allow a disconnect

	def start(parent):
		parent.user_timer.start(1000) # milliseconds

	def stop(parent):
		parent.user_timer.stop()





