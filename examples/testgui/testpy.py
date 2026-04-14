from functools import partial

def startup(parent):
	# connect a pushbutton without passing parent
	parent.external_tc_pb.clicked.connect(partial(external_tc, parent))

def external_tc(parent):
	parent.tool_change_pb.click()
