class RSSI3DExtractor:
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
        result=list()
        for channel in sample.getChannelList():
            data=sample.getDataByChannel(channel)
            self.savedData[channel]=data[2]
        return list(self.savedData)

    def getXLabel(self):
        return 'Time (s)'

    def getYLabel(self):
        return 'Channel'

    def getZLabel(self):
        return 'RSSI (dB)'
