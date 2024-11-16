from functools import partial

def startup(parent):
	# connect a pushbutton without passing parent
	parent.my_test_pb.clicked.connect(test_1)

	# connect a pushbutton and pass parent to fhe function
	parent.another_test_pb.clicked.connect(partial(test_2, parent))

def test_1():
	print('test 1')

def test_2(parent):
	# in this function you have access to all the objects in parent
	print(f'test 2 {parent.another_test_pb.text()}')
