from neighbor.NeighborManagerIF import *
from VivaldiNeighbor import *




class VivaldiNeighborManager(NeighborManagerIF):
    def __init__(self, _using_h = VIVALDI_USING_HEIGHT, _dim = DIMENTION, _strategy = VIVALDI_UPDATE_STRATEGY):
        self.update_strategy = _strategy
        self.using_height = _using_h
        self.dim = _dim
        self.neighborList = []
        self.updateCount = -1
        self.updateList = []
        
    def getLength(self):
        return len(self.neighborList)
    
    def addIP(self, ip):
        tmp = VivaldiNeighbor(self.using_height, self.dim)
        tmp.setIP(ip)
        tmp.setError(VIVALDI_ERROR_UNCONNECTED)
        if(self.getLength() == 0):
            self.neighborList.append(tmp)
            return
        for i in xrange(self.getLength()):
            if(self.neighborList[i].getIP() == ip):
                return
        self.neighborList.append(tmp)
        self.updateCount=-1

    def addClient(self, client):
        tmp = VivaldiNeighbor(self.using_height, self.dim)
        tmp.setClient(client)
        if(self.getLength() == 0):
            self.neighborList.append(tmp)
            return
        for i in xrange(self.getLength()):
            if(tmp.getIP() == self.neighborList[i].getIP()):
                if(tmp.getError() < self.neighborList[i].getError()):
                    self.neighborList[i].setClient(client)
                return
        self.neighborList.append(tmp)
        self.updateCount=-1
    
    '''
    this method is add by wgd, get the neighbor according to the ip, if fails, return None
    @Dec 5, 2009
    '''
    def getNeighbor(self, ip):
        for nb in self.neighborList:
            if( nb.getIP() == ip ):
                return nb
        return None
    
    def update(self, neighbor):
        for i in xrange(self.getLength()):
            if(neighbor.getIP() == self.neighborList[i].getIP()):
                self.neighborList[i].update(neighbor.client.coor.getCoor(), neighbor.getError(), neighbor.getRTT())
                
    def removeIP(self, ip):
        for i in xrange(self.getLength()):
            if(self.neighborList[i].getIP() == ip):
                self.neighborList.remove(self.neighborList[i])
                return True
        return False
                
    def printNeighbor(self, i):
        self.neighborList[i].printInfo()
    
    def printNeighborList(self):
        for i in xrange(self.getLength()):
            self.printNeighbor(i)
            
    def randomNC(self):
        if(self.getLength() == 0):
            self.updateCount = -1
            return
        if(self.updateCount == -1 or self.updateCount == VIVALDI_SELECTED_NEIGHBOR_NUM - 1 or self.updateCount == self.getLength() - 1):
            self.updateList = random.sample(range(0, self.getLength()), min(VIVALDI_SELECTED_NEIGHBOR_NUM, self.getLength()))
            self.updateCount = 0
        else:
            self.updateCount = self.updateCount + 1

    def closestNC(self):
        if(self.getLength() == 0):
            self.updateCount = -1
            return
        if(self.updateCount == -1 or self.updateCount == VIVALDI_SELECTED_NEIGHBOR_NUM - 1 or self.updateCount == self.getLength() - 1):
            if(self.getLength() <= VIVALDI_SELECTED_NEIGHBOR_NUM):
                self.updateList = range(self.getLength())
                self.updateCount = 0
                return
            tmpList = []
            self.updateList = []
            for i in xrange(self.getLength()):
                if(len(tmpList) == 0):
                    tmpList.append(i)
                else:
                    if(self.neighborList[i].getRTT == []):
                        tmpList.append(i)
                    else:
                        for j in xrange(i):
                            if(self.neighborList[j].getRTT() == []):
                                tmpList.insert(j, i)
                                break
                            if(self.neighborList[i].getRTT() < self.neighborList[tmpList[j]].getRTT()):
                                tmpList.insert(j, i)
                                break
                        if (j == i-1):
                            tmpList.append(i)
            for i in xrange(VIVALDI_SELECTED_NEIGHBOR_NUM):
                self.updateList.append(tmpList[i])
            self.updateCount = 0
        else:
            self.updateCount = self.updateCount + 1
        
    def hybridNC(self):
        if(self.getLength() == 0):
                self.updateCount = -1
                return
        if(self.updateCount == -1 or self.updateCount == VIVALDI_SELECTED_NEIGHBOR_NUM - 1 or self.updateCount == self.getLength() - 1):
            if(self.getLength() <= VIVALDI_SELECTED_NEIGHBOR_NUM):
                self.updateList = range(self.getLength())
                self.updateCount = 0
                return
            tmpList = []
            self.updateList = []
            for i in xrange(self.getLength()):
                if(len(tmpList) == 0):
                    tmpList.append(i)
                else:
                    if(self.neighborList[i].getRTT == []):
                        tmpList.append(i)
                    else:
                        for j in xrange(i):
                            if(self.neighborList[j].getRTT() == []):
                                tmpList.insert(j, i)
                                break
                            if(self.neighborList[i].getRTT() < self.neighborList[tmpList[j]].getRTT()):
                                tmpList.insert(j, i)
                                break
                        if (j == i-1):
                            tmpList.append(i)
            for i in xrange(VIVALDI_SELECTED_NEIGHBOR_NUM/2):
                self.updateList.append(tmpList[i])
            for i in xrange(VIVALDI_SELECTED_NEIGHBOR_NUM / 2):
                self.updateList.append(tmpList[i])
            self.updateCount = 0
        else:
            self.updateCount = self.updateCount + 1
        
    def selectIP(self):
        if (self.update_strategy == 0):
            self.randomNC()
        elif (self.update_strategy == 1):
            self.closestNC()
        elif (self.update_strategy == 2):
            self.hybridNC()
        tmp = self.updateList[self.updateCount]
        return self.neighborList[tmp].getIP()
      
    def upload(self):
        if(self.getLength() < VIVALDI_UPLOAD_NUM):
            return range(self.getLength())
        tmp = random.sample(range(self.getLength()), VIVALDI_UPLOAD_NUM)
        return tmp
