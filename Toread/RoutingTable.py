from config import *
import operator
import os
from time import time
import simpleflock

FILE = "vivaldi_ttfb"

class Route(object):
	def __init__(self,ip,distance,proxy=False, ttfb=0, myProxy=False):
		self.ip = ip
		self.distance = float(distance)/1000.0
		self.ttfb = float(ttfb)
		self.proxy = proxy
		self.myProxy = myProxy
		self.total = self.distance + self.ttfb
		self.last_ttfb_time = time()
		self.last_ttfb_backoff = time()
	
	def updateDistance(self,distance):
		self.distance =float(distance)/1000.0
		self.total = self.distance + self.ttfb
	
	def getDistance(self):
		return self.distance

	def setLastBackoff(self,last_backoff):
		self.last_ttfb_backoff = last_backoff


	def getLastBackoff(self):
		return self.last_ttfb_backoff
	
	def updateTTFB(self,ttfb, time_from_last_ttfb):
		current_time = time()
		if (current_time-self.last_ttfb_time) > time_from_last_ttfb : 
			self.ttfb = float(ttfb)
			self.total = self.distance + self.ttfb
			self.last_ttfb_time = current_time - time_from_last_ttfb
	
	def getTTFB(self):
		return self.ttfb

	def setTTFB(self,ttfb):
		self.ttfb = ttfb

	def getTTFBnTime(self):
		return self.ttfb, (time()-self.last_ttfb_time)
	
	def makeMyProxy(self):
		self.myProxy = True
	
	def unmakeMyProxy(self):
		self.myProxy = False
	
	def isProxy(self):
		return self.proxy

	def __str__(self):
		return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(self.ip,self.distance,self.ttfb, self.total, self.proxy,self.myProxy)


		
class RoutingTable(object):
	def __init__(self, outfile='proxy_route_table'):
		self.routes = {}
		self.proxy = None
		self.outfile = outfile
	
	def getRoute(self,ip):
		if ip in self.routes:
			return self.routes[ip]
		else:
			return None
	
	def addRoute(self,ip,distance,ttfb=0,myProxy=False):
		proxy = True if ip in PROXIES else False
		route = Route(ip=ip,distance=distance,proxy=proxy,ttfb=ttfb,myProxy=myProxy)
		self.routes[ip] = route
		if myProxy:
			self.proxy = ip

	def updateDistance(self, ip , distance):
		self.routes[ip].updateDistance(distance)

	def chooseAsProxy(self,ip):
		if self.proxy is not None:
			self.routes[self.proxy].unmakeMyProxy()
		self.routes[ip].makeMyProxy()
		self.proxy = ip
		if DEBUG:
			print "Chosen {} as proxy".format(ip)
	
	def updateTTFB(self,ip,ttfb, time_from_last_ttfb):
		if ip in self.routes:
			self.routes[ip].updateTTFB(ttfb, time_from_last_ttfb)
	
	def readTTFB(self):
		if self.proxy:
			if os.path.isfile(FILE):
				values = []
				with simpleflock.SimpleFlock("/tmp/foolock"):
					with open(FILE,'rb') as infile:
						values = infile.readline().strip().split(',')
				ip = values[0]
				ttfb = values[1]
				if self.proxy == ip:
					self.updateTTFB(self.proxy,ttfb,0)

	def getProxy(self):
		return self.proxy

	def getProxiesIPs(self):
		routes = self.routes.values()
		proxy_ips = [r.ip for r in routes if r.proxy]
		return proxy_ips

	def checkTTFBUpdate(self, neihgbors_number):
		current_time = time()
		for route in self.routes.values():
			last_backoff = route.getLastBackoff()
			t1 = current_time-route.last_ttfb_time
			t2 = current_time - last_backoff
			if t1>neihgbors_number*LOOPTIME and t2 > neihgbors_number*LOOPTIME:
				ttfb = route.getTTFB()
				route.setTTFB(ttfb/2)
				route.setLastBackoff(current_time)



	def chooseBestProxy(self):
		routes = self.routes.values()
		proxy_routes = [r for r in routes if r.proxy]
		if proxy_routes:
			min_route = min(proxy_routes,key=operator.attrgetter('total'))
			self.chooseAsProxy(min_route.ip)

	def store(self):
		with simpleflock.SimpleFlock("/tmp/foolock1"):
			with open(self.outfile,'wb') as f:
				f.write("ip\test_rtt\tTTFB\tTotal\tproxy\tmyProxy\n")
				for r in sorted(self.routes.values(),key=operator.attrgetter('total')):
					f.write(r.__str__())
					#print r.__str__()
	
