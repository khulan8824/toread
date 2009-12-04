#!/usr/bin/env python


import socket
import sys
sys.path.append('..')
import pickle
import math
import time
from Vivaldi import Vivaldi



PORT=11234
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


def loadHost(hostfile=""):
	if (len(hostfile)==0):
		return None;
	hostlist=[]
	fd = open(hostfile,'r')
	lines = fd.readlines()
	fd.close()
	for line in lines:
		h = line.split()[0]
		if(len(h)):
			hostlist.append(h)
	return hostlist

def saveResult( outputfile = "", REdict = {}):
	if(len(outputfile)==0):
		return False
	fd = open(outputfile, 'w')
	for k in REdict.keys():
		fd.write( k + "    " + str(REdict[k]) + "\n" )
	fd.close()
	return True

def saveLocalErr( outfile = "" , errDict = {}, ncDict={}):
	if(len(outfile)==0):
		return False
	fd = open( outfile, 'w')
	for k in errDict.keys():
		fd.write( k + "    " + str(ncDict[k]) + "    " + str(errDict[k]) + "\n")
	fd.close()
	return True
	

def tcpPing(hostname):
	pround = 5 # ping 5 times and use the average rtt
	port = 11232
	ip = socket.gethostbyname( hostname )
	rtt = 0
	for i in range(pround):
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock.settimeout(10)
			sock.connect((ip,port))
			rtt = rtt - time.time()
			sock.send("this is a tcp ping test!\n")
			buf = sock.recv(1024)
			rtt = rtt + time.time()
			sock.close()
		except:
			print "Error when ping host: ", hostname
			return -100
	rtt = rtt / pround
	return rtt * 1000  # time.time() returns the seconds, here we need micro-seconds
	


def calDistance( nc1=[], nc2=[], Height=False):  # Height means whether we use height vector
	if(len(nc1)!=len(nc2)):
		print "calculating the distance is wrong!\n"
		return -100;
	l = len(nc1)
	d = 0
	for i in range(l-1):
		d = d + ( nc1[i] - nc2[i] )**2
	d = math.sqrt(d)
	if(Height):
		return d + nc1[l-1] + nc2[l-1]
	else:
		return d


if (__name__=="__main__"):
	msg="Vivaldi"
	myselfname = socket.gethostname()

	inputfile = "../../nodelist.txt"
	out_re_file = "../evaluationResult/RE.txt"
	out_err_file = "../evaluationResult/localErr.txt"
	usingHeight = True

	# get the nc of myself
	mync = getNodeNCObj( myselfname, msg )
	if(mync==None):
		print "can not get NC of myself!"
		sys.exit(1)
	myvec = mync.vec
	myvec.append(mync.height)
	myerr = mync.error

	hosts = loadHost( inputfile )

	hostNC = {}
	hostLocalErr = {}

	hostNC[myselfname] = myvec
	hostLocalErr[myselfname] = myerr
	REdict = {}

	for host in hosts:
		if(host==myselfname):
			continue
		ncobj = getNodeNCObj( host, msg )
		if ncobj==None:
			continue
		ncobj.vec.append(ncobj.height)
		hostNC[host] = 	ncobj.vec
		hostLocalErr[host] = ncobj.error
		# calculate the RE
		k = myselfname + "--->" + host
		rtt = tcpPing(host)
		if (rtt == -100):
			print "ping ",host," Error!"
			continue
		predicted_rtt = calDistance( hostNC[myselfname], hostNC[host] , usingHeight)
		re = abs(rtt-predicted_rtt)/min(rtt,predicted_rtt)
		REdict[k] = re

		print "hostname: ", host
		print "host ip:", ncobj.ip
		print "host nc(including height):", ncobj.vec
		print "host error:", ncobj.error

	r = saveResult( out_re_file, REdict )
	if(not r):
		print "save RE result fails!"
	r = saveLocalErr( out_err_file, hostLocalErr, hostNC )
	if(not r):
		print "save node NC result fails!"
	
	
	

