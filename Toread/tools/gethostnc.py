#!/usr/bin/env python


import socket
import sys
sys.path.append('..')
import pickle
import sys
from Vivaldi import Vivaldi

nodelist = open("../..//debugNodes.txt")

PORT=51234
BUFLEN = 2048

def getNodeNCObj( hostname, token ):
	sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ip = socket.gethostbyname(hostname)
	sockfd.settimeout(10)
	try:
		sockfd.connect((ip,PORT))
		sockfd.send(token)
		ncbuf = sockfd.recv(BUFLEN)
		sockfd.close()
		ncobj = pickle.loads(ncbuf)
		return ncobj
	except:
		print "Error when connecting to ", hostname
		sockfd.close()
		return None
#		sys.exit(1)


if (__name__=="__main__"):
	msg="Vivaldi"
	hosts = []
	for eachLine in nodelist:
		eachLine=eachLine.strip()
		hosts.append(eachLine)
	for host in hosts:
		print host
		ncobj = getNodeNCObj( host, msg )
		if ncobj==None:
			continue
		print "hostname: ", host
		print "host ip:", ncobj.ip
		print "host nc:", ncobj.vec, "  height:", ncobj.height
		print "host error:", ncobj.error
