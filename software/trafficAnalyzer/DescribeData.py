import pickle
import time
import sys
import scipy.stats as stats
from Sample import Sample
from DictLineExtractor import DictLineExtractor
from LinePlot import LinePlot
from Plotter import Plotter
import matplotlib.pyplot as plt

readingDesc=['+25m','25m','15m','5m','2.5m(B)','3m']

def main():
    fileFiles=open('files.txt','r')
    dataList=list()
    plotterList=list()
    for line in fileFiles:
        file = open(line[:-1],'r')
        data=pickle.load(file)
        dataList.append(data)
        file.close()
    dataByReading=getDRAverageByReading(dataList)
    print 'Average Delivery Rate by Reading'
    getReadingAverages(dataByReading)
    plotter=Plotter()
    plotter.addPlot(LinePlot(DictLineExtractor('Channel','Delivery Rate')),name='Average Delivery Rate by Reading')
    for i in range(0,16):
        plotter.plotSample(dataByReading)
    plotterList.append(plotter)


    dataByReading=getDRAverageByReadingWithMoteExclusion(dataList,'bbbb::12:4b00:60d:85de')
    print "Average Delivery Rate with External Mote"
    getReadingAverages(dataByReading)
    plotter=Plotter()
    plotter.addPlot(LinePlot(DictLineExtractor('Channel','Delivery Rate')),name="Average Delivery Rate with External Mote")
    for i in range(0,16):
        plotter.plotSample(dataByReading)
    plotterList.append(plotter)

    dataByReading=getRSSIAverageByReadingWithMoteExclusion(dataList,'bbbb::12:4b00:60d:85de')
    print "Average RSSI with External Mote"
    getReadingAverages(dataByReading)
    plotter=Plotter()
    plotter.addPlot(LinePlot(DictLineExtractor('Channel','RSSI')),name="Average RSSI with External Mote")
    for i in range(0,16):
        plotter.plotSample(dataByReading)
    plotterList.append(plotter)

    dataByReading=getRSSIAverageByReading(dataList)
    print 'Average RSSI by Reading'
    getReadingAverages(dataByReading)
    plotter=Plotter()
    plotter.addPlot(LinePlot(DictLineExtractor('Channel','RSSI')),name='Average RSSI by Reading')
    for i in range(0,16):
        plotter.plotSample(dataByReading)
    plotterList.append(plotter)


    dataByReading=getLQIAverageByReadingWithMoteExclusion(dataList,'bbbb::12:4b00:60d:85de')
    print "Average LQI with External Mote"
    getReadingAverages(dataByReading)
    plotter=Plotter()
    plotter.addPlot(LinePlot(DictLineExtractor('Channel','LQI')),name="Average LQI with External Mote")
    for i in range(0,16):
        plotter.plotSample(dataByReading)
    plotterList.append(plotter)

    dataByReading=getLQIAverageByReading(dataList)
    print 'Average LQI by Reading'
    getReadingAverages(dataByReading)
    plotter=Plotter()
    plotter.addPlot(LinePlot(DictLineExtractor('Channel','LQI')),name='Average LQI by Reading')
    for i in range(0,16):
        plotter.plotSample(dataByReading)
    plotterList.append(plotter)


    saveData=raw_input("Save graphs?[Y/n]")
    if saveData!='N' or saveData!='n':
        for plotter in plotterList:
            plotter.save()

def getReadingAverages(readingData):
    averages=dict()
    for reading in sorted(readingData.keys()):
        data=readingData[reading]
        dataAverage=sum(data)/float(len(data))
        averages[reading]=dataAverage
        print reading,': ',dataAverage
    return averages


def getIPs(data):
    result=set()
    for i in data:
        result.add(i.getMoteIP())
    return list(result)

