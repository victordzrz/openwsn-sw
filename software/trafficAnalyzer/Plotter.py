import matplotlib.pyplot as plt
import LinePlot as LinePlot
import multiprocessing



class Plotter:
    def __init__(self):
        self.plotList=list()

    def addPlot(self,plot,filter=None,name=None):
        if filter!=None:
            plot.setTitle(str(filter))
        if name!=None:
            plot.setTitle(str(name))
        self.plotList.append((plot,filter))

    def plotSample(self,sample):
        for plot,filter in self.plotList:
            if filter!=None:
                if filter.accept(sample):
                    plot.plot(sample)
            else:
                plot.plot(sample)
            plot.animate()

    def animate(self):
        for plot,filter in self.plotList:
            plot.animate()

    def show(self):
        for plot,filter in self.plotList:
            plot.show()

    def save(self):
        for plot,filter in self.plotList:
            plot.save()
