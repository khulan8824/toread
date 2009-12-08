from neighbor.NeighborIF import *
from VivaldiNCClient import *
from VivaldiNeighbor import *


'''
this file seems useless, since pharos almost the same as vivaldi, we can use vivaldi neighbor 
'''


'''
class VivaldiNeighbor(NeighborIF):
    def __init__(self):
        self.client = VivaldiNCClient()
        self.rtt = []
    
    def updateRTT(self, rtt):
        if (len(self.rtt) < RTT_NUM):
            self.rtt.append(rtt)
        else:
            self.rtt.remove(max(self.rtt))
            self.rtt.append(rtt)
    
    def update(self, coor, err, rtt):
        self.client.coor = coor
        self.client.error_local = err
        self.updateRTT(rtt)
        
    def set(self, ip, coor, err, rtt):
        self.client.ip = ip
        self.client.coor = coor.getCoor()
        self.client.error_local = err
        self.updateRTT(rtt)
    
    def setClient(self, client):
        self.client.ip = client.ip
        self.client.coor = client.coor.getCoor()
        self.client.error_local = client.error_local
        
    
    def setNeighbor(self, neighbor):
        tmpCoor = neighbor.client.coor.getCoor()
        self.set(neighbor.getIP(), tmpCoor, neighbor.getError(), neighbor.getRTT())
        
    def getRTT(self):
        if(len(self.rtt) == 0):
            return []
        return min(self.rtt)

    def getRTT_last(self):
        return self.rtt[len(self.rtt)-1]

    def getError(self):
        return self.client.getError()
    
    def getPrintCoor(self):
        return self.client.getPrintCoor()
    
    def getIP(self):
        return self.client.getIP()
    
    def printInfo(self):
        str_ip = 'ip = ' + str(self.getIP())
        str_coor = 'coor = ' + str(self.getPrintCoor())
        str_error = 'error = ' + str(self.getError())
        str_rtt = 'rtt = ' + str(self.getRTT())
        print str_ip + ', ' + str_coor + ', ' + str_error + ', ' + str_rtt
        
'''



'''
a = VivaldiNeighbor()
ip = [192,1,1,1]
coor = [1,1,1,1]
err = 1.5
rtt = 60
a.set(ip, coor, err, rtt)
for i in xrange(15):
    rtt = random.uniform(1, 100)
    print 'rtt='+str(rtt)
    a.update(coor, err, rtt)

for i in xrange(10):
    print 'a.rtt = '+str(a.rtt[i])
    
print a.getRTT()
print a.getError()
'''