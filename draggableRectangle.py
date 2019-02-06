import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

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
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)


    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        if DraggableRectangle.lock is not None: return
        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('event contains', self.rect.xy)
        x0, y0 = self.rect.xy
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

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if DraggableRectangle.lock is not self:
            return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)

        canvas = self.rect.figure.canvas
        axes = self.rect.axes
        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.rect)

        # blit just the redrawn area
        canvas.blit(axes.bbox)

    def on_release(self, event):
        'on release we reset the press data'
        if DraggableRectangle.lock is not self:
            return

        self.press = None
        DraggableRectangle.lock = None

        # turn off the rect animation property and reset the background
        self.rect.set_animated(False)
        self.background = None

        # redraw the full figure
        self.rect.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)

class myFig:
    def __init__(self):
        self.fig = plt.figure()
        self.fig.set_size_inches(2, 2)
        self.axes = self.fig.add_subplot(111)
        self.fig.subplots_adjust(0, 0, 1, 1)
        self.axes.set_frame_on(False)
        self.axes.invert_yaxis()
        self.axes.axis('off')
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)
        self.press = None
        self.relativeSensorSize = [0.1, 0.1]
        self.connect()
    def connect(self):
        'connect to all the events we need'
        self.ciddouble = self.fig.canvas.mpl_connect('button_press_event', self.createRectangle)

    def createRectangle(self, event):
        print(event.x, event.y, event.dblclick)
        if event.dblclick:
            print("Nemo")
            rect = self.axes.add_artist(patches.Rectangle((0.1, 0.1), self.relativeSensorSize[0], self.relativeSensorSize[1],
                              edgecolor='black',
                              facecolor='black', fill=True))
            dr = DraggableRectangle(rect)
            dr.connect()
            drs.append(dr)
            self.fig.canvas.draw()
            self.fig.show()
            print("Doris")

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.fig.canvas.mpl_disconnect(self.ciddouble)





