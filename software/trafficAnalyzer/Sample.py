import time

class Sample:

    def __init__(self):
        self.timeStamp=time.time()
        self.moteData=dict()

    def addReading(self,moteIP,slot,txNum,ackNum):
        self.moteData[(moteIP,slot)]=(txNum,ackNum)

    def getMotesIP(self):
        ips=set();
        for e in self.moteData.keys():
            ips.add(e[0])
        return ips

    def getSlotOffsets(self):
        slots=set();
        for e in self.moteData.keys():
            slots.add(e[1])
        return slots

    def getDataByMote(self,ip):
        txNum=0
        ackNum=0
        for e in self.moteData.keys():
            if e[0]==ip:
                txNum+=self.moteData[e][0]
                ackNum+=self.moteData[e][1]
        return (txNum,ackNum)

    def getDataBySlot(self,slot):
        txNum=0
        ackNum=0
        for e in self.moteData.keys():
            if e[1]==slot:
                txNum+=self.moteData[e][0]
                ackNum+=self.moteData[e][1]
        return (txNum,ackNum)

    def getData(self):
        return self.moteData


    def getSlotDeliveryRate(self,slot):
        txSum=0
        ackSum=0
        for e in self.moteData.keys():
            if e[1]==slot:
                txSum+=self.moteData[e][0]
                ackSum+=self.moteData[e][1]
        return float(ackSum)/float(txSum)

    def getMoteDeliveryRate(self,ip):
        txSum=0
        ackSum=0
        for e in self.moteData.keys():
            if e[0]==ip:
                txSum+=self.moteData[e][0]
                ackSum+=self.moteData[e][1]
        return float(ackSum)/float(txSum)

    def getDeliveryRate(self):
        txSum=0
        ackSum=0
        for e in self.moteData.values():
            txSum+=e[0]
            ackSum+=e[1]
        return float(ackSum)/float(txSum)

    def getTime(self):
        return self.timeStamp

    def getTotalSum(self):
        txSum=0
        ackSum=0
        for e in self.moteData.values():
            txSum+=e[0]
            ackSum+=e[1]
        return (txSum,ackSum)

    def __str__(self):
        return str(self.timeStamp)+':'+str(self.moteData)
