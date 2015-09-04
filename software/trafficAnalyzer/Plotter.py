import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):
        self.plotList=list()

    def addPlot(self,plot,filter=None):
        if filter!=None:
            plot.setTitle(str(filter))
        self.plotList.append((plot,filter))

    def plotSample(self,sample):
        for plot,filter in self.plotList:
            if filter!=None:
                if filter.accept(sample):
                    plot.plot(sample)
            else:
                plot.plot(sample)

    def show(self):
        for plot,filter in self.plotList:
            plot.show()
