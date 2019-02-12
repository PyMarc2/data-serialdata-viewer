import matplotlib
from matplotlib import patches
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog
from sensorWindowUi import Ui_Dialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from draggableRectangle import DraggableRectangle
matplotlib.use('QT5Agg')


class MplWidgetHandler(Canvas):
    def __init__(self):

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

        # GET CANVAS INFORMATION
        #self.canvasPossibleSensorAmount()
        #self.getActualCanvasPixelSize()
        #self.getActualSensorRelativeSize()
        #print("Initialization canvas pixel: ", self.canvasSizePixel)

        # CONNECT CANVAS CLICK FUNCTIONS

        self.cigdouble  = self.mpl_connect('button_press_event', self.createRectangle)
        #self.ciddouble  = self.mpl_connect('button_release_event', self.updateOnCanvasRelease)
        self.cichange    = self.mpl_connect('button_release_event', self.changeRectangle)

        self.CheckClick = self.mpl_connect('button_press_event', self.checkRectangleOnClick)
        self.CheckRelease = self.mpl_connect('button_release_event', self.checkRectangleOnRelease)

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
            #print("The rectangle selected should be created.")

            rect = self.axes.add_artist(patches.Rectangle((relPosX, relPosY), relSizeX, relSizeY, edgecolor='black', facecolor='black', fill=True))
            dr = DraggableRectangle(rect)
            dr.connect()
            #dr.rect.figure.canvas.mpl_connect('button_release_event', self.updateRectangleOnRelease)
            print(dr.rect.xy)
            self.drs.append(dr)
            self.fig.canvas.draw()
            local = ["", "", (relPosX, relPosY), relSizeX, relSizeY, (absPoxX, absPosY), absSizeX, absSizeY]
            self.devicesNumber = self.devicesNumber + 1
            self.devices.append(local)

            #print("The amount of sensors is %i" % self.devicesNumber)

    def changeRectangle(self, event):
        if event.button == 3:
           # self.updateOnCanvasRelease()
            print(self.clickedIndex)
            if self.clickedIndex != None:
                print("You are changing sensor #%i." % self.clickedIndex)
                dialog = QDialog()
                dialog.ui = Ui_Dialog()
                dialog.ui.setupUi(dialog)
                dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                dialog.exec_()

    def checkRectangleOnClick(self, event):
        filename = "pos.txt"
        with open(filename, "r") as file:
            varia = file.read()
            file.flush()

        # print("\n varia is:", varia)

        for i in range(len(self.devices)):
            if str(varia) == str(self.devices[i][2]):
                print("Clicked rectangle #%i" % i)
                self.clickedIndex = i
                self.devices[i][2] = self.drs[i].rect.xy
                self.devices[i][5] = (self.drs[i].rect.xy[0] * (self.fig.get_size_inches()[0] * self.fig.dpi),
                                      self.drs[i].rect.xy[1] * (self.fig.get_size_inches()[1] * self.fig.dpi))
            else:
                self.clickedIndex = None

    def checkRectangleOnRelease(self, event):
        filename = "pos.txt"
        with open(filename, "r") as file:
            varia = file.read()
            file.flush()

        #print("\n varia is:", varia)

        for i in range(len(self.devices)):
            if str(varia) == str(self.devices[i][2]):
                print("Realeased rectangle #%i" % i)
                self.clickedIndex = i
                self.devices[i][2] = self.drs[i].rect.xy
                self.devices[i][5] = (self.drs[i].rect.xy[0] * (self.fig.get_size_inches()[0] * self.fig.dpi), self.drs[i].rect.xy[1] * (self.fig.get_size_inches()[1] * self.fig.dpi))
            else:
                self.clickedIndex = None

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
                dr = DraggableRectangle(rect)
                dr.connect()
                self.drs.append(dr)
                self.fig.canvas.draw()

        self.draw()

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