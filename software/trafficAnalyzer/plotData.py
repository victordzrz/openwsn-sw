import pickle
import matplotlib.pyplot as plt


# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.

def cumulativeDeliveryRate(data):
    plt.figure(figsize=(12, 9))
    plt.title("Cumulative Delivery Rate by Node")
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    t=range(0,300,5)
    slotData=dict()
    for (ip,slot) in data.keys():
        if slot not in slotData.keys():
            slotData[slot]=list();
        slotData[slot]

        for i in range(0,len(data[ip][data[ip].keys()[0]])):
            totalMote.append((data[ip][keys()[0]][i][0]+data[ip][keys()[1]][i][0],
            data[ip][keys()[0]][i][1]+data[ip][keys()[1]][i][1]))
        edr=[e[1]/e[0] for e in totalMote]
        plt.plot(t,edr,label=ip)
    plt.legend(loc='upper right')
    plt.show()

def packetLoss(data):
    plt.figure(figsize=(12, 9))
    plt.title("Packet Loss")
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    cellData=dict()
    for ip in data.keys():
        for e in data[ip]:
            cellData[e[0][0]]=list()
            cellData[e[1][0]]=list()

    t=range(0,300,5)
    for ip in data.keys():
        tx=[e[0][1]+e[1][1] for e in data[ip]]
        ack=[e[0][2]+e[1][2] for e in data[ip]]
        edr=[(float(e[0][2]+e[1][2]))/float((e[0][1]+e[1][1])) for e in data[ip]]
        plt.plot(t,edr,label=ip)
    plt.legend(loc='upper right')
    plt.show()

def printRawData(data):
    print "===================================================="
    print "RAW"
    print 'x',
    for key in data.keys():
        print str(key[1])+"TX"+str(key[0]),str(key[1])+"ACK"+str(key[0]),
    print ''
    for i in range(0,len(data.items()[0][1])):
        print(i),
        for key in data.keys():
            print data[key][i][0],data[key][i][1],
        print ''

def printCumulativeDeliveryRate(data):
    print "===================================================="
    print "Cumulative Delivery Rate"
    print 'x',
    for key in data.keys():
        print key[1],
    print ''
    for i in range(0,len(data.items()[0][1])):
        print(i),
        for key in data.keys():
            print float(data[key][i][1])/float(data[key][i][0]),
        print ''

def printPacketLoss(data):
    print "===================================================="
    print "Packet Loss"
    print 'x',
    for key in data.keys():
        print key[1],
    print ''
    for i in range(0,len(data.items()[0][1])):
        print(i),
        for key in data.keys():
            if i==0:
                print data[key][i][0]-data[key][i][1],
            else:
                print (data[key][i][0]-data[key][i-1][0])-(data[key][i][1]-data[key][i-1][1]),
        print ''

def printDeliveryRate(data):
    print "===================================================="
    print "Delivery Rate"
    print 'x',
    for key in data.keys():
        print key[1],
    print ''
    for i in range(0,len(data.items()[0][1])):
        print(i),
        for key in data.keys():
            if i==0:
                print float(data[key][i][1])/float(data[key][i][0]),
            else:
                print float(data[key][i][1]-data[key][i-1][1])/float(data[key][i][0]-data[key][i-1][0]),
        print ''

def main():
    file= open('150820093429-data.json','r')
    data=pickle.load(file)
    printRawData(data)
    printCumulativeDeliveryRate(data)
    printDeliveryRate(data)
    printPacketLoss(data)
    file.close()

if __name__ == "__main__":
    main()
