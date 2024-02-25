

def action_open(parent): # actionOpen
	print(parent.sender().objectName())

def action_recent(parent): # actionRecent
	print(parent.sender().objectName())

def action_edit(parent): # actionEdit
	print(parent.sender().objectName())

def action_reload(parent): # actionReload
	print(parent.sender().objectName())

def action_save_as(parent): # actionSave_As
	print(parent.sender().objectName())

def action_edit_tool_table(parent): # actionEdit_Tool_Table
	print(parent.sender().objectName())

def action_reload_tool_table(parent): # actionReload_Tool_Table
	print(parent.sender().objectName())

def action_ladder_editor(parent): # actionLadder_Editor
	print(parent.sender().objectName())

def action_quit(parent): # actionQuit
	print(parent.sender().objectName())

def action_clear_mdi(parent): # actionClear_MDI
	print(parent.sender().objectName())

def action_copy_mdi(parent): # actionCopy_MDI
	print(parent.sender().objectName())

def action_show_hal(parent): # actionShow_HAL
	print(parent.sender().objectName())
	# subprocess.Popen(r'c:\mytool\tool.exe', cwd=r'd:\test\local')
	# os.path.dirname(os.path.realpath(__file__)) 

def action_hal_meter(parent): # actionHal_Meter
	print(parent.sender().objectName())

def action_hal_scope(parent): # actionHal_Scope
	print(parent.sender().objectName())

def action_about(parent): # actionAbout
	print(parent.sender().objectName())

def action_quick_reference(parent): # actionQuick_Reference
	print(parent.sender().objectName())


