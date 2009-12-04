from CoordinateIF import *

def zeros(dim):
	vec = []
	for i in xrange(dim):
		vec.append(0.0)
	return vec

class EuclideanCoordinate(CoordinateIF):
    dim = DIMENTION

    def __init__(self):
        self.setCoor(zeros(self.dim))
    
    def setCoor(self, vec):
        if (len(vec) == self.dim):
            self.vec = vec[:]
        else:
            print 'Invalid input vector in construction function of class EuclideanCoordinate!'
            self.vec = []
            for i in xrange(self.dim):
                 self.vec.append(0.0)
                 
    def getCoor(self):
		tmpCoor = EuclideanCoordinate()
		tmpCoor.setCoor(self.vec)
		return tmpCoor
                 
    def printCoor(self):
        print 'Coordinate:'+str(self.vec)   #maybe write in log file

    def __add__(self, coor):
        if (len(coor.vec) == self.dim):
            tmpVec = []
            for i in xrange(self.dim):
                tmpVec.append(self.vec[i] + coor.vec[i])
            tmpCoor = EuclideanCoordinate()
            tmpCoor.setCoor(tmpVec)
            return tmpCoor
        else:
            print 'Invalid coordinate in add operation!'
            return self.getCoor()
        
    def __sub__(self, coor):
        if (len(coor.vec) == self.dim):
            tmpVec = []
            for i in xrange(self.dim):
                tmpVec.append(self.vec[i] - coor.vec[i])
            tmpCoor = EuclideanCoordinate()
            tmpCoor.setCoor(tmpVec)
            return tmpCoor
        else:
            print 'Invalid coordinate in sub operation!'
            tmpCoor = EuclideanCoordinate()
            tmpCoor.setCoor(self.vec)
            return tmpCoor
    
    def __mul__(self, n):
        tmpVec = []
        for i in xrange(self.dim):
            tmpVec.append(self.vec[i] * n) 
        tmpCoor = EuclideanCoordinate()
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
            dist = tmpCoor.getDistance(EuclideanCoordinate())
            tmpCoor = tmpCoor * (1 / dist)
            return tmpCoor
