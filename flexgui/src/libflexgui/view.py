
def view_dro(parent):
	if parent.sender().isChecked():
		parent.plotter.enable_dro = True
	else:
		parent.plotter.enable_dro = False
	parent.plotter.load()

def view_limits(parent):
	if parent.sender().isChecked():
		parent.plotter.show_limits = True
	else:
		parent.plotter.show_limits = False
	parent.plotter.load()

def view_extents_option(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_live_plot(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_velocity(parent):
	if parent.sender().isChecked():
		parent.plotter.show_velocity = True
	else:
		parent.plotter.show_velocity = False
	parent.plotter.load()

def view_metric_units(parent):
	if parent.sender().isChecked():
		parent.plotter.metric_units = False
	else:
		parent.plotter.metric_units = True
	parent.plotter.load()

def view_program(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_rapids(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_tool(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_lathe_radius(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_dtg(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_offsets(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_overlay(parent):
	if parent.sender().isChecked():
		pass
	else:
		pass

def view_rotate_up(parent): # rotateView(self,vertical=0,horizontal=0)
	parent.plotter.rotateView(0, -2)

def view_rotate_down(parent): # rotateView(self,vertical=0,horizontal=0)
	parent.plotter.rotateView(0, 2)

def view_rotate_left(parent): # rotateView(self,vertical=0,horizontal=0)
	parent.plotter.rotateView(-2, 0)

def view_rotate_right(parent): # rotateView(self,vertical=0,horizontal=0)
	parent.plotter.rotateView(2, 0)

def view_pan_up(parent):
	parent.view_y = parent.view_y - 10
	parent.plotter.translateOrRotate(parent.view_x, parent.view_y)

def view_pan_down(parent):
	parent.view_y = parent.view_y + 10
	parent.plotter.translateOrRotate(parent.view_x, parent.view_y)

def view_pan_left(parent):
	parent.view_x = parent.view_x - 10
	parent.plotter.translateOrRotate(parent.view_x, parent.view_y)

def view_pan_right(parent):
	parent.view_x = parent.view_x + 10
	parent.plotter.translateOrRotate(parent.view_x, parent.view_y)

def view_zoom_in(parent):
	parent.plotter.distance = parent.plotter.distance - 1
	parent.plotter.update()

def view_zoom_out(parent):
	parent.plotter.distance = parent.plotter.distance + 1
	parent.plotter.update()

def view_clear(parent):
	parent.plotter.clear_live_plotter()
'p', 'x', 'y', 'y2', 'z', 'z2'
def view_p(parent):
	parent.plotter.current_view = 'p'
	parent.plotter.load()

def view_x(parent):
	parent.plotter.current_view = 'x'
	parent.plotter.load()

def view_y(parent):
	parent.plotter.current_view = 'y'
	parent.plotter.load()

def view_y2(parent):
	parent.plotter.current_view = 'y2'
	parent.plotter.load()

def view_z(parent):
	parent.plotter.current_view = 'z'
	parent.plotter.load()

def view_z2(parent):
	parent.plotter.current_view = 'z2'
	parent.plotter.load()



