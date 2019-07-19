import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.offsetbox import AnnotationBbox, TextArea
import signal
from PyQt5 import QtCore
#from thermalViewer import MplWidgetHandler

class DraggableRectangle:
    lock = None  # only one can be animated at a time

    def __init__(self, rect, name, value, canvas):
        self.canvas = canvas
        #Rect is arectangle inside a container axes rect = axes.add_artist(patches.Rectangle)
        self.rect = rect
        self.name = name
        self.value = value
        self.press = None
        self.background = None
        self.namebackground = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        if DraggableRectangle.lock is not None: return
        contains, attrd = self.rect.contains(event)
        if not contains: return

        # Save position in file
        x0, y0 = self.rect.xy
        self.saveInFile(str(self.rect.xy))
        print("click write succeded")

        self.press = x0, y0, event.xdata, event.ydata
        DraggableRectangle.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        #the canvas and axes for the name, value and rectangle are the same
        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        self.rect.set_animated(True)
        self.name.set_animated(True)
        self.value.set_animated(True)
        #Draws on the canvas
        canvas.draw()

        #Sets the background to a copy of the axesbbox, so the whole container.
        self.background = canvas.copy_from_bbox(self.rect.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.name)
        axes.draw_artist(self.rect)
        axes.draw_artist(self.value)
        # and blit just the redrawn area
        canvas.blit(axes.bbox)

        self.canvas.checkRectangleOnClick()

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if DraggableRectangle.lock is not self:
            return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress

        # set position of the rectangle
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        self.name.set_x(self.rect.xy[0])
        self.name.set_y(self.rect.xy[1])

        self.value.set_x(self.rect.xy[0]+(self.canvas.sensorPixelSize[0]/(self.canvas.fig.get_size_inches()[0] * self.canvas.fig.dpi))/3)
        self.value.set_y(self.rect.xy[1]+(self.canvas.sensorPixelSize[1]/(self.canvas.fig.get_size_inches()[1] * self.canvas.fig.dpi))/1.8)


        canvas = self.rect.figure.canvas
        axes = self.rect.axes

        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.rect)
        axes.draw_artist(self.name)
        axes.draw_artist(self.value)

        # blit just the redrawn area
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
        self.name.set_animated(False)
        self.value.set_animated(False)

        self.background = None
        self.saveInFile(str(self.rect.xy))
        print("release write succeded\n\n")
        # redraw the full figure
        self.rect.figure.canvas.draw()

        #print("Realeased @", x0, y0)
        self.canvas.checkRectangleOnRelease()

    def saveInFile(self, drop):
        filename = "pos.txt"
        with open(filename, "w") as file:
            file.write(drop)
            file.close()


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)






