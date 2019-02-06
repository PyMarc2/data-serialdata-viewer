import matplotlib
from matplotlib import patches
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import itertools
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from draggableRectangle import DraggableRectangle
matplotlib.use('QT5Agg')


class MplWidgetHandler(Canvas):
    def __init__(self):
        # SET FIGURE OPTIONS
        self.fig = plt.figure(facecolor=(0.3, 0.3, 0.3))
        self.fig.set_size_inches(2, 2)
        self.axes = self.fig.add_subplot(111)
        self.fig.subplots_adjust(0, 0, 1, 1)
        self.axes.set_frame_on(False)
        self.axes.invert_yaxis()
        self.axes.axis('off')
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)
        self.drs = []
        self.sensorsTemp = []


        # SET CANVAS
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

        # SET PROGRAM OPTIONS
        self.sensorPixelSize = [84., 84.]
        print("Sensor size =", self.sensorPixelSize)
        print(self.getActualCanvasPixelSize())
        self.canvasPossibleSensorAmount()

        # SET CLASS VARIABLE INITIALISATION
        self.canvasSizePixel = []
        self.devicesNumber = 0
        self.devices = []  # [index, name, xPos, yPos, regex]
        self.relativeSensorSize = []
        self.getActualCanvasPixelSize()
        self.getActualSensorRelativeSize()
        self.xmax = 0
        self.ymax = 0

        #connection to functions
        self.ciddouble = self.mpl_connect('button_press_event', self.createRectangle)


    def createRectangle(self, event):
        print(event.x, event.y, event.dblclick)
        if event.dblclick:
            print("Nemo")
            rect = self.axes.add_artist(patches.Rectangle((0.1, 0.1), self.relativeSensorSize[0], self.relativeSensorSize[1],
                              edgecolor='black',
                              facecolor='black', fill=True))
            dr = DraggableRectangle(rect)
            dr.connect()
            self.drs.append(dr)
            self.draw()
            print("Doris")

    def getActualSensorRelativeSize(self):
        size = self.sensorPixelSize / (self.fig.get_size_inches() * self.fig.dpi)
        self.relativeSensorSize = size
        print("Relative size of sensor %f, %f " % (size[0], size[1]))
        return size

    def getActualCanvasPixelSize(self):
        size = (self.fig.get_size_inches() * self.fig.dpi)
        self.canvasSizePixel = size
        return size

    def calculateSensorRelativePosition(self):
        self.canvasPossibleSensorAmount()
        self.placedSensor = 0
        xPositions = []
        yPositions = []
        xPlaced = 0
        yPlaced = 0
        for xIndex in range(self.xmax):
            if self.xmax - xPlaced != 0:
                xPositions.append(0.5 * self.sensorPixelSize[0] + 1.5 * self.sensorPixelSize[0] * xPlaced)
                xPlaced = xPlaced + 1
            else:
                continue

        for yIndex in range(self.ymax):
            if self.ymax - yPlaced != 0:
                yPositions.append(0.5 * self.sensorPixelSize[0] + 1.5 * self.sensorPixelSize[0] * yPlaced)
                yPlaced = yPlaced + 1
            else:
                continue
        print(xPositions, yPositions)

        positionTuples = list(
            itertools.product(xPositions / self.canvasSizePixel[0], yPositions / self.canvasSizePixel[1]))
        self.relativePositionsTuples = positionTuples
        print(positionTuples)

    def calculateNewRelativePosition(self):
        self.canvasPossibleSensorAmount()
        self.placedSensor = 0

        for sensorIndex in range(len(self.sensorsTemp)):
            self.sensorsTemp[sensorIndex][2] = self.sensorsTemp[sensorIndex][6]/self.canvasSizePixel[0]
            self.sensorsTemp[sensorIndex][3] = self.sensorsTemp[sensorIndex][7] / self.canvasSizePixel[1]
            self.sensorsTemp[sensorIndex][4] = self.sensorsTemp[sensorIndex][8] / self.canvasSizePixel[0]
            self.sensorsTemp[sensorIndex][5] = self.sensorsTemp[sensorIndex][9] / self.canvasSizePixel[1]

    def placeSensor(self):
        self.getActualSensorRelativeSize()
        self.getActualCanvasPixelSize()
        self.calculateSensorRelativePosition()
        self.resetSensors()
        placed = 0
        for i in self.relativePositionsTuples:
            if self.devicesNumber - placed != 0:
                self.axes.add_artist(
                    patches.Rectangle((i[0], i[1]), self.relativeSensorSize[0], self.relativeSensorSize[1],
                                      edgecolor='black',
                                      facecolor='black', fill=True))
                placed = placed + 1
                localDevice = ["", "", i[0], i[1], self.relativeSensorSize[0], self.relativeSensorSize[1],
                               i[0] * self.canvasSizePixel[0], i[1] * self.canvasSizePixel[1],
                               self.relativeSensorSize[0] * self.canvasSizePixel[0],
                               self.relativeSensorSize[1] * self.canvasSizePixel[1]]
                '''Local device = ["Name", "regular expression", xRelPos, yRelPos, xRelSize, yRelSize, xAbsPos, yAbsPos, xAbsSize, yAbsSize]'''
                self.devices.append(localDevice)
        self.draw()

    def updateSensorNumber(self, number):
        self.devicesNumber = number
        print("The amount of sensors is %i" % number)

    def updateRelativePositions(self):
        self.calculateSensorRelativePosition()

    def canvasPossibleSensorAmount(self):
        canvasSize = self.getActualCanvasPixelSize()
        self.xmax = xAmount = int(
            round(canvasSize[0] / ((3 / 2) * self.sensorPixelSize[0] + 0.5 * self.sensorPixelSize[0])))
        self.ymax = yAmount = int(
            round(canvasSize[1] / ((3 / 2) * self.sensorPixelSize[1] + 0.5 * self.sensorPixelSize[1])))
        print("There can be %f sensor in the X axis" % xAmount)
        print("There can be %f sensor in the Y axis" % yAmount)

    def resetSensors(self):
        '''When new sensors are places, the graph must reset in order to add the new sensors'''
        self.devices = []
        self.axes.clear()
        self.fig.subplots_adjust(0, 0, 1, 1)
        self.axes.set_frame_on(False)
        self.axes.invert_yaxis()
        self.axes.axis('off')
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)
        pass

    def saveSensorsTemp(self):
        self.sensorsTemp = self.devices

    def updateSizePosition(self):
        '''When the window is resized, the size and the position of the rectangles have to be updated'''
        self.saveSensorsTemp()
        self.resetSensors()
        self.getActualCanvasPixelSize()
        self.calculateNewRelativePosition()

        placed = 0
        for sensor in self.sensorsTemp:
            if self.devicesNumber - placed != 0:
                self.axes.add_artist(
                    patches.Rectangle((sensor[2], sensor[3]), sensor[4], sensor[5],
                                      edgecolor='black',
                                      facecolor='black', fill=True))
                placed = placed + 1
                localDevice = sensor
                '''Local device = ["Name", "regular expression", xRelPos, yRelPos, xRelSize, yRelSize, xAbsPos, yAbsPos, xAbsSize, yAbsSize]'''
                self.devices.append(localDevice)
        self.draw()
