from functools import partial

from libflexgui import dialogs

def startup(parent):
	# connect a pushbutton without passing parent
	#parent.my_test_pb.clicked.connect(test_1)

	# connect a pushbutton and pass parent to the function
	parent.info_msg_ok_pb.clicked.connect(partial(test_info_msg_ok, parent))
	parent.confirm_msg_ok_cancel_pb.clicked.connect(partial(test_confirm_msg_ok_cancel, parent))
	parent.error_msg_ok_pb.clicked.connect(partial(test_error_msg_ok, parent))
	parent.warn_msg_ok_pb.clicked.connect(partial(test_warn_msg_ok, parent))
	parent.warn_msg_yes_no_pb.clicked.connect(partial(test_warn_msg_yes_no, parent))
	parent.critical_msg_ok_pb.clicked.connect(partial(test_critical_msg_ok, parent))

def test_info_msg_ok(parent):
	parent.result_lb.setText('Testing dialogs info_msg_ok')
	msg = ('This is a test message')
	result = dialogs.info_msg_ok(parent, msg, 'title')
	parent.result_lb.setText(f'The return Value was {result}')

def test_confirm_msg_ok_cancel(parent):
	parent.result_lb.setText('Testing dialogs confirm_msg_ok_cancel')
	msg = ('This is a test message')
	result = dialogs.confirm_msg_ok_cancel(parent, msg, 'title')
	parent.result_lb.setText(f'The return Value was {result}')

def test_error_msg_ok(parent):
	parent.result_lb.setText('Testing dialogs error_msg_ok')
	msg = ('This is a test message')
	result = dialogs.error_msg_ok(parent, msg, 'title')
	parent.result_lb.setText(f'The return Value was {result}')

def test_warn_msg_ok(parent):
	parent.result_lb.setText('Testing dialogs warn_msg_ok')
	msg = ('This is a test message')
	result = dialogs.warn_msg_ok(parent, msg, 'title')
	parent.result_lb.setText(f'The return Value was {result}')

def test_warn_msg_yes_no(parent):
	parent.result_lb.setText('Testing dialogs warn_msg_yes_no')
	msg = ('This is a test message')
	result = dialogs.warn_msg_yes_no(parent, msg, 'title')
	parent.result_lb.setText(f'The return Value was {result}')

def test_critical_msg_ok(parent):
	parent.result_lb.setText('Testing dialogs critical_msg_ok')
	msg = ('This is a test message')
	result = dialogs.critical_msg_ok(parent, msg, 'title')
	parent.result_lb.setText(f'The return Value was {result}')


