import matplotlib.pyplot as plt


class MotesPlot:

    def __init__(self):
        self.fig,self.subp=plt.subplots()
        self.subp.set_xlim(0,300)
        self.subp.set_ylim(0.8,1.1)
        self.motesPlot=None
        plt.ylabel("Delivery Rate")
        plt.xlabel("Time (s)")
        plt.suptitle("Delivery rate by mote")
        plt.grid(True)
        self.lastSample=None
        self.startTime=None
        self.motesData=None
        plt.ion()
        plt.show()

    def plot(self,sample):
        if self.lastSample==None:
            time=0
            self.startTime=sample.getTime()
            self.motesPlot=dict()
            self.motesData=dict()
            for mote in sample.getMotesIP():
                txNum,ackNum=sample.getDataByMote(mote)[0]
                self.motesPlot[mote],=self.subp.plot([],[],'-')
                self.motesPlot[mote].set_label(mote)
                self.motesData[mote]=[[time],[float(ackNum)/float(txNum)]]
            self.subp.legend(loc=2,fontsize=8)
        else:
            time=sample.getTime()-self.startTime
            titleText='m = ['
            for mote in sample.getMotesIP():
                titleText+=mote+'='+str(str(round(sum(self.motesData[mote][1])/float(len(self.motesData[mote][1])),4)))+' '
                self.motesData[mote][0].append(time)
                txNum,ackNum=sample.getDataByMote(mote)[0]
                txNumLast,ackNumLast=self.lastSample.getDataByMote(mote)[0]
                self.motesData[mote][1].append(float(ackNum-ackNumLast)/float(txNum-txNumLast))
            titleText+=']'
            self.subp.set_title(titleText)

        for mote in sample.getMotesIP():
            self.motesPlot[mote].set_data(self.motesData[mote][0],self.motesData[mote][1])
        self.subp.set_xlim(0,time)
        self.fig.canvas.draw()
        self.lastSample=sample
