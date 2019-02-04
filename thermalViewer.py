import matplotlib
from matplotlib import patches
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
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
        self.sensorPixelSize = [64., 64.]
        print("Sensor size =", self.sensorPixelSize)
        print(self.getActualCanvasPixelSize())
        self.canvasPossibleSensorAmount()

        # SET CLASS VARIABLE INITIALISATION
        self.devicesNumber = 1
        self.devices = []  # [index, name, xPos, yPos, regex]
        self.plotCount = 0
        self.currentTime = 0
        self.timeIncrement = 5  # in seconds
        self.tickLength = 100 * self.timeIncrement
        self.maxCount = 0

    def addSensor(self):
        self.devices += 1
        x, y = self.getNextPosition()
        sensorSize = self.getActualSensorRelativeSize()
        canvasSize = self.getActualCanvasPixelSize()
        self.axes.add_artist(patches.Rectangle((x/canvasSize[0], y/canvasSize[1]), sensorSize[0], sensorSize[1], edgecolor='black', facecolor='black', fill=True))
        self.draw()

    def getActualSensorRelativeSize(self):
        size = self.sensorPixelSize / (self.fig.get_size_inches() * self.fig.dpi)
        return size

    def getActualCanvasPixelSize(self):
        size = (self.fig.get_size_inches() * self.fig.dpi)
        return size



    def calculateSensorParameters(self):
        pass

    def placeSensor(self):
        pass

    def updateSensorNumber(self, number):
        self.devicesNumber = number
        print("The amount of sensors is %i" %number)

    def canvasPossibleSensorAmount(self):
        canvasSize = self.getActualCanvasPixelSize()
        xAmount = round(2*canvasSize[0]/(3*self.sensorPixelSize[0]))
        yAmount = round(2 * canvasSize[1] / (3 * self.sensorPixelSize[1]))
        print("There can be %f sensor in the X axis" % xAmount)
        print("There can be %f sensor in the Y axis" % yAmount)



    def updateSizePosition(self):
        pass
        # canvasSize = self.getActualCanvasPixelSize()
        # print("Actual canvas size:", canvasSize)



