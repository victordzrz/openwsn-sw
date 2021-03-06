import matplotlib.pyplot as plt


class LinePlot:

    def __init__(self,dataExtractor,buffered=False):
        self.setUpColor()
        self.buffered=buffered
        self.fig,self.subp=plt.subplots()
        box=self.subp.get_position()
        self.subp.set_position([box.x0, box.y0, box.width * 0.9, box.height])
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
        self.title=None
        plt.ion()
        plt.show()

    def setYLabel(self,label):
        plt.ylabel(label)

    def setXLabel(self,label):
        plt.xlabel(label)

    def setTitle(self,title):
        plt.suptitle(title)
        self.title=title

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
        self.subp.set_xlim(self.minX*0.999,self.maxX*1.001)
        self.subp.set_ylim(self.minY*0.999,self.maxY*1.001)


    def plot(self,sample):
        newY=self.extractor.extractY(sample)
        newX=self.extractor.extractX(sample)
        for y in sorted(newY.keys()):
            if y not in self.plots.keys():
                self.plots[y],=self.subp.plot([],[],lw=2,\
                    color=self.tableau20[len(self.plots.keys())])
                self.plots[y].set_label(y)
                self.dataY[y]=list()
                self.dataX[y]=list()
            self.dataY[y].append(newY[y])
            self.dataX[y].append(newX)
            self.plots[y].set_data(self.dataX[y],self.dataY[y])
        self.subp.legend(loc='center left',fontsize=8,bbox_to_anchor=(1, 0.5)).draggable()
        self.adjustLimits()
        if self.buffered==False:
            self.fig.canvas.draw()
        self.lastSample=sample

    def show(self):
        self.fig.canvas.draw()

    def save(self):
        self.fig.savefig(str(self.title)+'.pdf')

    def setUpColor(self):
        # These are the "Tableau 20" colors as RGB.
        self.tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),\
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),\
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),\
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),\
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
        for i in range(len(self.tableau20)):
            r, g, b = self.tableau20[i]
            self.tableau20[i] = (r / 255., g / 255., b / 255.)
