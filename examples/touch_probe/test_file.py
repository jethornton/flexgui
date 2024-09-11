#!/usr/bin/env python3

import os.path

path = './resources.py'
check_file = os.path.isfile(path)

if check_file:
	print(path)
	print(check_file)
	import resources
	print('Success!')
else:
		print(check_file)

################
#import os.path

#path = './resources.py'
#path2 = './'
#check_file = os.path.isfile(path)

#if check_file:
#	print(path)
#	print(check_file)
##	import /home/tom/linuxcnc/configs/touch-probe/resources
##	from resources.py import qt_resource_data
#	print('Success!')
#else:
#		print(check_file)


################
#import resources.py from JT:
#!/usr/bin/env python3

import importlib.util

def module_from_file(module_name, file_path):
	spec = importlib.util.spec_from_file_location(module_name, file_path)
	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module

foo = module_from_file("foo", "/home/john/linuxcnc/configs/flex_examples/xyz_resources/foo.py")
foo = module_from_file("foo", "/home/tom/linuxcnc/configs/touch-probe/images/resources.py")

if __name__ == "__main__":
	print(foo)
	print(dir(foo))
	foo.announce()



