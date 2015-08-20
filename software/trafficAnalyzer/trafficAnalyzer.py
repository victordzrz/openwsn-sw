from coap import coap
import time
import pickle

MOTE_PREFIX='bbbb::0012:4b00:060d:'
NUMBER_CELLS=2

def main():
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
        time.sleep(2)

    allNodeData=dict()
    for i in range(0,60):
        for ip in ipList:
            data = getTrafficData(connection,ip)
            for element in data:
                if (ip,element[0]) not in allNodeData.keys():
                    allNodeData[(ip,element[0])]=list()
                allNodeData[(ip,element[0])].append((element[1],element[2]))
                print '(',ip,',',element[0],'):',element[1],'/',element[2]
        time.sleep(5)
    connection.close()
    file = open(time.strftime("%y%m%d%H%M%S")+'-data.json','w+')
    pickle.dump(allNodeData,file)
    file.close()

def addCells(connection,ip):
    for i in range(0,NUMBER_CELLS):
        ok='n'
        while(ok=='n'):
            p=connection.PUT('coap://[{0}{1}]/6t'.format(MOTE_PREFIX,ip),)
            print p
            time.sleep(1)
            ok=raw_input("OK?")

def getTrafficData(connection,ip):
    try:
        response=connection.GET('coap://[{0}{1}]/6t'.format(MOTE_PREFIX,ip),)
    except:
        return [(0,0,0),(0,0,0)]
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
