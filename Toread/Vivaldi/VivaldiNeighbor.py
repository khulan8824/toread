from neighbor.NeighborIF import *
from VivaldiNCClient import *

class VivaldiNeighbor(NeighborIF):
    def __init__(self, _using_h = VIVALDI_USING_HEIGHT):
        self.client = VivaldiNCClient( _using_h )
        self.rtt = []
    
    def updateRTT(self, rtt):
        if (len(self.rtt) < VIVALDI_RTT_NUM):
            self.rtt.append(rtt)
        else:
            self.rtt.remove(max(self.rtt))
            self.rtt.append(rtt)
    
    def update(self, coor, err, rtt):
        self.client.coor = coor.getCoor()
        self.client.error_local = err
        self.rtt = rtt  # modified by wgd, @Dec 5, 2009
        #self.updateRTT(rtt)
       
    def setIP(self, ip):
        self.client.ip = ip
        
    def setError(self, err):
        self.client.error = err
    
    def setCoor(self, coor):
        self.client.coor = coor.getCoor()
    
    def set(self, ip, coor, err, rtt):
        self.setIP(ip)
        self.setCoor(coor)
        self.setError(err)
        self.rtt = rtt # modified by wgd, @Dec 5, 2009
        #self.updateRTT(rtt)
    
    def setClient(self, client):
        self.setIP(client.ip)
        self.setCoor(client.coor)
        self.setError(client.getError())
        
    
    def setNeighbor(self, neighbor):
        tmpCoor = neighbor.client.coor.getCoor()
        self.set(neighbor.getIP(), tmpCoor, neighbor.getError(), neighbor.getRTT())
        
    def getRTT(self):
        return self.rtt  # modified by wgd, @Dec 5, 2009
        
        '''
        if(len(self.rtt) == 0):
            return []
        return min(self.rtt)
        '''
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
        