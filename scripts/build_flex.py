#!/usr/bin/env python3

# **** notice there are hard coded directories that only work on my pc ****

import os, subprocess, time
from subprocess import Popen, PIPE

# change to the flexgui directory
os.chdir('/home/your_path_to/flexgui')

# build the deb
print('\n*** Building the DEB ***\n')
subprocess.run(['debuild', '-us', '-uc'])

# change to the github directory
os.chdir('/home/your_github_directory')

files = os.listdir()
debs = []
for file in files:
	if file.startswith('flexgui_'):
		if file.endswith('amd64.deb'):
			debs.append(file)

debs.sort()
deb = debs[-1]

print('\n*** Installing the DEB ***\n')
cmd = ['sudo', '-S', 'gdebi', '--n', deb]
p = Popen(cmd, stdin=PIPE, text=True)
prompt = p.communicate('your_password\n')

print('By By in 10 seconds')
time.sleep(10)
