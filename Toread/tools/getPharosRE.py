#!/usr/bin/env python


import socket
import sys
sys.path.append('..')
import pickle
import math
import time
import random
from Pharos import PHAROS
from config import *



PORT=NCPORT
BUFLEN = 2048
TCP = False

def getNodeNCObj( hostname, token ):
	try:
		try:
			ip = socket.gethostbyname(hostname)
		except:
			print "Get host name error:", hostname
			return None
		sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sockfd.settimeout(10)
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

def saveLocalErr( outfile = "" , globalerrDict = {}, globalncDict={}, clustererrDict = {}, clusterncDict={}, hostidDict = {}):
	if(len(outfile)==0):
		return False
	fd = open( outfile, 'w')
	for k in globalerrDict.keys():
		fd.write("[ClusterID]	" + k + "	" + hostidDict[k] +"\n")
		fd.write( "[Golbal NC and Error]	" + k + "    " + str(globalncDict[k]) + "    " + str(globalerrDict[k]) + "\n")
		fd.write( "[Cluster NC and Error]	" + k + "    " + str(clusterncDict[k]) + "    " + str(clustererrDict[k]) + "\n")
	fd.close()
	return True
	

def udpPing(hostname):
	pround = 5  # ping 5 times and use the average rtt
	port = PINGPORT
	ip = socket.gethostbyname( hostname )
	rtt = 0
	for i in range(pround):
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			sock.settimeout(10)
			rtt = rtt - time.time()
			sock.sendto("this is a tcp ping test!\n",(ip,port))
			buf = sock.recv(1024)
			rtt = rtt + time.time()
			sock.close()
		except:
			print "Error when ping host: ", hostname
			return -100
	rtt = rtt / pround
	return rtt * 1000  # time.time() returns the seconds, here we need micro-seconds	

def tcpPing(hostname):
	pround = 5 # ping 5 times and use the average rtt
	port = PINGPORT
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
		print "calculating the distance is wrong!"
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
	msg="PharosInfo"
	myselfname = socket.gethostname()

#
#This tool can caculate the CNAE, RE of the Pharos system
#
	#inputfile = "../../nodelist.txt"
	#inputfile = "../../pharosDebuglist.txt"
	inputfile = "../../myPLnodes.txt"
	out_re_file = "../evaluationResult/pharosRE.txt"
	out_err_file = "../evaluationResult/pharosErr.txt"
	out_cnae_file = "../evaluationResult/pharosCNAE.txt"
	usingHeight = True

	# get the nc of myself
	mync = getNodeNCObj( myselfname, msg )
	if(mync==None):
		print "can not get NC of myself!"
		sys.exit(1)
	myglobalvec = mync.globalvec
	myglobalvec.append(mync.globalheight)
	myglobalerr = mync.globalerror
	myclustervec = mync.clustervec
	myclustervec.append(mync.clusterheight)
	myclustererr = mync.clustererror
	myclusterid = mync.clusterID
	

	hosts = loadHost( inputfile )
	# shuffle the host, make sure the traffic is not converge to one node at the same time
	random.shuffle(hosts)

	hostGlobalNC = {}
	hostClusterNC = {}
	hostGlobalErr = {}
	hostClusterErr = {}
	hostID = {}
	hostRTT = {}

	hostGlobalNC[myselfname] = myglobalvec
	hostGlobalErr[myselfname] = myglobalerr
	hostClusterErr[myselfname] = myclustererr
	hostClusterNC[myselfname] = myclustervec
	hostID[myselfname] = myclusterid
	REdict = {}
	
	refreshMe = 5
	count = 0

# the vars is used to caculate the CNAE
	smallestRTT = 100000
	nearestHost = "" # the real nearest host
	ncOptRtt = 100000
	ncOptHost = ""   # the nearest host using NC predicted rtt
	ncSmallestRTT = 10000

	for host in hosts:
		if count==refreshMe:
			count = 0
			# get the nc of myself
			mync = getNodeNCObj( myselfname, msg )
			if(mync==None):
				print "can not get NC of myself!"
				sys.exit(1)
			print "Refreshing the information of myself..."
			myglobalvec = mync.globalvec
			myglobalvec.append(mync.globalheight)
			myglobalerr = mync.globalerror
			myclustervec = mync.clustervec
			myclustervec.append(mync.clusterheight)
			myclustererr = mync.clustererror
			myclusterid = mync.clusterID	
			hostGlobalNC[myselfname] = myglobalvec
			hostGlobalErr[myselfname] = myglobalerr
			hostClusterErr[myselfname] = myclustererr
			hostClusterNC[myselfname] = myclustervec
			hostID[myselfname] = myclusterid						
		if(host==myselfname):
			continue
		ncobj = getNodeNCObj( host, msg )
		count = count + 1
		if ncobj==None:
			continue
		ncobj.globalvec.append(ncobj.globalheight)
		ncobj.clustervec.append(ncobj.clusterheight)
		hostGlobalNC[host] = 	ncobj.globalvec
		hostGlobalErr[host] = ncobj.globalerror
		hostClusterErr[host] = ncobj.clustererror
		hostClusterNC[host] = ncobj.clustervec
		hostID[host] = ncobj.clusterID
		
		# calculate the RE
		k = myselfname + "--->" + host
		rtt = -100
		if TCP == True:
			rtt = tcpPing(host)
		else:
			rtt = udpPing(host)
		if (rtt == -100):
			print "ping ",host," Error!"
			continue
		#add rtt to dictionary
		hostRTT[host] = rtt
		if hostID[host] == hostID[myselfname]:
			predicted_rtt = calDistance( hostClusterNC[myselfname], hostClusterNC[host] , PHAROS_USING_HEIGHT_LOCAL)
		else:
			predicted_rtt = calDistance( hostGlobalNC[myselfname], hostGlobalNC[host] , PHAROS_USING_HEIGHT_GLOBAL)
		re = abs(rtt-predicted_rtt)/min(rtt,predicted_rtt)
		REdict[k] = re
		print "RE result:",k,"=",re
		
		# the following is about the CNAE
		if(predicted_rtt<ncSmallestRTT):
			ncSmallestRTT = predicted_rtt
			ncOptHost = host
			ncOptRtt = rtt
		if(rtt<smallestRTT):
			smallestRTT = rtt
			nearestHost = host

#		print "hostname: ", host
#		print "host ip:", ncobj.ip
#		print "host nc(including height):", ncobj.vec
#		print "host error:", ncobj.error

	r = saveResult( out_re_file, REdict )
	if(not r):
		print "save RE result fails!"
	r = saveLocalErr( out_err_file, hostGlobalErr, hostGlobalNC , hostClusterErr, hostClusterNC, hostID)
	if(not r):
		print "save node NC result fails!"
	# record the CNAE information
	cnaeout = open(out_cnae_file,'w')
	cnaeout.write("localhost	nearestPredictedHost	predictedRTT	ncOptRtt	realNearestHost	smallestRTT	CNAE\n")
	cnaeout.write(str(myselfname)+"	"+str(ncOptHost)+"	"+str(ncSmallestRTT)+"	"+str(ncOptRtt)+"	"+str(nearestHost)+"	"+str(smallestRTT)+"	"+str(ncOptRtt-smallestRTT)+"\n")
	cnaeout.close()
	
