
def save_settings(parent):
	parent.settings.setValue('gui/window_size', parent.size())
	parent.settings.setValue('gui/window_position', parent.pos())
	parent.settings.setValue('gui/geometry', parent.saveGeometry())
	parent.settings.sync()

