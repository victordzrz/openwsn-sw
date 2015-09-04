from SimpleExtractor import SimpleExtractor
from LinePlot import LinePlot

plot=LinePlot(SimpleExtractor())
for i in range(0,100):
    plot.plot(i)

raw_input()
