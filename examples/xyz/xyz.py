from functools import partial

def startup(parent):
	# connect a pushbutton without passing parent
	#parent.my_test_pb.clicked.connect(test_1)

	# connect a pushbutton and pass parent to the function
	#parent.another_test_pb.clicked.connect(partial(test_2, parent))
	parent.state_estop_pb.setEnabled(False)
	parent.state_estop['state_estop_pb'] = False
	parent.state_estop_reset['state_estop_pb'] = True
	parent.state_on_pb.setEnabled(False)
	parent.state_estop_reset['state_on_pb'] = False
	parent.state_on['state_on_pb'] = True
	parent.state_on['disabled_running_pb'] = True
	parent.program_running['disabled_running_pb'] = False






