import pickle
import time
import sys
from Plotter import Plotter
from Sample import Sample
from DRSignalPlot import DRSignalPlot
from DRExtractor import DRExtractor
from LQIExtractor import LQIExtractor
from RSSIExtractor import RSSIExtractor
from DR3DExtractor import DR3DExtractor
from RSSI3DExtractor import RSSI3DExtractor
from LQI3DExtractor import LQI3DExtractor
from ThreeDPlot import ThreeDPlot
from LinePlot import LinePlot
from MoteFilter import MoteFilter


def main():
    if len(sys.argv)>1:
        file = open(sys.argv[1],'r')
        data=pickle.load(file)
        file.close()
        plotter=Plotter()
        ipList=set()
        for i in range(30):
            ipList.add(data[i].getMoteIP())
        plotter=Plotter()
        for ip in ipList:
            plotter.addPlot(ThreeDPlot(RSSI3DExtractor(),buffered=False,windowSize=15),MoteFilter(ip))
        for sample in data:
            plotter.plotSample(sample)
            for i in range(0,2):
                time.sleep(0.005)
                plotter.animate()
        plotter.show()
        raw_input("Press any key to continue")

    else:
        print "Usage: python PlotData.py [dataFile]"


if __name__ == "__main__":
    main()
