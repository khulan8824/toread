from config import *
import operator


class Route(object):
	def __init__(self,ip,distance,proxy=False, ttfb=0, myProxy=False):
		self.ip = ip
		self.distance = float(distance)/1000.0
		self.ttfb = float(ttfb)
		self.proxy = proxy
		self.myProxy = myProxy
		self.total = self.distance + self.ttfb
	
	def updateDistance(self,distance):
		self.distance =float(distance)/1000.0
		self.total = self.distance + self.ttfb
	
	def getDistance(self):
		return self.distance
	
	def updateTTFB(self,ttfb):
		self.ttfb = float(ttfb)
		self.total = self.distance + self.ttfb
	
	def getTTFB(self):
		return self.ttfb
	
	def makeMyProxy(self):
		self.myProxy = True
	
	def unmakeMyProxy(self):
		self.myProxy = False
	
	def isProxy(self):
		return self.proxy

	def __str__(self):
		return "{0}\t{1}\t{2}\t{3}\t{4}\n".format(self.ip,self.distance,self.ttfb, self.total, self.proxy,self.myProxy)


		
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

	def chooseAsProxy(self,ip):
		self.routes[self.proxy].unmakeMyProxy()
		self.routes[ip].makeMyProxy()
		self.proxy = ip
	
	def updateTTFB(self,ip,ttfb):
		self.routes[ip].updateTTFB(ttfb)
	

	def chooseBestProxy(self):
		routes = self.routes.values()
		proxy_routes = [r for r in routes if r.proxy]
		if proxy_routes:
			min_route = min(proxy_routes,key=operator.attrgetter('total'))
			self.chooseAsProxy(min_route.ip)

	def store(self):
		with open(VIVALDI_ROUTE_TABLE,'wb') as f:
			f.write("ip\test_rtt\TTFB\tTotal\tproxy\ttotal\tmyProxy\n")
			for r in sorted(self.routes.values(),key=operator.attrgetter('total')):
				f.write(r.__str__())
				#print r.__str__()
	
