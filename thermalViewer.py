import matplotlib
import re
from matplotlib import patches
from matplotlib import text as mpltext
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from sensorWindowUi import Ui_Dialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from draggableRectangle import DraggableRectangle
matplotlib.use('QT5Agg')


class MplWidgetHandler(Canvas):
    def __init__(self):
        self.dialog = None
        # SET FIGURE OPTIONS
        self.fig = plt.figure(facecolor=(0.3, 0.3, 0.3))
        self.axes = self.fig.add_subplot(111)
        self.fig.subplots_adjust(0, 0, 1, 1)
        self.axes.set_frame_on(False)
        self.axes.invert_yaxis()
        self.axes.axis('off')
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)

        # SET CANVAS OF FIGURE
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

        # SET PROGRAM OPTIONS
        self.sensorPixelSize = [84., 84.]
        print("Sensor size =", self.sensorPixelSize)

        # DECLARE GENERAL VARIABLES
        self.devices = []  # [name, re, xRelPos, yRelPos, xRelSize, yRelSize, xAbsPos, yAbsPos, xAbsSize, yAbsSize]
        self.drs = []
        self.clickedIndex = None
        self.devicesNumber = 0
        self.xmax = 0
        self.ymax = 0

        # CONNECT CANVAS CLICK FUNCTIONS

        self.cigdouble  = self.mpl_connect('button_press_event', self.createRectangle)
        #self.ciddouble  = self.mpl_connect('button_release_event', self.updateOnCanvasRelease)
        self.cichange    = self.mpl_connect('button_release_event', self.changeRectangle)

    # ===== BASIC RECTANGLE CREATION ===== #
    def createRectangle(self, event):
        #print(event.x, event.y, event.dblclick)

        relPosX = event.x / (self.fig.get_size_inches()[0] * self.fig.dpi)
        relPosY = 1 - (event.y / (self.fig.get_size_inches()[1] * self.fig.dpi))
        relSizeX = self.sensorPixelSize[0]/(self.fig.get_size_inches()[0] * self.fig.dpi)
        relSizeY = self.sensorPixelSize[1]/(self.fig.get_size_inches()[1] * self.fig.dpi)
        absPoxX = relPosX * (self.fig.get_size_inches()[0] * self.fig.dpi)
        absPosY = relPosY * (self.fig.get_size_inches()[1] * self.fig.dpi)
        absSizeX = self.sensorPixelSize[0]
        absSizeY = self.sensorPixelSize[1]

        if event.dblclick and event.button == 1:

            rect = self.axes.add_artist(patches.Rectangle((relPosX, relPosY), relSizeX, relSizeY, edgecolor='black', facecolor='black', fill=True))
            text = self.axes.add_artist(mpltext.Text(relPosX, relPosY, 'Name'))
            value = self.axes.add_artist(mpltext.Text(relPosX+relSizeX/3, relPosY+relSizeY/1.8, 'value', color='white'))
            dr = DraggableRectangle(rect, text, value, self)
            dr.connect()
            print(dr.rect.xy)
            self.drs.append(dr)
            self.fig.canvas.draw()
            local = ["", "", (relPosX, relPosY), relSizeX, relSizeY, (absPoxX, absPosY), absSizeX, absSizeY, "", 0.0, 0.0, ""]
            self.devicesNumber = self.devicesNumber + 1
            self.devices.append(local)

    def deleteRectangle(self, event):
        ''' TODO: Implement deleteRectangle function '''
        pass

    def checkRectangleOnClick(self):
        filename = "pos.txt"
        with open(filename, "r") as file:
            varia = file.read()
            file.flush()

        for i in range(len(self.devices)):
            verify = str(self.devices[i][2])
            if str(varia) == verify:
                print("Clicked rectangle #%i" % i)
                self.clickedIndex = i
                break

            else:
                self.clickedIndex = None

    def checkRectangleOnRelease(self):
            i = self.clickedIndex
            self.devices[i][2] = self.drs[i].rect.xy
            self.devices[i][5] = (self.drs[i].rect.xy[0] * (self.fig.get_size_inches()[0] * self.fig.dpi), self.drs[i].rect.xy[1] * (self.fig.get_size_inches()[1] * self.fig.dpi))

    def resetCanvas(self):
        '''When new sensors are places, the graph must reset in order to add the new sensors'''
        #self.devices = []
        self.axes.clear()
        self.fig.subplots_adjust(0, 0, 1, 1)
        self.axes.set_frame_on(False)
        self.axes.invert_yaxis()
        self.axes.axis('off')
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)

    def updateSizePosition(self):
        '''TODO: REPAIR, broken because of changes on the devices list.'''
        '''When the window is resized, the size and the position of the rectangles have to be updated'''
        self.resetCanvas()
        for sensorIndex in range(len(self.devices)):
            self.devices[sensorIndex][2] = (self.devices[sensorIndex][5][0] / (self.fig.get_size_inches()[0] * self.fig.dpi), self.devices[sensorIndex][5][1] / (self.fig.get_size_inches()[1] * self.fig.dpi))
            self.devices[sensorIndex][3] = self.devices[sensorIndex][6] / (self.fig.get_size_inches()[0] * self.fig.dpi)
            self.devices[sensorIndex][4] = self.devices[sensorIndex][7] / (self.fig.get_size_inches()[1] * self.fig.dpi)

        self.drs = []
        placed = 0
        for sensor in self.devices:
            if self.devicesNumber - placed != 0:
                rect = self.axes.add_artist(patches.Rectangle((sensor[2][0], sensor[2][1]), sensor[3], sensor[4], edgecolor='black', facecolor='black', fill=True))
                placed = placed + 1
                dr = DraggableRectangle(rect, self)
                dr.connect()
                self.drs.append(dr)
                self.fig.canvas.draw()

        self.draw()

    # ===== RECTANGLE OPTIONS AND MORE ===== #
    def refreshCanvas(self):
        self.resetCanvas()
        self.updateSizePosition()

    def changeRectangle(self, event):
        if event.button == 3:
            if self.clickedIndex != None:
                print("You are changing sensor #%i." % self.clickedIndex)

                # Initialisation
                self.dialog = QDialog()
                self.dialog.ui = Ui_Dialog()
                self.dialog.ui.setupUi(self.dialog)
                self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)

                # Settings
                self.dialog.setWindowTitle("Sensor {} Options".format(self.clickedIndex))
                self.dialog.ui.comboBox_colorMap.addItems(['None', 'Viridis', 'Jet', 'Polar'])
                self.loadRectangleOptions()

                # Connections
                self.dialog.ui.pushButton_ok.clicked.connect(self.updateRectangleOptions)

                #self.dialog.ui.lineEdit_Name.setText()
                # self.dialog.ui.lineEdit_re.text()
                # self.dialog.ui.lineEdit_min.text()
                #self.dialog.ui.comboBox_colorMap.setCurrentText()

                self.dialog.exec_()

    def loadRectangleOptions(self):
        self.dialog.ui.lineEdit_Name.setText(str(self.devices[self.clickedIndex][0]))
        self.dialog.ui.lineEdit_re.setText(str(self.devices[self.clickedIndex][1]))
        self.dialog.ui.comboBox_colorMap.setCurrentText(str(self.devices[self.clickedIndex][8]))
        self.dialog.ui.lineEdit_min.setText(str(self.devices[self.clickedIndex][9]))
        self.dialog.ui.lineEdit_max.setText(str(self.devices[self.clickedIndex][10]))

    def updateRectangleOptions(self):
        self.errorOptions = 0
        self.msgbox = QMessageBox()
        self.msgbox.setIcon(QMessageBox.Warning)
        self.msgbox.setText("Warning")
        self.msgbox.setWindowTitle("Option format warning")
        try:
            self.devices[self.clickedIndex][0] = self.dialog.ui.lineEdit_Name.text()
        except Exception:
            self.errorOptions = 1
            self.msgbox.setInformativeText("You must enter text which complies with the UTF-8 encoding.")
            self.msgbox.exec_()

        try:
            self.devices[self.clickedIndex][1] = (self.dialog.ui.lineEdit_re.text())
        except Exception:
            self.errorOptions = 1
            self.msgbox.setInformativeText("You must enter a valid regular expression.")
            self.msgbox.exec_()

        try:
            self.devices[self.clickedIndex][8] = self.dialog.ui.comboBox_colorMap.currentText()
        except Exception:
            self.errorOptions = 1
            self.msgbox.setInformativeText("You must enter a valid Colormap.")
            self.msgbox.exec_()

        try:
            self.devices[self.clickedIndex][9] = float(self.dialog.ui.lineEdit_min.text())
        except Exception:
            self.errorOptions = 1
            self.msgbox.setInformativeText("You must enter a number.")
            self.msgbox.exec_()

        try:
            self.devices[self.clickedIndex][10] = float(self.dialog.ui.lineEdit_max.text())

        except Exception:
            self.errorOptions = 1
            self.msgbox.setInformativeText("You must enter a number.")
            self.msgbox.exec_()

        if not self.errorOptions:
            self.dialog.close()
            self.drs[self.clickedIndex].name.set_text(self.devices[self.clickedIndex][0])

            print("Object name:", self.drs[self.clickedIndex].name.get_text())
            print("Device:", self.devices[self.clickedIndex])
            print("Options updated.")

    # ===== LIVE RE DATA FETCHING FROM SERIAL ===== #
    def fetchFromSerial(self, data):
        '''TODO: Implement fetchFromSerial function'''
        #print("Initialization of regex evaluation")
        for i in range(len(self.devices)):
            regex = self.devices[i][1]
            regexTest = "\w*\d?=?:? *(\d+.?\d+)"
            research = re.search(regexTest, data)
            if len(research.group())>0:
                self.devices[i][11] = research.group(1)
                self.drs[i].value.set_animated(True)
                self.drs[i].value.set_text(research.group(1))
                print(self.drs[i].value.get_text())

                #self.background = self.copy_from_bbox(self.axes.bbox)
                #self.restore_region(self.background)
                self.draw()

                #self.blit(self.axes.bbox)


            else:
                print("bozo")

    def updateRectangleValue(self):
        '''TODO: Implement updateRectangleValue function'''
        pass

    def updateRectangleColor(self):
        '''TODO: Implement updateRectanlgeColor function'''
        pass


    # OLD FUNCTION THAT MIGHT BE REUSED IN THE FUTURE
    # def deleteRectangle(self, event):
    #     if event.dblclick==False and event.button == 2:
    #         if self.clickedIndex != None:
    #             print("The rectangle %i should disseapear." % self.clickedIndex)
    #             del self.devices[self.clickedIndex]
    #             self.devicesNumber = self.devicesNumber -1
    #             del self.drs[self.clickedIndex]
    #             self.updateSizePosition()

    # Possibly obsolete functions

    # def placeSensor(self):
    #     self.getActualSensorRelativeSize()
    #     self.getActualCanvasPixelSize()
    #     self.calculateSensorRelativePosition()
    #     self.resetSensors()
    #     placed = 0
    #     for i in self.relativePositionsTuples:
    #         if self.devicesNumber - placed != 0:
    #             self.axes.add_artist(
    #                 patches.Rectangle((i[0], i[1]), self.relativeSensorSize[0], self.relativeSensorSize[1],
    #                                   edgecolor='black',
    #                                   facecolor='black', fill=True))
    #             placed = placed + 1
    #             localDevice = ["", "", i[0], i[1], self.relativeSensorSize[0], self.relativeSensorSize[1],
    #                            i[0] * self.canvasSizePixel[0], i[1] * self.canvasSizePixel[1],
    #                            self.relativeSensorSize[0] * self.canvasSizePixel[0],
    #                            self.relativeSensorSize[1] * self.canvasSizePixel[1]]
    #             '''Local device = ["Name", "regular expression", xRelPos, yRelPos, xRelSize, yRelSize, xAbsPos, yAbsPos, xAbsSize, yAbsSize]'''
    #             self.devices.append(localDevice)
    #     self.draw()

    # def canvasPossibleSensorAmount(self):
    #     canvasSize = (self.fig.get_size_inches() * self.fig.dpi)
    #     self.xmax = xAmount = int(
    #         round(canvasSize[0] / ((3 / 2) * self.sensorPixelSize[0] + 0.5 * self.sensorPixelSize[0])))
    #     self.ymax = yAmount = int(
    #         round(canvasSize[1] / ((3 / 2) * self.sensorPixelSize[1] + 0.5 * self.sensorPixelSize[1])))
    #     #print("There can be %f sensor in the X axis" % xAmount)
    #     #print("There can be %f sensor in the Y axis" % yAmount)

    # def calculateSensorArrayPosition(self):
    #     self.canvasPossibleSensorAmount()
    #     self.placedSensor = 0
    #     xPositions = []
    #     yPositions = []
    #     xPlaced = 0
    #     yPlaced = 0
    #     for xIndex in range(self.xmax):
    #         if self.xmax - xPlaced != 0:
    #             xPositions.append(0.5 * self.sensorPixelSize[0] + 1.5 * self.sensorPixelSize[0] * xPlaced)
    #             xPlaced = xPlaced + 1
    #         else:
    #             continue
    #
    #     for yIndex in range(self.ymax):
    #         if self.ymax - yPlaced != 0:
    #             yPositions.append(0.5 * self.sensorPixelSize[0] + 1.5 * self.sensorPixelSize[0] * yPlaced)
    #             yPlaced = yPlaced + 1
    #         else:
    #             continue
    #     print(xPositions, yPositions)
    #
    #     positionTuples = list(
    #         itertools.product(xPositions / self.canvasSizePixel[0], yPositions / self.canvasSizePixel[1]))
    #     self.relativePositionsTuples = positionTuples
    #     print(positionTuples)