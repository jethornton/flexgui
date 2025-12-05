from functools import partial

def startup(parent):
	# connect a pushbutton without passing parent
	parent.my_test_pb.clicked.connect(test_1)
	parent.get_names_pb.clicked.connect(partial(get_names, parent))
	parent.get_names_p_pb.clicked.connect(partial(get_names_p, parent))

	# connect a pushbutton and pass parent to the function
	parent.another_test_pb.clicked.connect(partial(test_2, parent))

def test_1():
	print('test 1')

def test_2(parent):
	# in this function you have access to all the objects in parent
	print(f'test 2 {parent.another_test_pb.text()}')

def get_names(parent):
	# get all the object names from the parent
	print(dir(parent))

def get_names_p(parent):
	# get all the object names from the parent
	names = dir(parent)
	for name in names:
		if name.startswith('j'):
			print(name)


