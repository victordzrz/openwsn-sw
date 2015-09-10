from coap import coap
import pickle
import time
from Plotter import Plotter
from DRSignalPlot import DRSignalPlot
from Sample import Sample
from DR3DExtractor import DR3DExtractor
from RSSI3DExtractor import RSSI3DExtractor
from LQI3DExtractor import LQI3DExtractor
from ThreeDPlot import ThreeDPlot
from LinePlot import LinePlot
from MoteFilter import MoteFilter
import socket
import struct

MOTE_PREFIX='bbbb::0012:4b00:060d:'
NUM_CELLS=2
NUM_SAMPLE=300



def main():
    ipList=setUp()
    sampleList=list()
    plotter=Plotter()
    for ip in ipList:
        plotter.addPlot(ThreeDPlot(RSSI3DExtractor()),MoteFilter(ip))
        plotter.addPlot(ThreeDPlot(LQI3DExtractor()),MoteFilter(ip))
        plotter.addPlot(ThreeDPlot(DR3DExtractor()),MoteFilter(ip))
    sampleList=startRecording(plotter,ipList)
    raw_input("Press any key to continue...")
    file = open('./data/'+time.strftime("%y%m%d%H%M%S")+'-data.pk','w+')
    pickle.dump(sampleList,file)
    writeCSV(sampleList)
    file.close()

def setUp():
    connection=coap.coap(udpPort=5683)
    ipList=[]
    print("Enter the IPs of the nodes to analyze or press ENTER to continue:")
    ip=raw_input()
    while(ip!=''):
        ipList.append(ip)
        ip=raw_input()
    putCells=raw_input("Add TX cells?[Y/n]")
    if(putCells=="Y" or putCells=="" or putCells=="y"):

        for ip in ipList:
          addCells(connection,ip)
        time.sleep(1)
    connection.close()
    return ipList
def resetConnection(connection):
    connection.close()
    del connection
    return coap.coap(udpPort=5683)

def addCells(connection,ip):
    for i in range(0,NUM_CELLS):
        ok='n'
        while(ok=='n' or ok=='N'):
            p=connection.PUT('coap://[{0}]/6t'.format(ip),)
            time.sleep(1)
            ok=raw_input("OK?")

def startRecording(plotter,ipList):
    switchMLog(ipList)
    soc=socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
    soc.bind(('',16792))
    b=bytearray(56)
    sampleList=list()
    for i in range(0,NUM_SAMPLE):
        size,addr=soc.recvfrom_into(b,56)
        result=struct.unpack('<'+'BHHbB'*8,str(b))
        #result = struct.unpack('<'+'b'*56,str(b))
        newSample=Sample(addr[0])
        for index in range(0,40,5):
            channel=result[index]
            tx=result[index+1]
            ack=result[index+2]
            rssi=result[index+3]
            lqi=result[index+4]
            #print addr[0].split(':')[-1],'C:'+str(channel),str(ack)+'/'+str(tx),'RSSI='+str(rssi),'LQI='+str(lqi)
            newSample.addReading(channel,tx,ack,rssi,lqi)
        plotter.plotSample(newSample)
        sampleList.append(newSample)
    switchMLog(ipList)
    return sampleList

def switchMLog(ipList):
    connection=coap.coap(udpPort=5683)
    for ip in ipList:
        connection.GET('coap://[{0}]/6t'.format(ip),)
    connection.close()

def writeCSV(sampleList):
    file = open('./data/'+time.strftime("%y%m%d%H%M%S")+'-data.csv','w+')

    for sample in sampleList:
        for channel in sample.getChannelList():
            line=''
            line+=str(sample.getTime())
            line+=','
            line+=str(sample.getMoteIP())
            line+=','
            line+=str(channel)
            line+=','
            data=sample.getDataByChannel(channel)
            line+=str(data[0])
            line+=','
            line+=str(data[1])
            line+=','
            line+=str(data[2])
            line+=','
            line+=str(data[3])
            line+='\n'

            file.write(line)

    file.close()



if __name__ == "__main__":
    main()
