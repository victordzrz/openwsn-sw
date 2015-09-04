class DR3DExtractor:
    def __init__(self):
        self.startTime=None
        self.lastData=dict()
        self.savedData=[1]*16

    def extractX(self,sample):
        if self.startTime==None:
            self.startTime=sample.getTime()
            return 0
        else:
            return sample.getTime()-self.startTime

    def extractZ(self,sample):
        for channel in sample.getChannelList():
            data=sample.getDataByChannel(channel)
            if channel in self.lastData.keys():
                txNum=data[0]-self.lastData[channel][0]
                ackNum=data[1]-self.lastData[channel][1]
            else:
                txNum=data[0]
                ackNum=data[1]
            self.savedData[channel]=ackNum/float(txNum)
            self.lastData[channel]=(data[0],data[1])
        return list(self.savedData)

    def getXLabel(self):
        return 'Time (s)'

    def getYLabel(self):
        return 'Channel'

    def getZLabel(self):
        return 'Delivery Rate'
