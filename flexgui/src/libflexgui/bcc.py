# Bolt Circle G code generator

import sys
import math
import linuxcnc
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QPushButton
from PyQt6.QtWidgets import QTextEdit, QLineEdit, QFormLayout
from PyQt6.QtWidgets import QDoubleSpinBox, QSpinBox, QSplitter, QComboBox
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer

def generate_bolt_circle_gcode(comment, x, y, radius, angle, holes, depth, retract, feed, is_metric, cycle_type, peck):
	if holes <= 0: return "; Error: Hole count must be > 0"
	
	gcode = [
		f"; {comment}" if comment else "; --- Flex GUI Auto Bolt Circle ---",
		"G21" if is_metric else "G20",
		"G90",
		f"G00 Z{retract + (5.0 if is_metric else 0.2):.4f}"
	]
	
	cycle = f"G83 R{retract:.4f} Z{depth:.4f} Q{peck:.4f} F{feed:.1f}" if "G83" in cycle_type else f"G81 R{retract:.4f} Z{depth:.4f} F{feed:.1f}"

	for i in range(holes):
		a = math.radians(angle + (i * (360.0 / holes)))
		hx = x + (radius * math.cos(a))
		hy = y + (radius * math.sin(a))
		if i == 0:
			gcode.append(f"G00 X{hx:.4f} Y{hy:.4f}")
			gcode.append(cycle)
		else:
			gcode.append(f"X{hx:.4f} Y{hy:.4f}")
			
	gcode.append("G80\nM02")
	return "\n".join(gcode)

