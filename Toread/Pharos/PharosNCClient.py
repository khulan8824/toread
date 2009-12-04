from config import *
from coor.HeightCoordinate import *

class PharosNCClient:
    def __init__(self):
        if(PHAROS_USING_HEIGHT_GLOBAL):
            self.coor_global = HeightCoordinate(zeros(DIMENTION), THRESHOLD_HEIGHT)
        else:
            self.coor_global = EuclideanCoordinate(zeros(DIMENTION))
        if(PHAROS_USING_HEIGHT_LOCAL):
            self.coor_local = HeightCoordinate(zeros(DIMENTION), THRESHOLD_HEIGHT)
        else:
            self.coor_local = EuclideanCoordinate(zeros(DIMENTION))            
        self.ip = "127.0.0.1" 
        self.error_global = PHAROS_GLOBAL_ERROR
        self.error_local = PHAROS_LOCAl_ERROR
        
    def set(self, ip, coor_global, error_global, coor_local, error_local):
        self.ip = ip
        self.coor_global = coor_global.getCoor()
        self.error_global = error_global
        self.coor_local = coor_local.getCoor()
        self.error_local = error_local
        
    def update(self, client, rtt):
        dist_predict = self.coor.getDistance(client.coor)
        weight = self.error_local / (self.error_local + client.error_local)
        error_calc = abs(dist_predict - rtt) / rtt
        self.error_local = error_calc * CE * weight + self.error_local * (1 - CE * weight)
        delta = CC * weight
        self.coor = self.coor + delta * (rtt - dist_predict) * self.coor.getDirection(client.coor)
        
    def getIP(self):
        return self.ip
    
    def getGlobalError(self):
        return self.error_global
    
    def getLocalError(self):
        return self.error_local

    def getGlobalCoor(self):
        return self.coor_global.getCoor()
    
    def getLocalCoor(self):
        return self.coor_local.getCoor()
    
    def getPrintCoor(self):
        if(PHAROS_USING_HEIGHT_GLOBAL):
            coor_global = [self.coor_global.vec, self.coor_global.height]
        else:
            coor_global = self.coor_global.vec
        if(PHAROS_USING_HEIGHT_LOCAL):
            coor_local = [self.coor_local.vec, self.coor_local.height]
        else:
            coor_local = self.coor_local.vec
        return [coor_global, coor_local]

    def printInfo(self):
        str_ip = 'ip = ' + str(self.getIP())
        str_coor = 'coor = ' + str(self.getPrintCoor())
        str_error_global = 'error_global = ' + str(self.getGlobalError())
        str_error_local = 'error_local = ' + str(self.getLocalError())
        print str_ip + ', ' + str_coor + ', ' + str_error_global + ', ' + str_error_local

        
        