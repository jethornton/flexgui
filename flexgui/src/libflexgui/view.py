

def view_rotate_up(parent): # rotateView(self,vertical=0,horizontal=0)
	parent.plotter.rotateView(0, -2)

def view_rotate_down(parent): # rotateView(self,vertical=0,horizontal=0)
	parent.plotter.rotateView(0, 2)

def view_rotate_left(parent): # rotateView(self,vertical=0,horizontal=0)
	parent.plotter.rotateView(-2, 0)

def view_rotate_right(parent): # rotateView(self,vertical=0,horizontal=0)
	parent.plotter.rotateView(2, 0)

def view_pan_up(parent):
	parent.view_y = parent.view_y - 2
	parent.plotter.translateOrRotate(parent.view_x, parent.view_y)

def view_pan_down(parent):
	parent.view_y = parent.view_y + 2
	parent.plotter.translateOrRotate(parent.view_x, parent.view_y)

def view_pan_left(parent):
	parent.view_x = parent.view_x - 2
	parent.plotter.translateOrRotate(parent.view_x, parent.view_y)

def view_pan_right(parent):
	parent.view_x = parent.view_x + 2
	parent.plotter.translateOrRotate(parent.view_x, parent.view_y)

def view_zoom_in(parent):
	parent.plotter.distance = parent.plotter.distance - 1
	parent.plotter.update()

def view_zoom_out(parent):
	parent.plotter.distance = parent.plotter.distance + 1
	parent.plotter.update()

def view_clear(parent):
	parent.plotter.clear_live_plotter()
	#'p', 'x', 'y', 'y2', 'z', 'z2'
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



