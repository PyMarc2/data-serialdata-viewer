from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt, QTimer, QThreadPool, pyqtSignal, QTime
from threadWorker import Worker
from PyQt5 import QtCore
from mainWindowUi import Ui_ViewerWidget
#import serialMock as serial
import serial
import sys
import glob


class MainWindow(QWidget, Ui_ViewerWidget):
    resized = QtCore.pyqtSignal()
    writeSignal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # VARIABLES DECLARATION
        self.selectedPort = ''
        self.connectedPort = ''
        self.connected = 0
        self.baudrate = 9600

        self.checkbox_Autoscroll.setChecked(True)
        self.autoScroll = 1

        # INITIALISATION SERIAL COMMUNICATION
        self.ports = self.scanPorts()
        self.comboBox_port.addItems(self.ports)

        # INSERT TERMINAL IN MAIN WINDOW
        self.threadPool = QThreadPool()
        self.writeSignal.connect(self.writeTerminal)
        self.terminalWorker = None

        # TERMINAL CONNECTIONS
        self.lineEdit_baudrate.textChanged.connect(self.updateBaudrate)
        self.updateBaudrate()
        self.lineEdit_baudrate.returnPressed.connect(self.Connect)

        self.comboBox_port.currentTextChanged.connect(self.updatePort)
        self.updatePort()

        self.checkBox_Terminal.setChecked(True)
        self.checkBox_Terminal.stateChanged.connect(self.showTerminal)

        self.pushButton_Connect.clicked.connect(self.Connect)
        self.checkbox_Autoscroll.stateChanged.connect(self.autoScrollEnable)

        # GRAPHICAL FUNCTIONS SETTINGS
        self.SpinBox_numberSelect.valueChanged.connect(self.updateSensorNumber)
        self.pushButton_Place.clicked.connect(self.placeSensors)

        self.resized.connect(self.updateSizePosition)

        # INTERACTION FUNCTIONS
        self.widget_Mpl.canvas.mpl_connect('button_press_event', self.clickRectangle)

        # COLOR SELECTION SETTINGS
        color_dict = {
            'red': '#ff0000',
            'green': '#00ff00',
            'blue': '#0000ff',
            'yellow': '#ffff00',
            'gold': '#ffd700',
            'pink': '#ffc0cb',
            'bisque': '#ffe4c4',
            'ivory': '#fffff0',
            'black': '#000000',
            'white': '#ffffff',
            'violet': '#ee82ee',
            'silver': '#c0c0c0',
            'forestgreen': '#228b22',
            'brown': '#a52a3a',
            'chocolate': '#d2691e',
            'azure': '#fffff0',
            'orange': '#ffa500'
        }
        self.comboBox_minColor.addItems(color_dict)
        self.comboBox_maxColor.addItems(color_dict)
        self.comboBox_minColor.currentTextChanged.connect(self.updateColors)
        self.comboBox_maxColor.currentTextChanged.connect(self.updateColors)
        self.lineEdit_minColor.returnPressed.connect(self.updateColors)
        self.lineEdit_maxColor.returnPressed.connect(self.updateColors)

    # =========== TERMINAL FUNCTIONS ============== #
    def scanPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        print("Found devices:", result)
        return result

    def updateBaudrate(self):
        try:
            localBaudrate = int(self.lineEdit_baudrate.text())
            self.baudrate = localBaudrate
            print("Baudrate has been changed to: %i bits/s" % self.baudrate)
        except ValueError:
            if self.lineEdit_baudrate.text() == "":
                self.baudrate = 0

            else:
                print("Baudrate must be a number.")
                self.lineEdit.setText("")

    def updatePort(self):
        portName = self.comboBox_port.currentText()
        self.selectedPort = portName
        print("Selected Port updated to %s" % self.selectedPort)

    def Connect(self):
        try:
            if not self.connected:

                self.serialComm = serial.Serial(port=self.selectedPort, baudrate=self.baudrate,
                                            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                            stopbits=serial.STOPBITS_ONE)
                self.connected = 1
                self.connectedPort = self.selectedPort
                self.terminalWorker = Worker(self.readSerial)
                self.threadPool.start(self.terminalWorker)
                print("Connection to Port %s succeeded." % self.connectedPort)
                self.pushButton_Connect.setText("Disconnect")
                self.pushButton_Connect.clicked.disconnect()
                self.pushButton_Connect.clicked.connect(self.Disconnect)

        except Exception as e:
            print("\nError occurred during connection initialisation to Port %s." % self.selectedPort)
            print(e)

    def Disconnect(self):
        if self.connected:
            try:
                self.connected = 0
                self.serialComm.close()
                print("Disconnection from Port %s succeeded." % self.connectedPort)
                self.pushButton_Connect.setText("Connect")
                self.pushButton_Connect.clicked.disconnect()
                self.pushButton_Connect.clicked.connect(self.Connect)

            except Exception as e:
                print("Error occurred during disconnection form Port %s" % self.connectedPort)
                print(e)
                pass

    def readSerial(self, statusSignal=None):
        print("Thread has initiated serial read")
        while self.connected:
            data = (self.serialComm.read().decode('ASCII'))
            # print(data)
            self.writeSignal.emit(data)
        else:
            print("Thread has disconnected")
            return

    def showTerminal(self):
        if self.checkBox_Terminal.isChecked():
            self.terminal.setEnabled(True)
            print("Terminal Opens")
            self.terminal.setVisible(True)
        else:
            self.terminal.setEnabled(False)
            print("Terminal Closes")
            self.terminal.setVisible(False)

    def writeTerminal(self, msg):
        self.terminal.insertPlainText(msg)
        if self.autoScroll:
            self.terminal.moveCursor(QtGui.QTextCursor.End)

    def autoScrollEnable(self):
        if self.checkbox_Autoscroll.isChecked():
            self.autoScroll = 1
        else:
            self.autoScroll = 0

    # =========== GRAPHICAL INTERACTION FUNCTIONS ============== #
    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def updateSizePosition(self):
        self.widget_Mpl.canvas.updateSizePosition()

    def updateSensorNumber(self):
        sensors = self.SpinBox_numberSelect.value()
        self.widget_Mpl.canvas.updateSensorNumber(sensors)

    def placeSensors(self):
        self.widget_Mpl.canvas.updateRelativePositions()
        self.widget_Mpl.canvas.placeSensor()


    def clickRectangle(self):
        print(self.cursor().pos())



    # ============= COLOR SELECTION FUNCTIONS ============ #
    def updateColors(self):
        self.min_color = self.comboBox_minColor.currentText()
        self.max_color = self.comboBox_maxColor.currentText()
        self.min_color_value = self.lineEdit_minColor.text()
        self.max_color_value = self.lineEdit_maxColor.text()
        print("Couleur minimale:%s" % self.min_color)
        print("Couleur maximale:%s" % self.max_color)
        print("Valeur minimale:%s" % self.min_color_value)
        print("Valeur maximale:%s" % self.max_color_value)



