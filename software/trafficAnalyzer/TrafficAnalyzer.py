from coap import coap
import pickle
import time
from Plotter import Plotter
from DRPlot import DRPlot
from MotesPlot import MotesPlot
from Sample import Sample

MOTE_PREFIX='bbbb::0012:4b00:060d:'
NUM_CELLS=2
SECOND_SAMPLE=2
NUM_SAMPLES=60


def main():
    connection,ipList=setUp()
    sampleList=list()
    plotter=Plotter()
    plotter.addPlot(DRPlot())
    plotter.addPlot(MotesPlot())
    for i in range(0,NUM_SAMPLES):
        sample=getSample(connection,ipList)
        print '.'
        if sample != None:
            sampleList.append(sample)
            plotter.plotSample(sample)
        else:
            connection=resetConnection(connection)
        time.sleep(SECOND_SAMPLE)
    connection.close()
    raw_input("Press any key to continue...")
    file = open('./data/'+time.strftime("%y%m%d%H%M%S")+'-data.pk','w+')
    pickle.dump(sampleList,file)
    file.close()

def setUp():
    connection=coap.coap(udpPort=5683)
    ipList=[]
    print("Enter the 4 last numbers of the IPs of the nodes to analyze or press ENTER to continue:")
    ip=raw_input(MOTE_PREFIX)
    while(ip!=''):
        ipList.append(ip)
        ip=raw_input(MOTE_PREFIX)

    putCells=raw_input("Add TX cells?[Y/n]")
    if(putCells=="Y" or putCells==""):
        for ip in ipList:
          addCells(connection,ip)
        time.sleep(1)
    return connection,ipList

def resetConnection(connection):
    connection.close()
    del connection
    return coap.coap(udpPort=5683)

def addCells(connection,ip):
    for i in range(0,NUM_CELLS):
        ok='n'
        while(ok=='n'):
            p=connection.PUT('coap://[{0}{1}]/6t'.format(MOTE_PREFIX,ip),)
            time.sleep(1)
            ok=raw_input("OK?")

def getSample(connection,ips):
    s=Sample()
    for ip in ips:
        data=getTrafficData(connection,ip)
        if data == None:
            return None
        for e in data:
            s.addReading(ip,e[0],e[1],e[2])
    return s

def getTrafficData(connection,ip):
    try:
        response=connection.GET('coap://[{0}{1}]/6t'.format(MOTE_PREFIX,ip),)
    except:
        print "Error, skipping data"
        return None
    stringResponse=''.join([chr(b) for b in response])
    lines=stringResponse.split('\n');
    dataTraffic=list()
    for line in lines:
        if len(line) > 5:
            slotSplit=line.split(':')
            slot=int(slotSplit[0],16)
            dataSplit=slotSplit[1].split('/')
            numTx=int(dataSplit[0],16)
            numAck=int(dataSplit[1],16)
            dataTraffic.append((slot,numTx,numAck))
    return dataTraffic

if __name__ == "__main__":
    main()
