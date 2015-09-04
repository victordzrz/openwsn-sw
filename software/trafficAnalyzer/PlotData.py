import pickle
import time
import sys
from Plotter import Plotter
from DRPlot import DRPlot
from MotesPlot import MotesPlot
from SignalPlot import SignalPlot
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


def main():
    if len(sys.argv)>1:
        file = open(sys.argv[1],'r')
        data=pickle.load(file)
        file.close()
        plotter=Plotter()
        #plotter.addPlot(LinePlot(DRExtractor(),buffered=True))
        #plotter.addPlot(LinePlot(LQIExtractor(),buffered=True))
        #plotter.addPlot(LinePlot(RSSIExtractor(),buffered=True))
        plotter.addPlot(ThreeDPlot(RSSI3DExtractor()))
        plotter.addPlot(ThreeDPlot(LQI3DExtractor()))
        plotter.addPlot(ThreeDPlot(DR3DExtractor()))
        for sample in data:
            plotter.plotSample(sample)
        plotter.show()
        raw_input("Press any key to continue")

    else:
        print "Usage: python PlotData.py [dataFile]"


if __name__ == "__main__":
    main()
