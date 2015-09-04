import time

class Sample:

    def __init__(self,moteIp):
        self.timeStamp=time.time()
        self.moteIp=moteIp
        self.moteData=dict()

    def addReading(self,channel,txNum,ackNum,rssi,lqi):
        self.moteData[channel]=(txNum,ackNum,rssi,lqi)

    def getMoteIP(self):
        return self.moteIp

    def getChannelList(self):
        return self.moteData.keys()

    def getDataByChannel(self,channel):
        return self.moteData[channel]

    def getData(self):
        return self.moteData

    def getChannelDeliveryRate(self,channel):
        return self.moteData[channel][1]/float(self.moteData[channel][0])

    def getMoteDeliveryRate(self):
        txSum=0
        ackSum=0
        for data in self.moteData.values():
            txSum+=data[0]
            ackSum+=data[1]
        return float(ackSum)/float(txSum)


    def getTime(self):
        return self.timeStamp

    def __str__(self):
        return str(self.timeStamp)+':'+str(self.moteData)
