from EuclideanCoordinate import *

class HeightCoordinate(CoordinateIF):
    dim = -1
    
    def __init__(self, arg_dim = DIMENTION):
        self.dim = arg_dim
        self.setCoor(zeros(self.dim), THRESHOLD_HEIGHT)
    
    def setCoor(self, vec, height):
        if (len(vec) == self.dim):
            self.vec = vec[:]
            self.height = height
            if(self.height < THRESHOLD_HEIGHT):
                self.height = THRESHOLD_HEIGHT
        else:
            print "[ HeightCoordinate Fatal Error ] Invalid input vector dimension in setCoor!"
            print "[ HeightCoordinate Fatal Error ] Input vector dimension:", len(vec),"    HeightCoordinate dimension:", self.dim
            self.vec = []
            for i in xrange(self.dim):
                 self.vec.append(0.0)
            self.height = height
            if(self.height < THRESHOLD_HEIGHT):
                self.height = THRESHOLD_HEIGHT
                 
    def getCoor(self):
        tmpCoor = HeightCoordinate(self.dim)
        tmpCoor.setCoor(self.vec, self.height)
        return tmpCoor
                 
    def printCoor(self):
        print 'Coordinate:'+str(self.vec)+' Height:'+str(self.height)   #maybe write in log file
        
    def __add__(self, coor):
        if (len(coor.vec) == self.dim):
            tmpVec = []
            for i in xrange(self.dim):
                tmpVec.append(self.vec[i] + coor.vec[i])
            tmpHeight = self.height + coor.height
            if (tmpHeight < THRESHOLD_HEIGHT):
                tmpHeight = THRESHOLD_HEIGHT
            tmpCoor = HeightCoordinate(self.dim)
            tmpCoor.setCoor(tmpVec, tmpHeight)
            return tmpCoor
        else:
            print "[ HeightCoordinate Fatal Error ] Invalid input vector dimension in coordinate add operation!"
            return self.getCoor()
    
    def __sub__(self, coor):
        if (len(coor.vec) == self.dim):
            tmpVec = []
            for i in xrange(self.dim):
                tmpVec.append(self.vec[i] - coor.vec[i])
            tmpHeight = self.height + coor.height
            tmpCoor = HeightCoordinate(self.dim)
            tmpCoor.setCoor(tmpVec, tmpHeight)
            return tmpCoor
        else:
            print "[ HeightCoordinate Fatal Error ] Invalid input vector dimension in coordinate sub operation!"
            return self.getCoor()
    
    def __mul__(self, n):
        tmpVec = []
        for i in xrange(self.dim):
            tmpVec.append(self.vec[i] * n)
        tmpCoor = HeightCoordinate(self.dim)
        tmpCoor.setCoor(tmpVec, THRESHOLD_HEIGHT)
        tmpCoor.height = self.height * n
        return tmpCoor
    
    def __rmul__(self, n):
        return self * n
    
    def getDistance(self, coor):
        tmpCoor = self - coor
        tmpSum = 0.0
        for i in xrange(self.dim):
           tmpSum = tmpSum + tmpCoor.vec[i]**2
        dist = math.sqrt(tmpSum) + tmpCoor.height
        return dist

    def getDirection(self, coor):
        tmpCoor = self - coor
        dist = self.getDistance(coor)
        if (dist != self.height + coor.height):
            tmpCoor = tmpCoor * (1 / dist)
            return tmpCoor
        else:
            for i in xrange(self.dim):
                tmpCoor.vec[i] = random.uniform(0.1, 10)
            dist = tmpCoor.getDistance(HeightCoordinate(self.dim))
            tmpCoor = tmpCoor * (1 / dist)
            return tmpCoor

