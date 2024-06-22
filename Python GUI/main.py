import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QComboBox, QCheckBox, QGroupBox, \
	QHBoxLayout, QPushButton, QAction, QLineEdit, QDialog, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QSizePolicy
import FSCVMotherboard as FM
from UART import UART
from PyQt5.QtGui import QPainter, QColor, QIcon


class Channel(QWidget):
	CH_EN = "CH_EN"
	COND_EN = "COND_EN"
	HPF_EN = "HPF_EN"
	SEL_CH = "SEL_CH"

	item_selected = pyqtSignal(int)

	def __init__(self, parent, chList):
		super().__init__(parent)

		layout = QVBoxLayout()
		self.setLayout(layout)

		self.enabled_checkbox0 = QCheckBox("Channel Enable", self)
		layout.addWidget(self.enabled_checkbox0)
		self.channelCombo = None
		if chList is not None:
			self.channelCombo = QComboBox(self)
			list = ["FSCV Channel " + str(i) for i in chList]
			self.channelCombo.addItems(list)
			self.channelCombo.activated[str].connect(self.onComboBoxSelected)
			layout.addWidget(self.channelCombo)

		checkbox_layout = QHBoxLayout()
		layout.addLayout(checkbox_layout)

		self.enabled_checkbox1 = QCheckBox("Conditioning Enable", self)
		checkbox_layout.addWidget(self.enabled_checkbox1)

		self.enabled_checkbox2 = QCheckBox("HPF Enable", self)
		checkbox_layout.addWidget(self.enabled_checkbox2)


	def onComboBoxSelected(self, ch):
		self.item_selected.emit(int(ch.split()[-1]))

	def changeItem(self,index):
		self.channelCombo.setCurrentIndex(index)

	def getValues(self):
		values = {
			Channel.CH_EN: self.enabled_checkbox0.isChecked(),
			Channel.COND_EN: self.enabled_checkbox1.isChecked(),
			Channel.HPF_EN: self.enabled_checkbox2.isChecked(),
			Channel.SEL_CH: 0  # Default value if channel_combo is null
		}

		if self.channelCombo is not None:
			selected_text = self.channelCombo.currentText()
			if selected_text:
				values[Channel.SEL_CH] = int(selected_text.split()[-1])

		return values


class CurrentGeneration(QWidget):
	IREF_TEST_EN = "IREF_TEST_EN"
	IREF_EN = "IREF_EN"

	def __init__(self, parent=None):
		super().__init__(parent)
		self.initUI()

	def initUI(self):
		layout = QVBoxLayout(self)
		layout.setContentsMargins(20, 20, 20, 20)
		layout.setSpacing(20)
		self.checkboxes = []
		# Creating checkbox layout for each row
		for row_name in ['Channel 12', 'Channel 34', 'Channel 56', 'Channel 78', 'Debug Channel']:
			row_layout = QHBoxLayout()
			row_label = QLabel(row_name)
			row_label.setStyleSheet("font-weight: bold; font-size: 12px;")
			row_layout.addWidget(row_label)

			checkbox_enable = QCheckBox("Enable")
			row_layout.addWidget(checkbox_enable)

			checkbox_test_enable = QCheckBox("Test Enable")
			row_layout.addWidget(checkbox_test_enable)

			layout.addLayout(row_layout)
			self.checkboxes.append((row_name, checkbox_enable, checkbox_test_enable))

	def getValues(self):
		values = {}
		for row_name, checkbox_enable, checkbox_test_enable in self.checkboxes:
			enable_value = checkbox_enable.isChecked()
			test_enable_value = checkbox_test_enable.isChecked()

			if row_name == "Channel 12":
				row_name = FM.FSCVMotherboard.CH_12
			elif row_name == "Channel 34":
				row_name = FM.FSCVMotherboard.CH_34
			elif row_name == "Channel 56":
				row_name = FM.FSCVMotherboard.CH_56
			elif row_name == "Channel 78":
				row_name = FM.FSCVMotherboard.CH_78
			elif row_name == "Debug Channel":
				row_name = FM.FSCVMotherboard.CH_DE

			values[row_name] = {
				CurrentGeneration.IREF_EN: enable_value,
				CurrentGeneration.IREF_TEST_EN: test_enable_value
			}
		return values


