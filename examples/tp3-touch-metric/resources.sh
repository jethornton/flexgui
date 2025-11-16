#!/bin/b

source ~/venv/bin/activate
~/venv/bin/pyside6-rcc resources.qrc -o resources.py
sed -i 's/from PySide6 import QtCore/from PyQt6 import QtCore/g' resources.py
deactivate 
echo
echo "**** all done, have a nice day ****"
echo
sleep 3
