from twisted.internet.protocol import DatagramProtocol
from time import time
from twisted.internet import defer
from subprocess import PIPE, Popen
import shlex
from config import *
import os
import string
import random
#from Vivaldi import Vivaldi


class HTTPPingClient():
        def __init__(self, option):
                self.option = option
                self.count = 0
                self.time = 0
                self.done = False
                self.sigma = map(chr, range(256))
                self.defer = defer.Deferred()


	def sendData(self):
		pid = self.sigma[self.count]
                data = pid+'\x00'*(self.option.bytes-1)
		
		allowed = string.ascii_letters # add any other allowed characters here
		data = ''.join([allowed[random.randint(0, len(allowed) - 1)] for x in xrange(self.option.bytes)])
 
		url = self.option.host
		#print('Pinging',url)
		cmd =""
		if url in PROXIES:
			cmd='curl -m 180 -w %{time_starttransfer} '+url+':8080/1Mb.dat -o /dev/null'
                else:
			cmd='curl -m 180 -w %{time_starttransfer} '+url+':'+str(self.option.port)+' -o /dev/null -s --data-binary \"'+data+'\"'
                cmd = Popen(shlex.split(cmd),stdout=PIPE, stderr=PIPE)
                command = cmd.poll()
                out, err = cmd.communicate()
		out = float(out.replace(",","."))
		#print url,'<<',out
		return out
	
        def ping(self):
                self.time += self.sendData()
		self.count +=1
		if self.count < self.option.num:
			self.time = self.sendData()
		self.option.time = self.time/self.option.num
		#print self.option.time
                self.defer.callback(self.option)

