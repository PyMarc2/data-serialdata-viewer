import matplotlib.pyplot as plt
from matplotlib import patches
from draggableRectangle import DraggableRectangle

class myFigure():

    def __init__(self):
        self.fig = plt.figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.fig.subplots_adjust(0, 0, 1, 1)
        self.axes.set_frame_on(False)
        self.axes.invert_yaxis()
        self.axes.axis('off')
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)
        self.ciddouble = self.fig.canvas.mpl_connect('button_press_event', self.createRectangle)

        self.object = []

    def createRectangle(self, event):
        print(event.x, event.y, event.dblclick)

        relPosX = event.x / (self.fig.get_size_inches() * self.fig.dpi)[0]
        relPosY = 1- (event.y / (self.fig.get_size_inches() * self.fig.dpi)[1])

        if event.dblclick and event.button == 1:
            print("Relative X Rectangle Position:", relPosX)
            print("Relative Y Rectangle Position:", relPosY)

            shape = self.axes.add_artist(patches.Rectangle((relPosX, relPosY), 0.1, 0.1, edgecolor='black', facecolor='black', fill=True))
            dr = DraggableRectangle(shape)
            dr.connect()
            drs.append(dr)
            self.fig.canvas.draw()


fig = myFigure()
drs = []
plt.show()