class PR(QWidget):
	SEL_1 = "SEL_1"
	SEL_2 = "SEL_2"
	SEL_3 = "SEL_3"
	IREF_SWITCH_SEL = "IREF_SWITCH_SEL"

	def __init__(self, parent=None):
		super().__init__(parent)
		self.initUI()

	def initUI(self):
		layout = QHBoxLayout(self)

		self.checkboxSel1 = QCheckBox("SEL 1")
		layout.addWidget(self.checkboxSel1)

		self.checkboxSel2 = QCheckBox("SEL 2")
		layout.addWidget(self.checkboxSel2)

		self.checkboxSel3 = QCheckBox("SEL 3")
		layout.addWidget(self.checkboxSel3)

		self.checkboxIrefpr = QCheckBox("IREF Switch Sel")
		layout.addWidget(self.checkboxSel3)

		layout.addWidget(self.checkboxSel1)
		layout.addWidget(self.checkboxSel2)
		layout.addWidget(self.checkboxSel3)
		layout.addWidget(self.checkboxIrefpr)

	def getValues(self):
		values = {
			PR.SEL_1: self.checkboxSel1.isChecked(),
			PR.SEL_2: self.checkboxSel2.isChecked(),
			PR.SEL_3: self.checkboxSel3.isChecked(),
			PR.IREF_SWITCH_SEL: self.checkboxIrefpr.isChecked()
		}
		return values