def getRSSIAverageByReading(dataList):
    dataByReading=dict()
    counter=0
    for data in dataList:
        channelData=list()
        for i in range(0,16):
            channelData.append(0)
        ipList=getIPs(data)
        RSSImeans=getRSSIAverageByMote(data)
        for ip in ipList:
            for channel in range(0,16):
                channelData[channel]+=RSSImeans[ip][channel]
        for channel in range(0,16):
            channelData[channel]/=float(len(ipList))
        dataByReading['R'+str(counter)+' ('+readingDesc[counter]+')']=channelData
        counter+=1
    return dataByReading

def getRSSIAverageByReadingWithMoteExclusion(dataList,moteIP):
    dataByReading=dict()
    counter=0
    for data in dataList:
        channelData=list()
        sampleNumber=list()
        for i in range(0,16):
            channelData.append(0)
            sampleNumber.append(0)
        ipList=getIPs(data)
        RSSImeans=getRSSIAverageByMote(data)
        for ip in ipList:
            if ip!=moteIP:
                for channel in range(0,16):
                    channelData[channel]+=RSSImeans[ip][channel]
                    sampleNumber[channel]+=1
            else:
                dataByReading['R'+str(counter)+' ('+readingDesc[counter]+' Ex.)']=RSSImeans[ip]
        for channel in range(0,16):
            channelData[channel]/=float(sampleNumber[channel])
        dataByReading['R'+str(counter)+' ('+readingDesc[counter]+')']=channelData
        counter+=1
    return dataByReading

def getLQIAverageByReading(dataList):
    dataByReading=dict()
    counter=0
    for data in dataList:
        channelData=list()
        for i in range(0,16):
            channelData.append(0)
        ipList=getIPs(data)
        LQImeans=getLQIAverageByMote(data)
        for ip in ipList:
            for channel in range(0,16):
                channelData[channel]+=LQImeans[ip][channel]
        for channel in range(0,16):
            channelData[channel]/=float(len(ipList))
        dataByReading['R'+str(counter)+' ('+readingDesc[counter]+')']=channelData
        counter+=1
    return dataByReading

def getLQIAverageByReadingWithMoteExclusion(dataList,moteIP):
    dataByReading=dict()
    counter=0
    for data in dataList:
        channelData=list()
        sampleNumber=list()
        for i in range(0,16):
            channelData.append(0)
            sampleNumber.append(0)
        ipList=getIPs(data)
        LQImeans=getLQIAverageByMote(data)
        for ip in ipList:
            if ip!=moteIP:
                for channel in range(0,16):
                    channelData[channel]+=LQImeans[ip][channel]
                    sampleNumber[channel]+=1
            else:
                dataByReading['R'+str(counter)+' ('+readingDesc[counter]+' Ex.)']=LQImeans[ip]
        for channel in range(0,16):
            channelData[channel]/=float(sampleNumber[channel])
        dataByReading['R'+str(counter)+' ('+readingDesc[counter]+')']=channelData
        counter+=1
    return dataByReading

def getDRAverageByReading(dataList):
    dataByReading=dict()
    counter=0
    for data in dataList:
        channelData=list()
        for i in range(0,16):
            channelData.append(0)
        ipList=getIPs(data)
        DRmeans=getDRAverageByMote(data)
        for ip in ipList:
            for channel in range(0,16):
                channelData[channel]+=DRmeans[ip][channel]
        for channel in range(0,16):
            channelData[channel]/=float(len(ipList))
        dataByReading['R'+str(counter)+' ('+readingDesc[counter]+')']=channelData
        counter+=1
    return dataByReading

def getDRAverageByReadingWithMoteExclusion(dataList,moteIP):
    dataByReading=dict()
    counter=0
    for data in dataList:
        channelData=list()
        sampleNumber=list()
        for i in range(0,16):
            channelData.append(0)
            sampleNumber.append(0)
        ipList=getIPs(data)
        DRmeans=getDRAverageByMote(data)
        for ip in ipList:
            if ip!=moteIP:
                for channel in range(0,16):
                    channelData[channel]+=DRmeans[ip][channel]
                    sampleNumber[channel]+=1
            else:
                dataByReading['R'+str(counter)+' ('+readingDesc[counter]+' Ex.)']=DRmeans[ip]
        for channel in range(0,16):
            channelData[channel]/=float(sampleNumber[channel])
        dataByReading['R'+str(counter)+' ('+readingDesc[counter]+')']=channelData
        counter+=1

    return dataByReading

