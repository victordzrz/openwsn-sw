class DictLineExtractor:
    def __init__(self,xlabel='X',ylabel='Y'):
        self.x=0
        self.xlabel=xlabel
        self.ylabel=ylabel

    def getXLabel(self):
        return self.xlabel

    def getYLabel(self):
        return self.ylabel

    def extractX(self,sample):
        return self.x

    def extractY(self,sample):
        result=dict()
        for reading in sample.keys():
            result[reading]=sample[reading][self.x]
        self.x+=1
        return result
