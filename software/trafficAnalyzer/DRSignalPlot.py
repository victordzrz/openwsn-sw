import matplotlib.pyplot as plt

class DRSignalPlot:

    def __init__(self):
        self.fig,(self.subRSSI,self.subLQI)=plt.subplots(2,sharex=True)
        self.subRSSI.set_xlim(0.6,1.1)
        self.subRSSI.set_ylim(-100,0)
        self.subRSSI.set_title("RSSI")
        self.subRSSI.set_xlim(0.6,1.1)
        self.subLQI.set_ylim(40,120)
        self.subLQI.set_title("LQI")
        self.motesPlotRSSI=None
        self.motesPlotLQI=None
        self.subRSSI.set_ylabel("-dBm")
        self.subRSSI.grid()
        self.subLQI.grid()
        self.maxRSSI=-40
        self.minRSSI=-40
        self.maxLQI=240
        self.minLQI=240
        self.lastSample=None
        self.motesData=None
        self.moteColor=None
        self.colors=None
        plt.ion()
        plt.show()

    def plot(self,sample):
        if self.motesPlotRSSI==None:
            frame=0
            self.startFrame=sample.getTotalSum()[0][0]
            self.motesPlotRSSI=dict()
            self.motesPlotLQI=dict()
            self.motesData=dict()
            self.colors=dict()
            c=['b', 'g', 'r', 'm', 'y']
            cCounter=0
            for mote in sample.getMotesIP():
                self.motesPlotRSSI[mote]=self.subRSSI.scatter([],[])
                self.motesPlotRSSI[mote].set_label(mote)
                self.motesPlotLQI[mote]=self.subLQI.scatter([],[])
                self.motesPlotLQI[mote].set_label(mote)
                self.motesData[mote]=([],[],[])
                self.colors[mote]=c[cCounter]
                cCounter+=1
            self.subRSSI.legend(loc=2,fontsize=8)
            self.subLQI.legend(loc=2,fontsize=8)
        else:
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
                txNum,ackNum=sample.getDataByMote(mote)[0]
                txNumLast,ackNumLast=self.lastSample.getDataByMote(mote)[0]
                dr=float(ackNum-ackNumLast)/float(txNum-txNumLast)
                self.motesData[mote][0].append(dr)
                self.motesData[mote][1].append(rssi)
                self.motesData[mote][2].append(lqi)
                self.subRSSI.scatter(dr,rssi,marker='x',color=self.colors[mote])
                self.subLQI.scatter(dr,lqi,marker='x',color=self.colors[mote])
                #self.motesPlotRSSI[mote].set_data(self.motesData[mote][0],self.motesData[mote][1])
                #self.motesPlotLQI[mote].set_data(self.motesData[mote][0],self.motesData[mote][2])
            self.subLQI.set_ylim(self.minLQI-3,self.maxLQI+3)
            self.subRSSI.set_ylim(self.minRSSI-3,self.maxRSSI+3)
            self.fig.canvas.draw()
        self.lastSample=sample
