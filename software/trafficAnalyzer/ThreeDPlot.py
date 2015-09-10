import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
from numpy import array
import time





class ThreeDPlot:

    def __init__(self,dataExtractor,buffered=False,windowSize=None):
        self.windowSize=windowSize
        self.fig,self.subp=plt.subplots()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.angle= self.ax.azim
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["bottom"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_visible(False)
        self.buffered=buffered
        self.plots=dict()
        self.minX=float('Inf')
        self.maxX=-float('Inf')
        self.minY=float('Inf')
        self.maxY=-float('Inf')
        self.minZ=float('Inf')
        self.maxZ=-float('Inf')
        plt.grid(True)
        self.dataY=np.arange(0,16,1)
        self.dataZ=[]
        self.dataX=[]
        self.extractor=dataExtractor
        self.surf=None
        self.init=True
        self.setYLabel(self.extractor.getYLabel())
        self.setXLabel(self.extractor.getXLabel())
        self.setZLabel(self.extractor.getZLabel())
        self.setTransparentPane()
        plt.ion()
        plt.show()

    def setYLabel(self,label):
        plt.ylabel(label)


    def setXLabel(self,label):
        plt.xlabel(label)

    def setZLabel(self,label):
        self.ax.set_zlabel(label)

    def setTitle(self,title):
        plt.suptitle(title)

    def animate(self):
        self.angle=(self.angle+10)%360
        self.ax.view_init(azim=self.angle)
        self.fig.canvas.draw()

    def setTransparentPane(self):
        self.ax.w_xaxis.set_pane_color((0.8, 0.8, 0.8, 0))
        self.ax.w_yaxis.set_pane_color((0.8, 0.8, 0.8, 0))
        self.ax.w_zaxis.set_pane_color((0.8, 0.8, 0.8, 0))

    def plot(self,sample):
        if self.surf != None:
            self.surf.remove()
        newX=self.extractor.extractX(sample)
        newZ=self.extractor.extractZ(sample)
        if self.init:
            self.init=False
        else:
            self.dataX.append(newX)
            self.dataZ.append(newZ)
            if self.windowSize!=None and len(self.dataX)>self.windowSize:
                self.dataX=self.dataX[1:self.windowSize]
                self.dataZ=self.dataZ[1:self.windowSize]
            self.X,self.Y=np.meshgrid(self.dataX,self.dataY)
            self.Z=np.transpose(array(self.dataZ))
            if self.buffered==False:
                self.surf=self.ax.plot_surface(
                    self.X, self.Y, self.Z, rstride=1, cstride=1,
                    cmap=cm.jet, linewidth=0.05, antialiased=True ,alpha=0.8)
                self.fig.canvas.draw()
    def show(self):
        self.surf=self.ax.plot_surface(
            self.X, self.Y, self.Z, rstride=1, cstride=1,
            cmap=cm.jet, linewidth=0.01, antialiased=True ,alpha=0.7)
        self.fig.canvas.draw()