class StatusCircle(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.setMinimumSize(30, 30)  # Increase the minimum size for more padding
		self.status_color = QColor("#FF3B30")  # Red by default

	def setStatus(self, active):
		if active:
			self.status_color = QColor("#5EFF63")  # Green
		else:
			self.status_color = QColor("#FF3B30")  # Red
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setBrush(self.status_color)
		painter.setPen(QtCore.Qt.NoPen)
		radius = min(self.width(), self.height()) / 2.5
		painter.drawEllipse(self.rect().center(), radius, radius)


class SettingsDialog(QDialog):
	settingsSaved = pyqtSignal(int, str)

	def __init__(self):
		super().__init__()

		self.setWindowTitle("Settings")
		self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
		self.init_ui()

	def init_ui(self):
		layout = QVBoxLayout()

		# Textbox for entering the baud rate
		self.baudrate_label = QLabel("Baud Rate:")
		layout.addWidget(self.baudrate_label)
		self.baudrate_input = QLineEdit()
		layout.addWidget(self.baudrate_input)

		# Textbox for entering the port
		self.port_label = QLabel("Port:")
		layout.addWidget(self.port_label)
		self.port_input = QLineEdit()
		layout.addWidget(self.port_input)

		# Save button
		self.save_button = QPushButton("Save")
		self.save_button.clicked.connect(self.saveSettings)
		layout.addWidget(self.save_button)

		self.setLayout(layout)

	def saveSettings(self):
		baudRate = self.baudrate_input.text()
		try:
			baudRate = int(baudRate)
		except ValueError:
			# If not an integer, show an error message and return without emitting the signal
			QMessageBox.critical(self, "Error", "Baud rate must be an integer.")
			return
		self.settingsSaved.emit(baudRate, self.port_input.text())

		self.accept()  # Close the dialog

	def setValues(self, baudRate, port):
		self.baudrate_input.setText(str(baudRate))
		self.port_input.setText(port)


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		# self.setStyleSheet("background-color: white;")
		self.setWindowTitle("FSCV Motherboard V2")
		self.setWindowFlags(self.windowFlags() | QtCore.Qt.CustomizeWindowHint)
		self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
		central_widget = QWidget()
		self.setCentralWidget(central_widget)
		baselayout = QVBoxLayout()

		hbox = QHBoxLayout()
		self.setWindowIcon(QIcon("Icons/nyu.png"))
		central_widget.setLayout(baselayout)

		self.label = QLabel("FSCV Motherboard V2", self)
		self.label.setStyleSheet("font-size: 14pt")
		self.label.setAlignment(QtCore.Qt.AlignHCenter)  # Aligning label to center

		iconLabel = QLabel()
		icon = QIcon("Icons/arduino.png")  # Replace with the path to your icon file
		pixmap = icon.pixmap(24, 24)  # Adjust the size as needed
		iconLabel.setPixmap(pixmap)

		hbox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
		hbox.addWidget(iconLabel)
		hbox.addWidget(self.label)
		baselayout.addLayout(hbox)


		layout = QHBoxLayout()
		baselayout.addLayout(layout)

		self.channels = []
		vlayout1 = QVBoxLayout()
		vlayout2 = QVBoxLayout()
		# vlayout2.setSizeConstraint(QVBoxLayout.SetFixedSize)
		layout.addLayout(vlayout1)
		layout.addLayout(vlayout2)
		vlayout1.addWidget(self.createChannel("Channel A", [1, 5]))
		vlayout1.addWidget(self.createChannel("Channel B", [2, 6]))
		vlayout1.addWidget(self.createChannel("Channel C", [3, 7]))
		vlayout1.addWidget(self.createChannel("Channel D", [4, 8]))
		vlayout2.addWidget(self.createChannel("Debug Channel", None))
		vlayout2.addWidget(self.createCurrentGen())
		vlayout2.addWidget(self.createPR())
		vlayout2.setAlignment(QtCore.Qt.AlignTop)

		uartStatusLayout = QHBoxLayout()
		uartStatusLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
		self.status_label = QLabel("Status:")
		self.status_label.setStyleSheet("font-size: 14px;")
		self.statusCircle = StatusCircle(self)
		uartStatusLayout.addWidget(self.status_label)
		uartStatusLayout.addWidget(self.statusCircle)

		vlayout = QVBoxLayout()
		vlayout.addLayout(uartStatusLayout, stretch=1)

		vlayout2.addLayout(vlayout)
		self.statusCircle.setStatus(True)

		# Add button
		buttonLayout = QHBoxLayout()
		self.uploadButton = QPushButton("Upload", self)
		self.testButton = QPushButton("Test Connection", self)
		self.settingsButton = QPushButton("Settings", self)
		buttonLayout.addWidget(self.uploadButton)
		buttonLayout.addWidget(self.testButton)
		buttonLayout.addWidget(self.settingsButton)
		baselayout.addLayout(buttonLayout)
		self.uploadButton.clicked.connect(self.upload)
		self.testButton.clicked.connect(self.testConnection)
		self.settingsButton.clicked.connect(self.settings)

		# icon = QIcon("Icons\gear.png")
		# self.settingsButton.setIcon(icon)
		#
		# icon = QIcon("Icons\link.png")
		# self.testButton.setIcon(icon)
		#
		# icon = QIcon("Icons\\upload.png")
		# self.saveButton.setIcon(icon)


		QTimer.singleShot(1000, self.done)

		self.uart = UART()
		self.dialog = SettingsDialog()


	def createChannel(self, chName, chList):
		channel_layout = QVBoxLayout()
		channel_groupbox = QGroupBox(self)
		channel_groupbox.setStyleSheet("font-weight: bold;")
		channel_groupbox.setTitle(chName)
		channel_groupbox.setLayout(channel_layout)
		channel_groupbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		channel_widget = Channel(self, chList)
		channel_widget.setStyleSheet("font-weight:normal;")
		channel_widget.item_selected.connect(self.onComboBoxSelected)
		self.channels.append(channel_widget)

		channel_layout.addWidget(channel_widget)

		return channel_groupbox


	def createCurrentGen(self):
		channel_layout = QVBoxLayout()
		currentgen_groupbox = QGroupBox("Current Generation", self)
		currentgen_groupbox.setStyleSheet("font-weight:bold;")
		currentgen_groupbox.setLayout(channel_layout)
		currentgen_groupbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.currentGen = CurrentGeneration(self)
		self.channels.append(self.currentGen)
		self.currentGen.setStyleSheet("font-weight:normal;")
		channel_layout.addWidget(self.currentGen)

		return currentgen_groupbox


	def createPR(self):
		pr_layout = QVBoxLayout()
		pr_groupbox = QGroupBox("Pseudo Resistors", self)
		pr_groupbox.setStyleSheet("font-weight:bold;")
		pr_groupbox.setLayout(pr_layout)
		pr_groupbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.pr = PR(self)
		self.pr.setStyleSheet("font-weight:normal;")
		pr_layout.addWidget(self.pr)

		return pr_groupbox

	def onComboBoxSelected(self, ch):
		channelMap = {
		1: (1, 0),
		5: (1, 1),
		2: (0, 0),
		6: (0, 1),
		3: (3, 0),
		7: (3, 1),
		4: (2, 0),
		8: (2, 1)}
		a,b = channelMap[ch]
		self.channels[a].changeItem(b)


	def testConnection(self):
		packet = []
		packet.append(84)
		self.statusCircle.setStatus(self.uart.uartSendReceive(packet) == UART.UART_SUCCESS)


	def settings(self):
		self.dialog.setValues(self.uart.getBaudRate(), self.uart.getPort())
		self.dialog.settingsSaved.connect(self.handleSettingsSaved)
		self.dialog.exec_()


	def handleSettingsSaved(self, baudRate, port):
		self.uart.baudRate = baudRate
		self.uart.port = port


	def about(self):
		pass


	def done(self):
		# Lock the window size
		self.setFixedSize(self.size())


	def upload(self):
		fscvMotherBoard = FM.FSCVMotherboard()
		fscvMotherBoard.initChannel('A', self.channels[0].getValues())
		fscvMotherBoard.initChannel('B', self.channels[1].getValues())
		fscvMotherBoard.initChannel('C', self.channels[2].getValues())
		fscvMotherBoard.initChannel('D', self.channels[3].getValues())
		fscvMotherBoard.initChannel('DE', self.channels[4].getValues())

		iref_values = self.currentGen.getValues()
		fscvMotherBoard.initIref(FM.FSCVMotherboard.CH_12, iref_values[FM.FSCVMotherboard.CH_12])
		fscvMotherBoard.initIref(FM.FSCVMotherboard.CH_34, iref_values[FM.FSCVMotherboard.CH_34])
		fscvMotherBoard.initIref(FM.FSCVMotherboard.CH_56, iref_values[FM.FSCVMotherboard.CH_56])
		fscvMotherBoard.initIref(FM.FSCVMotherboard.CH_78, iref_values[FM.FSCVMotherboard.CH_78])
		fscvMotherBoard.initIref(FM.FSCVMotherboard.CH_DE, iref_values[FM.FSCVMotherboard.CH_DE])

		fscvMotherBoard.initPR(self.pr.getValues())

		port_values = fscvMotherBoard.getValues()
		packet = []
		packet.append(83)  # ASCII Value of S
		packet.append(port_values[FM.FSCVMotherboard.MCU_PORT3])
		packet.append(port_values[FM.FSCVMotherboard.MCU_PORT4])
		packet.append(port_values[FM.FSCVMotherboard.MCU_PORT6])
		packet.append(port_values[FM.FSCVMotherboard.MCU_PORT7])
		packet.append(port_values[FM.FSCVMotherboard.IOE1_PORT0])
		packet.append(port_values[FM.FSCVMotherboard.IOE1_PORT1])
		packet.append(port_values[FM.FSCVMotherboard.IOE2_PORT0])
		packet.append(port_values[FM.FSCVMotherboard.IOE2_PORT1])
		print(port_values[FM.FSCVMotherboard.MCU_PORT6])
		# print(fscvMotherBoard.getValues())
		self.statusCircle.setStatus(self.uart.uartSendReceive(packet) == UART.UART_SUCCESS)


def main():
	app = QApplication(sys.argv)
	window = MainWindow()
	window.setGeometry(100, 100, 400, 200)
	window.show()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()
