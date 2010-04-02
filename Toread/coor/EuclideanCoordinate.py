from CoordinateIF import *

def zeros(d):
    vec = []
    for i in xrange(d):
        vec.append(0.0)
    return vec

class EuclideanCoordinate(CoordinateIF):
    dim = -1

    def __init__(self, arg_dimension = DIMENTION):
        self.dim = arg_dimension
        self.setCoor(zeros(self.dim))
    
    def setCoor(self, vec):
        if (len(vec) == self.dim):
            self.vec = vec[:]
        else:
            print "[ EuclideanCoordinate Fatal Error] Different dimensions error in SetCoor !"
            print "[ EuclideanCoordinate Fatal Error] Argument vector dimension:",len(vec),"    EuclideanCoordinate.dimension:",self.dim
            self.vec = []
            for i in xrange(self.dim):
                 self.vec.append(0.0)
                 
    def getCoor(self):
        tmpCoor = EuclideanCoordinate(self.dim)
        tmpCoor.setCoor(self.vec)
        return tmpCoor
                 
    def printCoor(self):
        print 'Coordinate:'+str(self.vec)   #maybe write in log file

    def __add__(self, coor):
        if (len(coor.vec) == self.dim):
            tmpVec = []
            for i in xrange(self.dim):
                tmpVec.append(self.vec[i] + coor.vec[i])
            tmpCoor = EuclideanCoordinate(self.dim)
            tmpCoor.setCoor(tmpVec)
            return tmpCoor
        else:
            print "[ EuclideanCoordinate Fatal Error] Invalid input vector dimension in coordinate add operation!"
            return self.getCoor()
        
    def __sub__(self, coor):
        if (len(coor.vec) == self.dim):
            tmpVec = []
            for i in xrange(self.dim):
                tmpVec.append(self.vec[i] - coor.vec[i])
            tmpCoor = EuclideanCoordinate(self.dim)
            tmpCoor.setCoor(tmpVec)
            return tmpCoor
        else:
            print "[ EuclideanCoordinate Fatal Error] Invalid input vector dimension in coordinate sub operation!"
            tmpCoor = EuclideanCoordinate(self.dim)
            tmpCoor.setCoor(self.vec)
            return tmpCoor
    
    def __mul__(self, n):
        tmpVec = []
        for i in xrange(self.dim):
            tmpVec.append(self.vec[i] * n) 
        tmpCoor = EuclideanCoordinate(self.dim)
        tmpCoor.setCoor(tmpVec)
        return tmpCoor
    
    def __rmul__(self, n):
        return self * n

    def getDistance(self, coor):
        tmpCoor = self - coor
        tmpSum = 0.0
        for i in xrange(self.dim):
           tmpSum = tmpSum + tmpCoor.vec[i]**2
        dist = math.sqrt(tmpSum)
        return dist

    def getDirection(self, coor):
        tmpCoor = self - coor
        dist = self.getDistance(coor)
        if (dist != 0.0):
            tmpCoor = tmpCoor * (1 / dist)
            return tmpCoor
        else:
            for i in xrange(self.dim):
                tmpCoor.vec[i] = random.uniform(0.1, 10)
            dist = tmpCoor.getDistance(EuclideanCoordinate(self.dim))
            tmpCoor = tmpCoor * (1 / dist)
            return tmpCoor
