from config import *
from coor.HeightCoordinate import *


class VivaldiNCClient:
    def __init__(self, _using_h = VIVALDI_USING_HEIGHT):
        self.using_height = _using_h
        if(self.using_height):
            self.coor = HeightCoordinate()
        else:
            self.coor = EuclideanCoordinate()
        self.ip = "127.0.0.1" 
        self.error = VIVALDI_ERROR
        
    def set(self,ip,coor,error):
        self.ip = ip
        self.coor = coor.getCoor()
        self.error = error
        
    def update(self, client, rtt):
        dist_predict = self.coor.getDistance(client.coor)
        weight = self.error / (self.error + client.error)
        error_calc = abs(dist_predict - rtt) / rtt
        self.error = error_calc * VIVALDI_CE * weight + self.error * (1 - VIVALDI_CE * weight)
        if (self.error > VIVALDI_ERROR):
            self.error = VIVALDI_ERROR
        delta = VIVALDI_CC * weight
        self.coor = self.coor + delta * (rtt - dist_predict) * self.coor.getDirection(client.coor)
        
    def getIP(self):
        return self.ip
    
    def getError(self):
        return self.error
    
    def getCoor(self):
        return self.coor.getCoor()
    
    def getPrintCoor(self):
        if(self.using_height):
            return [self.coor.vec, self.coor.height]
        else:
            return self.coor.vec
        
    def printInfo(self):
        str_ip = 'ip = ' + str(self.getIP())
        str_coor = 'coor = ' + str(self.getPrintCoor())
        str_error = 'error = ' + str(self.getError())
        print str_ip + ', ' + str_coor + ', ' + str_error

        
        