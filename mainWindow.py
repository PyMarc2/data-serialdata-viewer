from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt, QTimer, QThreadPool, pyqtSignal, QTime
from threadWorker import Worker
import PyQt5.QtCore as QC
from mainWindowUi import Ui_ViewerWidget
import serial
import sys
import glob


class MainWindow(QWidget, Ui_ViewerWidget):
    resized = QC.pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)


        # VARIABLES declarations
        self.selectedPort = ''
        self.connectedPort = ''
        self.connected = 0
        self.baudrate = 9600

        # INSERT TERMINAL IN MAIN WINDOW
        self.threadPool = QThreadPool()
        self.terminalWorker = Worker(self.readSerial)

        # INITIALIZATION Functions
        self.ports = self.scanPorts()
        self.comboBox_port.addItems(self.ports)

        # TERMINAL Function connections
        self.lineEdit_baudrate.textChanged.connect(self.updateBaudrate)
        self.updateBaudrate()

        self.checkBox_Terminal.stateChanged.connect(self.showTerminal)

        self.comboBox_port.currentTextChanged.connect(self.updatePort)
        self.updatePort()

        self.pushButton_Connect.clicked.connect(self.initializeCommunication)

        # GRAPHICAL Function connections
        self.SpinBox_numberSelect.valueChanged.connect(self.updateSensorNumber)
        self.pushButton_Place.clicked.connect(self.placeSensors)

        self.resized.connect(self.updateSizePosition)



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

    def initializeCommunication(self):
        try:
            if self.connected == 0:

                self.serialComm = serial.Serial(port=self.selectedPort, baudrate=self.baudrate,
                                            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                            stopbits=serial.STOPBITS_ONE)
                self.connected = 1
                self.connectedPort = self.selectedPort
                self.threadPool.start(self.terminalWorker)
                print("Connection to Port %s succeeded." % self.connectedPort)
                self.pushButton_Connect.setText("Disconnect")

            else:
                try:
                    self.serialComm.close()
                    self.connected = 0
                    #self.threadPool.stop(self.terminalWorker)
                    print("Disconnection from Port %s succeeded." % self.connectedPort)
                    self.pushButton_Connect.setText("Connect")

                except Exception as e:
                    print("Error occurred during disconnection form Port %s" % self.connectedPort)
                    print(e)

        except Exception as e:
            print("\nError occurred during connection initialisation to Port %s." % self.selectedPort)
            print(e)

    def readSerial(self, statusSignal=None):
        print("Serial read initiated")
        while True:
            print((self.serialComm.read()))
            self.write(self.serialComm.read())
            print((self.serialComm.read()))
        else:
            print("caca ici")

    def showTerminal(self):
        if self.checkBox_Terminal.isChecked():
            self.terminal.setEnabled(True)
            print("Terminal Opens")
        else:
            self.terminal.setEnabled(False)
            print("Terminal Closes")



    # =========== GRAPHICAL INTERACTION FUNCTIONS ============== #

    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainWindow, self).resizeEvent(event)

    def indicator(self):
        print("a")

    def updateSensorNumber(self):
        sensors = self.SpinBox_numberSelect.value()
        self.widget_Mpl.canvas.updateSensorNumber(sensors)

    def placeSensors(self):
        self.widget_Mpl.canvas.updateRelativePositions()
        self.widget_Mpl.canvas.placeSensor()

    def updateSizePosition(self):
        self.widget_Mpl.canvas.getActualSensorRelativeSize()
        self.widget_Mpl.canvas.updateSizePosition()


 # ================= TERMINAL LIKE CONSOLE FOR OUTPUTTING ========== #

    def write(self, msg, statusSignal=None):
        self.messageSignal.emit()
        self.terminal.insertPlainText(msg)
        self.terminal.insertPlainText('\n')
