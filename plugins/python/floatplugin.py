
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from libflexgui.floatdisplay import FlexFloatDisplay

class FlexFloatDisplayPlugin(QPyDesignerCustomWidgetPlugin):
	# The __init__() method is only used to set up the plugin and define its
	# initialized variable.
	def __init__(self):
		super().__init__()
		self.initialized = False

	# The initialize() and isInitialized() methods allow the plugin to set up
	# any required resources, ensuring that this can only happen once for each
	# plugin.
	def initialize(self, core):
		if self.initialized:
			return
		self.initialized = True

	def isInitialized(self):
		return self.initialized

	# This factory method creates new instances of our custom widget with the
	# appropriate parent.
	def createWidget(self, parent):
		return FlexFloatDisplay(parent)

	# This method returns the name of the custom widget class that is provided
	# by this plugin.
	def name(self):
		return "FlexFloatDisplay"

	# Returns the name of the group in Qt Designer's widget box that this
	# widget belongs to.
	def group(self):
		return "Flex Widgets"

	# Returns the icon used to represent the custom widget in Qt Designer's
	# widget box.
	def icon(self):
		# TODO
		return QIcon(QPixmap(None))

	# Returns a short description of the custom widget for use in a tool tip.
	def toolTip(self):
		return ""

	# Returns a short description of the custom widget for use in a "What's
	# This?" help message for the widget.
	def whatsThis(self):
		return ""

	# Returns True if the custom widget acts as a container for other widgets;
	# otherwise returns False. Note that plugins for custom containers also
	# need to provide an implementation of the QDesignerContainerExtension
	# interface if they need to add custom editing support to Qt Designer.
	def isContainer(self):
		return False

	# Returns an XML description of a custom widget instance that describes
	# default values for its properties. Each custom widget created by this
	# plugin will be configured using this description.
	def domXml(self):
		return '<widget class="FlexFloatDisplay" name="floatDisplay">\n' \
			' <property name="toolTip">\n' \
			'  <string>Float number display</string>\n' \
			' </property>\n' \
			' <property name="whatsThis">\n' \
			'  <string>Used with Flex GUI</string>\n' \
			' </property>\n' \
			' <property name="text">\n' \
			'  <string>0.0</string>\n' \
			' </property>\n' \
			' <property name="alignment">\n' \
			'  <set>Qt::Alignment::AlignRight|Qt::Alignment::AlignTrailing|Qt::Alignment::AlignVCenter</set>\n' \
			' </property>\n' \
			'</widget>\n'

	# Returns the module containing the custom widget class. It may include
	# a module path.
	def includeFile(self):
		return "libflexgui.floatdisplay"




