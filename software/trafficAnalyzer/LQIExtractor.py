class LQIExtractor:
    def __init__(self):
        self.startTime=None

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
            result[channel]=data[3]
        return result

    def getXLabel(self):
        return 'Time (s)'

    def getYLabel(self):
        return 'LQI'
