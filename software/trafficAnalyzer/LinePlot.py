import matplotlib.pyplot as plt


class LinePlot:

    def __init__(self,dataExtractor,buffered=False):
        self.buffered=buffered
        self.fig,self.subp=plt.subplots()
        self.plots=dict()
        self.minX=float('Inf')
        self.maxX=-float('Inf')
        self.minY=float('Inf')
        self.maxY=-float('Inf')
        plt.grid(True)
        self.lastSample=None
        self.startTime=None
        self.dataY=dict()
        self.dataX=dict()
        self.extractor=dataExtractor
        self.setYLabel(self.extractor.getYLabel())
        self.setXLabel(self.extractor.getXLabel())
        plt.ion()
        plt.show()

    def setYLabel(self,label):
        plt.ylabel(label)

    def setXLabel(self,label):
        plt.xlabel(label)

    def setTitle(self,title):
        plt.suptitle(title)

    def adjustLimits(self):
        for key in self.dataY.keys():
            if self.dataY[key][-1]>self.maxY:
                self.maxY=self.dataY[key][-1]
            if self.dataY[key][-1]<self.minY:
                self.minY=self.dataY[key][-1]
        for key in self.dataX.keys():
            if self.dataX[key][-1]>self.maxX:
                self.maxX=self.dataX[key][-1]
            if self.dataX[key][-1]<self.minX:
                self.minX=self.dataX[key][-1]
        self.subp.set_xlim(self.minX*0.95,self.maxX*1.05)
        self.subp.set_ylim(self.minY*0.95,self.maxY*1.05)


    def plot(self,sample):
        newY=self.extractor.extractY(sample)
        newX=self.extractor.extractX(sample)
        for y in newY.keys():
            if y not in self.plots.keys():
                self.plots[y],=self.subp.plot([],[],'-')
                self.plots[y].set_label(y)
                self.dataY[y]=list()
                self.dataX[y]=list()
            self.dataY[y].append(newY[y])
            self.dataX[y].append(newX)
            self.plots[y].set_data(self.dataX[y],self.dataY[y])
        self.subp.legend(loc=2,fontsize=8)
        self.adjustLimits()
        if self.buffered==False:
            self.fig.canvas.draw()
        self.lastSample=sample

    def show(self):
        self.fig.canvas.draw()
