
class MoteFilter:

    def __init__(self,moteIP):
        self.moteIP=moteIP

    def accept(self,sample):
        return sample.getMoteIP().split(':')[-1]==self.moteIP.split(':')[-1]

    def __str__(self):
        return str(self.moteIP)
