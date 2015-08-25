import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.plotList=list()

    def addPlot(self,plot):
        self.plotList.append(plot)

    def plotSample(self,sample):
        for plot in self.plotList:
            plot.plot(sample)
