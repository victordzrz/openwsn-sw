import matplotlib.pyplot as plt


class SignalPlot:

    def __init__(self):
        self.fig,(self.subRSSI,self.subLQI)=plt.subplots(2,sharex=True)
        self.subRSSI.set_xlim(0,300)
        self.subRSSI.set_ylim(-100,0)
        self.subRSSI.set_title("RSSI")
        self.subLQI.set_xlim(0,300)
        self.subLQI.set_ylim(40,120)
        self.subLQI.set_title("LQI")
        self.motesPlotRSSI=None
        self.subRSSI.set_ylabel("-dBm")
        plt.xlabel("Time (s)")
        plt.suptitle("Signal Quality")
        self.subRSSI.grid()
        self.subLQI.grid()
        self.maxRSSI=-40
        self.minRSSI=-40
        self.maxLQI=100
        self.minLQI=100
        self.lastSample=None
        self.startTime=None
        self.motesData=None
        plt.ion()
        plt.show()

    def plot(self,sample):
        if self.motesPlotRSSI==None:
            time=0
            self.startTime=sample.getTime()
            self.motesPlotRSSI=dict()
            self.motesPlotLQI=dict()
            self.motesData=dict()
            for mote in sample.getMotesIP():
                self.motesPlotRSSI[mote],=self.subRSSI.plot([],[])
                self.motesPlotRSSI[mote].set_label(mote)
                self.motesPlotLQI[mote],=self.subLQI.plot([],[])
                self.motesPlotLQI[mote].set_label(mote)
                self.motesData[mote]=([],[],[])
            self.subRSSI.legend(loc=2,fontsize=8)
            self.subLQI.legend(loc=2,fontsize=8)
        for mote in sample.getMotesIP():
            (rssi,lqi)=sample.getDataByMote(mote)[1]
            if(rssi>self.maxRSSI):
                self.maxRSSI=rssi
            elif rssi<self.minRSSI:
                self.minRSSI=rssi
            if(lqi>self.maxLQI):
                self.maxLQI=lqi
            elif lqi<self.minLQI:
                self.minLQI=lqi
            time=sample.getTime()-self.startTime
            self.motesData[mote][0].append(time)
            self.motesData[mote][1].append(rssi)
            self.motesData[mote][2].append(lqi)
            self.motesPlotRSSI[mote].set_data(self.motesData[mote][0],self.motesData[mote][1])
            self.motesPlotLQI[mote].set_data(self.motesData[mote][0],self.motesData[mote][2])
        self.subRSSI.set_xlim(0,time)
        self.subLQI.set_xlim(0,time)
        self.subLQI.set_ylim(self.minLQI-5,self.maxLQI+5)
        self.subRSSI.set_ylim(self.minRSSI-10,self.maxRSSI+10)
        self.fig.canvas.draw()
