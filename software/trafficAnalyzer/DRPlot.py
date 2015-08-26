import matplotlib.pyplot as plt


class DRPlot:

    def __init__(self):
        self.fig,self.subp=plt.subplots()
        self.subp.set_ylim(0.8,1.1)
        self.a0,=self.subp.plot([],[],'r')
        plt.ylabel("Delivery Rate")
        plt.xlabel("Time (s)")
        plt.suptitle("Average delivery rate")
        plt.grid(True)
        self.lastSample=None
        self.startTime=None
        self.xData=[]
        self.yData=[]
        plt.ion()
        plt.show()

    def plot(self,sample):
        if self.lastSample==None:
            time=0
            self.xData.append(time)
            self.startTime=sample.getTime()
            txNum,ackNum=sample.getTotalSum()[0]
            self.yData.append(float(ackNum)/float(txNum))
        else:
            time=sample.getTime()-self.startTime
            self.xData.append(time)
            txNum,ackNum=sample.getTotalSum()[0]
            txNumLast,ackNumLast=self.lastSample.getTotalSum()[0]
            self.yData.append(float(ackNum-ackNumLast)/float(txNum-txNumLast))
        text='m = {0}'.format(str(round(sum(self.yData)/float(len(self.yData)),4)))
        self.subp.set_title(text)
        self.subp.set_xlim(0,time)
        self.a0.set_data(self.xData,self.yData)
        self.fig.canvas.draw()
        self.lastSample=sample
