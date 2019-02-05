import matplotlib
from matplotlib import patches
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import itertools
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas


matplotlib.use('QT5Agg')


class MplWidgetHandler(Canvas):
    def __init__(self):
        # SET FIGURE OPTIONS
        self.fig = plt.figure(facecolor=(0.3, 0.3, 0.3))
        self.fig.set_size_inches(2,2)
        self.axes = self.fig.add_subplot(111)
        self.axes.set_frame_on(False)
        self.axes.invert_yaxis()
        self.axes.axis('off')
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)

        # SET CANVAS
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

        # SET PROGRAM OPTIONS
        self.sensorPixelSize = [128., 128.]
        print("Sensor size =", self.sensorPixelSize)
        print(self.getActualCanvasPixelSize())
        self.canvasPossibleSensorAmount()

        # SET CLASS VARIABLE INITIALISATION
        self.canvasSizePixel = []
        self.devicesNumber = 1
        self.devices = []  # [index, name, xPos, yPos, regex]
        self.relativeSensorSize = []
        self.xmax = 0
        self.ymax = 0


    def addSensor(self):
        self.devices += 1
        x, y = self.getNextPosition()
        sensorSize = self.getActualSensorRelativeSize()
        canvasSize = self.getActualCanvasPixelSize()
        self.axes.add_artist(patches.Rectangle((x/canvasSize[0], y/canvasSize[1]), sensorSize[0], sensorSize[1], edgecolor='black', facecolor='black', fill=True))
        self.draw()

    def getActualSensorRelativeSize(self):
        size = self.sensorPixelSize/(self.fig.get_size_inches() * self.fig.dpi)
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
                xPositions.append(0.5*self.sensorPixelSize[0] + 1.5*self.sensorPixelSize[0]*xPlaced)
                xPlaced = xPlaced +1
            else:
                continue

        for yIndex in range(self.ymax):
            if self.ymax - yPlaced != 0:
                yPositions.append(0.5*self.sensorPixelSize[0] + 1.5*self.sensorPixelSize[0]*yPlaced)
                yPlaced = yPlaced +1
            else:
                continue
        print(xPositions, yPositions)

        positionTuples = list(itertools.product(xPositions/self.canvasSizePixel[0], yPositions/self.canvasSizePixel[1]))
        self.relativePositionsTuples = positionTuples
        print(positionTuples)

    def placeSensor(self):
        self.getActualSensorRelativeSize()
        self.getActualCanvasPixelSize()
        self.calculateSensorRelativePosition()
        for i in self.relativePositionsTuples:
            self.axes.add_artist(
            patches.Rectangle((i[0], i[1]), self.relativeSensorSize[0], self.relativeSensorSize[1], edgecolor='black',
                              facecolor='black', fill=True))

        self.fig.subplots_adjust(0, 0, 1, 1)
        self.draw()

    def updateSensorNumber(self, number):
        self.devicesNumber = number
        print("The amount of sensors is %i" %number)

    def updateRelativePositions(self):
        self.calculateSensorRelativePosition()

    def canvasPossibleSensorAmount(self):
        canvasSize = self.getActualCanvasPixelSize()
        self.xmax = xAmount = int(round(2*canvasSize[0]/(3*self.sensorPixelSize[0])))
        self.ymax = yAmount = int(round(2 * canvasSize[1] / (3 * self.sensorPixelSize[1])))
        print("There can be %f sensor in the X axis" % xAmount)
        print("There can be %f sensor in the Y axis" % yAmount)

    def updateSizePosition(self):
        pass
        # canvasSize = self.getActualCanvasPixelSize()
        # print("Actual canvas size:", canvasSize)



