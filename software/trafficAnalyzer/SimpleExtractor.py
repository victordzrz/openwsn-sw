class SimpleExtractor:
    def __init__(self):
        self.x=0

    def extractX(self,sample,lastSample):
        return self.x

    def extractY(self,sample,lastSample):
        self.x+=1
        return {'test':self.x*self.x,'test2':self.x*2,'test3':1/float(self.x)}
