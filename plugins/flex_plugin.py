#!/usr/bin/env python3

# Print Out to see designer loaded it
print('Loading Flex GUI Designer Custom Widgets Plugins')

#print('Loading Number Display Plugin')
#from libflexgui.numberplugin import PyNumberDisplayPlugin

print('Loading Float Number Display Plugin')
from libflexgui.floatplugin import FlexFloatDisplayPlugin

print("Finished loading")
