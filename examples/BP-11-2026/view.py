#!/usr/bin/env python3

import importlib
import sys
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QScrollArea, QVBoxLayout, QWidget

# Initialize the PyQt6 Application
app = QApplication(sys.argv)

# Load your resource file
importlib.import_module("resources")

# Build the layout container
window = QWidget()
layout = QVBoxLayout(window)
scroll = QScrollArea()
scroll_widget = QWidget()
scroll_layout = QVBoxLayout(scroll_widget)

# Scan the resource tree and inject elements into the UI
iterator = QDir(":/").entryInfoList()
for file_info in iterator:
    res_path = file_info.absoluteFilePath()

    # Create the visual elements
    pixmap = QPixmap(res_path)
    path_label = QLabel(f"<b>Internal Path:</b> {res_path}")
    img_label = QLabel()
    img_label.setPixmap(pixmap)

    # Add to the scrollable view
    scroll_layout.addWidget(path_label)
    scroll_layout.addWidget(img_label)

# Render the window
scroll.setWidget(scroll_widget)
scroll.setWidgetResizable(True)
layout.addWidget(scroll)
window.setWindowTitle("Resource Viewer")
window.resize(450, 650)
window.show()

sys.exit(app.exec())

