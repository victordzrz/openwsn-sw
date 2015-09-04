class DRExtractor:
    def __init__(self):
        self.startTime=None
        self.lastData=dict()

    def extractX(self,sample):
        if self.startTime==None:
            self.startTime=sample.getTime()
            return 0
        else:
            return sample.getTime()-self.startTime

    def extractY(self,sample):
        result=dict()
        for channel in sample.getChannelList():
            data=sample.getDataByChannel(channel)
            if channel in self.lastData.keys():
                txNum=data[0]-self.lastData[channel][0]
                ackNum=data[1]-self.lastData[channel][1]
            else:
                txNum=data[0]
                ackNum=data[1]
            result[channel]=ackNum/float(txNum)
            self.lastData[channel]=(data[0],data[1])
        return result

    def getXLabel(self):
        return 'Time (s)'

    def getYLabel(self):
        return 'Delivery Rate'
