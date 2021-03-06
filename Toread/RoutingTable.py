from config import *
from queryProxy import queryProxy
import operator
import os
from time import time, sleep
import simpleflock
import random


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
		self.command_pending = None
	
	def updateDistance(self,distance):
		self.distance =float(distance)/1000.0
		self.total = self.distance + self.ttfb
	
	def getDistance(self):
		return self.distance

	def getPendingCommand(self):
		return self.command_pending

	def setPendingCommand(self, command_pending):
		self.command_pending = command_pending
	
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

	def checkTTFBUpdate(self):
		proxies = self.routes.keys()
		to_query = []
		current_time = time()
		if self.proxy:
			proxies.remove(self.proxy)
		# Choose random proxy
		for proxy in proxies:
			route = self.routes[proxy]
			# If a command is pending from previous round
			command_pending = route.getPendingCommand()
			if command_pending:
				code = command_pending.poll()
				if code is not None:
					out, err = command_pending.communicate()
					self.updateTTFB(proxy,out,0)
					route.setPendingCommand(None)
				# No need for else, if no results check next time
				continue
			# If time from last known measurement higher than threshold
			if (current_time-route.last_ttfb_time) > (PROXY_RECOVER_TIME+route.distance*1000) and (route.distance*1000 < 20):
				to_query.append(proxy)
			elif (current_time-route.last_ttfb_time) > (PROXY_RECOVER_TIME+route.distance):
				to_query.append(proxy)
		cmd = None
		proxyToQuery = None
		if len(to_query) == 1:
			proxyToQuery = to_query[0]
			cmd = queryProxy(proxyToQuery)
		# If many nodes choose randomly
		elif len(to_query) > 1:
			proxyToQuery = random.sample(proxies,1)[0]
			cmd =queryProxy(proxyToQuery)
		else:
			return
		
		sleep(1)
		code = cmd.poll()
		if code is not None:
			out, err = cmd.communicate()
			self.updateTTFB(proxyToQuery,out,0)
		else:
			route.setPendingCommand(cmd)


	def chooseBestProxy(self):
		metric = 'total'
		routes = self.routes.values()
		proxy_routes = [r for r in routes if r.proxy]
		if proxy_routes:
			min_route = min(proxy_routes,key=operator.attrgetter(metric))
			if self.proxy:
				if metric == 'total':
				#Change proxy only if difference with current route more than 200 ms
					if abs(min_route.total - self.routes[self.proxy].total) < CHANGE_PROXY_TOTAL_THRESHOLD:
						return
				elif metric == 'distance':
					if abs(min_route.distance - self.routes[self.proxy].distance) < CHANGE_PROXY_DISTANCE_THRESHOLD:
						return
			self.chooseAsProxy(min_route.ip)

	def store(self):
		with simpleflock.SimpleFlock("/tmp/foolock1"):
			with open(self.outfile,'wb') as f:
				f.write("ip\test_rtt\tTTFB\tTotal\tproxy\tmyProxy\n")
				for r in sorted(self.routes.values(),key=operator.attrgetter('total')):
					f.write(r.__str__())
					#print r.__str__()
	
