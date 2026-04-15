from functools import partial

def startup(parent):
	parent.external_tc_pb.toggled.connect(partial(external_tc, parent))

def external_tc(parent):
	if not parent.sender().isChecked():
		parent.tool_change_pb.click()

