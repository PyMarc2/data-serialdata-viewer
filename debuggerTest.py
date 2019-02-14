import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib import text as mpltext
import re

class DraggableRectangle:
    lock = None  # only one can be animated at a time

    def __init__(self, rect):
        self.rect = rect
        self.press = None
        self.background = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        if DraggableRectangle.lock is not None: return
        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('Held @', self.rect.xy)
        x0, y0 = self.rect.xy
        self.saveInFile(str(self.rect.xy))
        print("click write succeded")
        self.press = x0, y0, event.xdata, event.ydata
        DraggableRectangle.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        self.rect.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.rect.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.rect)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggableRectangle.lock is not self:
            return

        x0, y0 = self.rect.xy
        self.press = None
        DraggableRectangle.lock = None

        # turn off the rect animation property and reset the background
        self.rect.set_animated(False)
        self.background = None
        self.saveInFile(str(self.rect.xy))
        print("release write succeded\n")
        # redraw the full figure
        self.rect.figure.canvas.draw()
        #print("Realeased @", x0, y0)

    def saveInFile(self, drop):
        filename = "pos.txt"
        with open(filename, "w") as file:
            file.write(drop)
            file.close()


class MyFigure:

    def __init__(self):
        # Figure initialisation
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.fig.subplots_adjust(0, 0, 1, 1)
        self.axes.set_frame_on(False)
        self.axes.invert_yaxis()
        self.axes.axis('off')
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)

        # Connections
        self.ciddouble = self.fig.canvas.mpl_connect('button_press_event', self.createRectangle)
        self.CheckClick = self.fig.canvas.mpl_connect('button_press_event', self.checkRectangleOnClick)
        self.CheckRelease = self.fig.canvas.mpl_connect('button_release_event', self.checkRectangleOnRelease)

        # Variables
        self.devices = []
        self.drs = []
        self.sensorPixelSize = [50, 50]

    def createRectangle(self, event):
        relPosX = event.x / (self.fig.get_size_inches()[0] * self.fig.dpi)
        relPosY = 1 - (event.y / (self.fig.get_size_inches()[1] * self.fig.dpi))
        relSizeX = self.sensorPixelSize[0] / (self.fig.get_size_inches()[0] * self.fig.dpi)
        relSizeY = self.sensorPixelSize[1] / (self.fig.get_size_inches()[1] * self.fig.dpi)
        absPoxX = relPosX * (self.fig.get_size_inches()[0] * self.fig.dpi)
        absPosY = relPosY * (self.fig.get_size_inches()[1] * self.fig.dpi)
        absSizeX = self.sensorPixelSize[0]
        absSizeY = self.sensorPixelSize[1]

        if event.dblclick and event.button == 1:

            rect = self.axes.add_artist(
                patches.Rectangle((relPosX, relPosY), relSizeX, relSizeY, edgecolor='black', facecolor='black',
                                  fill=True))
            dr = DraggableRectangle(rect)
            dr.connect()
            print(dr.rect.xy)
            self.drs.append(dr)
            self.fig.canvas.draw()
            local = ["", "", (relPosX, relPosY), relSizeX, relSizeY, (absPoxX, absPosY), absSizeX, absSizeY]
            self.devices.append(local)

    def checkRectangleOnClick(self, event):
        filename = "pos.txt"
        with open(filename, "r") as file:
            varia = file.read()
            file.flush()

        for i in range(len(self.devices)):
            if str(varia) == str(self.devices[i][2]):
                print("Clicked rectangle #%i" % i)
                self.clickedIndex = i

            else:
                self.clickedIndex = None

    def checkRectangleOnRelease(self, event):
        filename = "pos.txt"
        with open(filename, "r") as file:
            varia = file.read()
            file.flush()

        for i in range(len(self.devices)):
            if str(varia) == str(self.devices[i][2]):
                print("Realeased rectangle #%i" % i)
                self.clickedIndex = i

            else:
                self.clickedIndex = None



# t = mpltext.Text(0.1,0.2,'Hello')
#
# t.set_text('s')
# print(t.get_text())

data= "s4:24.55\ns3:344"
express = "\w*\d?=?:? *(\d+.?\d+)"
trouv = re.search(express, data)

print(trouv, trouv.group(1))

