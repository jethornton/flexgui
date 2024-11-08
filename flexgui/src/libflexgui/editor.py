from PyQt6.QtGui import QTextCursor, QTextBlockFormat, QColor, QPalette

######## I don't think any of this is used any more it's in utilities or should be

def show_line(parent):
	#background = parent.gcode_pte.palette().color(QPalette.ColorRole.Window).name()
	# QColor background = your_label.palette().color(QPalette::Window);
	# get a copy of the QTextCursor that represents the currently visible cursor
	#cursor = parent.gcode_pte.textCursor()
	#selected_block = cursor.blockNumber() # get current block number
	#self.lbl.setText(f'Current line number: {selected_block}')
	#if 'start_line_lb' in parent.children:
	#	parent.start_line_lb.setText(f'{selected_block}')
	#format_normal = QTextBlockFormat()
	#format_normal.setBackground(QColor('black'))
	#highlight_format = QTextBlockFormat()
	#highlight_format.setBackground(QColor('yellow'))
	#cursor.select(QTextCursor.SelectionType.Document)
	#cursor.setBlockFormat(format_normal) # clear the format
	# I'm not sure what's going on on the next line but it seems that is could be simpler
	#cursor.select(QTextCursor.SelectionType.Document.findBlockByNumber(selected_block))
	#cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(selected_block))
	#cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor)
	#cursor.setBlockFormat(highlight_format)
	#parent.gcode_pte.setTextCursor(cursor)

def select_line(parent, event): # not used anywhere
	editor = QtGui.QPlainTextEdit()

	fmt = QtGui.QTextCharFormat()
	fmt.setUnderlineColor(Qt.red)
	fmt.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)

	block = editor.document().findBlockByLineNumber(line)
	blockPos = block.position()

	cursor = QtGui.QTextCursor(editor.document())
	cursor.setPosition(blockPos)
	cursor.select(QtGui.QTextCursor.LineUnderCursor)
	cursor.setCharFormat(fmt)

def highlight_line(parent): # update highlighted line when program is running
	""" Sets the highlighting of a given line number in the QTextEdit"""
	format_normal = QTextBlockFormat()
	format_normal.setBackground(QColor('black'))
	highlight_format = QTextBlockFormat()
	highlight_format.setBackground(QColor('yellow'))
	motion_line = parent.status.motion_line

	cursor = parent.gcode_pte.textCursor()
	cursor.select(QTextCursor.SelectionType.Document)
	cursor.setBlockFormat(format_normal)

	cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(motion_line))
	cursor.setBlockFormat(highlight_format)
	parent.gcode_pte.setTextCursor(cursor)

def move_cursor(parent): # not used anywhere
	format_normal = QTextBlockFormat()
	format_normal.setBackground(QColor('white'))
	highlight_format = QTextBlockFormat()
	highlight_format.setBackground(QColor('yellow'))
	motion_line = parent.status.motion_line

	cursor = parent.gcode_pte.textCursor()
	cursor.select(QTextCursor.SelectionType.Document)
	cursor.setBlockFormat(format_normal)
	cursor = parent.gcode_pte.textCursor()
	next_block = cursor.blockNumber()
	cursor = QTextCursor(parent.gcode_pte.document().findBlockByNumber(next_block))
	cursor.setBlockFormat(highlight_format)

def clear_highlight(parent): # not used anywhere
	format_normal = QTextBlockFormat()
	format_normal.setBackground(QColor('white'))
	cursor = parent.gcode_pte.textCursor()
	cursor.select(QTextCursor.SelectionType.Document)
	cursor.setBlockFormat(format_normal)
	cursor.clearSelection()
	parent.gcode_pte.setTextCursor(cursor)
	parent.gcode_pte.setCursorWidth(0)