def getDRAverageByMote(data):
    result=dict()
    lastData=dict()
    for sample in data:
        ip=sample.getMoteIP()
        if ip not in result.keys():
            result[ip]=list()
            lastData[ip]=list()
            for i in range(0,16):
                result[ip].append(list())
                lastData[ip].append(None)
        for channel in sample.getChannelList():
            tx,ack=sample.getDataByChannel(channel)[0:2]
            lastData[ip][channel]=(tx,ack)
    for ip in result.keys():
        for channel in range(0,16):
            tx,ack=lastData[ip][channel]
            result[ip][channel]=ack/float(tx)
    return result

def getRSSIAverageByMote(data):
    sum=dict()
    count=dict()
    #Calculate RSSI sum per channel
    for sample in data:
        ip=sample.getMoteIP()
        if ip not in sum.keys():
            count[ip]=list()
            sum[ip]=list()
            for i in range(0,16):
                sum[ip].append(0)
                count[ip].append(0)
        for channel in sample.getChannelList():
            rssi=sample.getDataByChannel(channel)[2]
            sum[ip][channel]+=rssi
            count[ip][channel]+=1
    #Divide RSSI by number of samples in each channel
    for ip in count.keys():
        for i in range(0,16):
            sum[ip][i]/=count[ip][i]
    return sum

def getLQIAverageByMote(data):
    sum=dict()
    count=dict()
    #Calculate LQI sum per channel
    for sample in data:
        ip=sample.getMoteIP()
        if ip not in sum.keys():
            count[ip]=list()
            sum[ip]=list()
            for i in range(0,16):
                sum[ip].append(0)
                count[ip].append(0)
        for channel in sample.getChannelList():
            lqi=sample.getDataByChannel(channel)[3]
            sum[ip][channel]+=lqi
            count[ip][channel]+=1
    #Divide LQI by number of samples in each channel
    for ip in count.keys():
        for i in range(0,16):
            sum[ip][i]/=count[ip][i]
    return sum

def getDRData(data):
    result=dict()
    lastData=dict()
    for sample in data:
        ip=sample.getMoteIP()
        if ip not in result.keys():
            result[ip]=list()
            lastData[ip]=list()
            for i in range(0,16):
                result[ip].append(list())
                lastData[ip].append(None)
        for channel in sample.getChannelList():
            tx,ack=sample.getDataByChannel(channel)[0:2]
            if lastData[ip][channel]==None:
                result[ip][channel].append(ack/float(tx))
                lastData[ip][channel]=(tx,ack)
            else:
                lastTx,lastAck=lastData[ip][channel]
                result[ip][channel].append((ack-lastAck)/float(tx-lastTx))
                lastData[ip][channel]=(tx,ack)
    return result

def getRSSIData(data):
    result=dict()
    for sample in data:
        ip=sample.getMoteIP()
        if ip not in result.keys():
            result[ip]=list()
            for i in range(0,16):
                result[ip].append(list())
        for channel in sample.getChannelList():
            rssi=sample.getDataByChannel(channel)[2]
            result[ip][channel].append(rssi)
    return result

def getLQIDict():
    result=dict()
    for sample in data:
        ip=sample.getMoteIP()
        if ip not in result.keys():
            result[ip]=list()
            for i in range(0,16):
                result[ip].append(list())
        for channel in sample.getChannelList():
            lqi=sample.getDataByChannel(channel)[3]
            result[ip][channel].append(lqi)
    return result




if __name__ == "__main__":
    main()
