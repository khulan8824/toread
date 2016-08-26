from config import *
import operator


class Route(object):
	def __init__(self,ip,distance,proxy=False, ttfb=0, myProxy=False):
		self.ip = ip
		self.distance = distance
		self.ttfb = ttfb
		self.proxy = proxy
		self.myProxy = myProxy
	
	def updateDistance(self,distance):
		self.distance = distance
	
	def getDistance(self):
		return self.distance
	
	def updateTTFB(self,ttfb):
		self.ttfb = ttfb
	
	def getTTFB(self):
		return self.ttfb
	
	def makeMyProxy(self):
		self.myProxy = True
	
	def unmakeMyProxy(self):
		self.myProxy = False
	
	def isProxy(self):
		return self.proxy

	def __str__(self):
		return "{0}\t{1}\t{2}\t{3}\t{4}\n".format(self.ip,self.distance,self.proxy,self.ttfb,self.myProxy)


		
class RoutingTable(object):
	def __init__(self):
		self.routes = {}
		self.proxy = None
	
	def addRoute(self,ip,distance,ttfb=0,myProxy=False):
		proxy = True if ip in PROXIES else False
		route = Route(ip=ip,distance=distance,proxy=proxy,ttfb=ttfb,myProxy=myProxy)
		self.routes[ip] = route
		if myProxy:
			self.proxy = ip

	def updateDistance(self, ip , distance):
		self.routes[ip].updateDistance(distance)

	def selectProxy(self,ip):
		self.routes[self.proxy].unmakeMyProxy()
		self.routes[ip].makeMyProxy()
	
	def updateTTFB(self,ip,ttfb):
		self.routes[ip].updateTTFB(ttfb)
	

	def store(self):
		with open(VIVALDI_ROUTE_TABLE,'wb') as f:
			f.write("ip\tdistance\tproxy\tTTFB\tmyProxy\n")
			for r in sorted(self.routes.values(),key=operator.attrgetter('distance')):
				f.write(r.__str__())
				#print r.__str__()
	