class bc_gen(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent_ui = parent # Holds reference to the main Flex GUI window context

		self.command_channel = linuxcnc.command()
		self.status_channel = linuxcnc.stat()

		self.init_ui()

		# Monitor machine state for live MDI execution safety lockouts
		self.safety_timer = QTimer(self)
		self.safety_timer.timeout.connect(self.verify_machine_state)
		self.safety_timer.start(100)

	def init_ui(self):
		splitter = QSplitter(Qt.Orientation.Horizontal)
		left_widget = QWidget()
		form = QFormLayout(left_widget)

		self.combo_units = QComboBox()
		self.combo_units.addItem('Imperial', 'inch')
		self.combo_units.addItem('Metric', 'mm')

		self.combo_cycle = QComboBox()
		self.combo_cycle.addItems(["Normal Drill", "Peck Drill"])
		self.combo_cycle.currentIndexChanged.connect(self.toggle_peck)
		
		self.spin_x = QDoubleSpinBox(); self.spin_x.setRange(-999, 999)
		self.spin_y = QDoubleSpinBox(); self.spin_y.setRange(-999, 999)
		self.spin_radius = QDoubleSpinBox(); self.spin_radius.setRange(0, 999); self.spin_radius.setValue(2.0)
		self.spin_angle = QDoubleSpinBox(); self.spin_angle.setRange(0, 360)
		self.spin_holes = QSpinBox(); self.spin_holes.setRange(1, 100); self.spin_holes.setValue(6)
		self.spin_depth = QDoubleSpinBox(); self.spin_depth.setRange(-999, 999); self.spin_depth.setValue(-0.5)
		self.spin_retract = QDoubleSpinBox(); self.spin_retract.setRange(-999, 999); self.spin_retract.setValue(0.125)
		self.spin_peck = QDoubleSpinBox(); self.spin_peck.setRange(0, 999); self.spin_peck.setValue(0.100); self.spin_peck.setEnabled(False)
		self.spin_feed = QDoubleSpinBox(); self.spin_feed.setRange(1, 5000); self.spin_feed.setValue(10.0)
		self.comment = QLineEdit()

		input_frame = QFrame()
		input_layout = QGridLayout(input_frame)
		input_layout.setColumnStretch(1, 1)
		input_layout.setColumnStretch(3, 1)


		input_layout.addWidget(QLabel('Units:'), 0, 0, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.combo_units, 0, 1)
		input_layout.addWidget(QLabel('Cycle:'), 0, 2, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.combo_cycle, 0, 3)

		input_layout.addWidget(QLabel('Center X:'), 1, 0, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_x, 1, 1)
		input_layout.addWidget(QLabel('Center Y:'), 1, 2, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_y, 1, 3)

		input_layout.addWidget(QLabel('Radius:'), 2, 0, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_radius, 2, 1)
		input_layout.addWidget(QLabel('Start Angle:'), 2, 2, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_angle, 2, 3)

		input_layout.addWidget(QLabel('Depth Z:'), 3, 0, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_depth, 3, 1)
		input_layout.addWidget(QLabel('Retract R:'), 3, 2, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_retract, 3, 3)

		input_layout.addWidget(QLabel('Peck Q:'), 4, 0, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_peck, 4, 1)
		input_layout.addWidget(QLabel('Feed F:'), 4, 2, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_feed, 4, 3)

		input_layout.addWidget(QLabel('Comment:'), 5, 0, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.comment, 5, 1)
		input_layout.addWidget(QLabel('Hole Count:'), 5, 2, Qt.AlignmentFlag.AlignRight)
		input_layout.addWidget(self.spin_holes, 5, 3)


		form.addRow(input_frame)

		button_frame = QFrame()
		button_layout = QGridLayout(button_frame)

		# Fire directly using instant MDI blocks if operator prefers bypassing editing tabs completely
		self.btn_mdi = QPushButton("Run as MDI (Locked)")
		self.btn_mdi.setStyleSheet("background-color: #7f8c8d; color: white; font-weight: bold;")
		self.btn_mdi.setEnabled(False)
		self.btn_mdi.clicked.connect(self.run_mdi)
		button_layout.addWidget(self.btn_mdi, 0, 0)

		# Local test frame render preview
		self.btn_preview = QPushButton("Local Preview")
		self.btn_preview.clicked.connect(self.generate_local_preview)
		button_layout.addWidget(self.btn_preview, 0, 1)

		# This will automatically trip nc_code_changed() via parent text signals!
		# Append code to G Code Viewer
		self.btn_append_pte = QPushButton("Append to gcode_pte")
		self.btn_append_pte.setStyleSheet("background-color: #1f77b4; color: white; font-weight: bold;")

		# Stream code directly to main editor window canvas layout panel
		self.btn_send_pte = QPushButton("Send to gcode_pte")
		self.btn_send_pte.setStyleSheet("background-color: #1f77b4; color: white; font-weight: bold;")
		has_pte = self.parent_ui and hasattr(self.parent_ui, 'gcode_pte')
		if not has_pte:
			self.btn_send_pte.hide()
			self.btn_append_pte.hide()
		self.btn_send_pte.clicked.connect(self.send_to_gcode_pte)
		self.btn_append_pte.clicked.connect(self.append_to_gcode_pte)
		button_layout.addWidget(self.btn_append_pte, 1, 0)
		button_layout.addWidget(self.btn_send_pte, 1, 1)

		form.addRow(button_frame)

		self.text_preview = QTextEdit()
		self.text_preview.setReadOnly(True)
		self.text_preview.setPlaceholderText("Local G-Code preview...")

		splitter.addWidget(left_widget)
		splitter.addWidget(self.text_preview)

		layout = QVBoxLayout(self)
		layout.addWidget(splitter)
		layout.setContentsMargins(0, 0, 0, 0)

	def verify_machine_state(self):
		try:
			self.status_channel.poll()
			is_manual_mode = self.status_channel.task_mode == linuxcnc.MODE_MANUAL
			homed_tuple = self.status_channel.homed
			joints_configured = self.status_channel.joints
			all_joints_homed = all(homed_tuple[i] == 1 for i in range(joints_configured))

			if is_manual_mode and all_joints_homed:
				if not self.btn_mdi.isEnabled():
					self.btn_mdi.setEnabled(True)
					self.btn_mdi.setText("Run as MDI")
					self.btn_mdi.setStyleSheet("background-color: #2ca02c; color: white; font-weight: bold;")
			else:
				if self.btn_mdi.isEnabled():
					self.btn_mdi.setEnabled(False)
					self.btn_mdi.setStyleSheet("background-color: #7f8c8d; color: white; font-weight: bold;")
					if not is_manual_mode and not all_joints_homed:
						self.btn_mdi.setText("MDI Locked: Set Manual Mode & Home All")
					elif not is_manual_mode:
						self.btn_mdi.setText("MDI Locked: Switch to Manual Mode")
					else:
						self.btn_mdi.setText("MDI Locked: Home All Joints")
		except Exception:
			self.btn_mdi.setEnabled(False)
			self.btn_mdi.setText("MDI State Error")

	def toggle_peck(self):
		self.spin_peck.setEnabled("G83" in self.combo_cycle.currentText())

	def get_calculated_gcode(self):
		return generate_bolt_circle_gcode(self.comment.text(),
			self.spin_x.value(), self.spin_y.value(), self.spin_radius.value(),
			self.spin_angle.value(), self.spin_holes.value(), self.spin_depth.value(),
			self.spin_retract.value(), self.spin_feed.value(),
			self.combo_units.currentData() == 'mm', self.combo_cycle.currentText(), self.spin_peck.value()
		)

	def generate_local_preview(self):
		self.text_preview.setPlainText(self.get_calculated_gcode())

	def append_to_gcode_pte(self):
		if self.parent_ui and hasattr(self.parent_ui, 'gcode_pte'):
			# Updating text via setPlainText natively wakes parent.gcode_pte.textChanged
			# and automatically invokes utilities.nc_code_changed(parent)
			self.parent_ui.gcode_pte.appendPlainText(self.get_calculated_gcode())

	def send_to_gcode_pte(self):
		if self.parent_ui and hasattr(self.parent_ui, 'gcode_pte'):
			# Updating text via setPlainText natively wakes parent.gcode_pte.textChanged
			# and automatically invokes utilities.nc_code_changed(parent)
			self.parent_ui.gcode_pte.setPlainText(self.get_calculated_gcode())

	def run_mdi(self):
		gcode_text = self.get_calculated_gcode()

		self.command_channel.mode(linuxcnc.MODE_MDI)
		print('Changing Mode to MDI')
		self.command_channel.wait_complete()

		for line in gcode_text.split('\n'):
			line = line.strip()
			if line and not line.startswith(';'):
				self.command_channel.mdi(line)
				print(f'Executing {line}')
				self.command_channel.wait_complete()

		self.command_channel.mode(linuxcnc.MODE_MANUAL)

