#! /usr/bin/env python
#coding=utf-8
import re
import socket
import random
import time
import math

import sys
sys.path.append('..')
import pickle
import random
from Vivaldi import Vivaldi
from config import *


PORT=NCPORT
BUFLEN = 2048

#socket.setdefaulttimeout(10)

# This option control the ping method, if it is True, it is TCP ping, else it is udp ping
TCP = (PINGMETHOD=="TCP")

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

def udpPing(hostname):
    pround = 4  # ping 5 times and use the average rtt
    port = PINGPORT
    try:
        ip = socket.gethostbyname( hostname )
    except:
        print "DNS query error for ", hostname
        return -100
    rtt = 0
    for i in range(pround):
        try:
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock.settimeout(3)
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
	port = 11232
    	try:
        	ip = socket.gethostbyname( hostname )
	except:
        	print "[TCP ping] unknown hostname:",hostname
	        return -100
	
	rtt = 0
	for i in range(pround):
		try:
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			sock.settimeout(10)
			sock.connect((ip,port))
			#print "[TCP ping] Connect to ",host,"Round",i
			rtt = rtt - time.time()
			sock.send("this is a tcp ping test!\n")
			buf = sock.recv(1024)
			rtt = rtt + time.time()
			sock.close()
		except Exception,e:
			print "Error when ping host: ", hostname
			print e
			return -100
	rtt = rtt / pround
	return rtt * 1000  # time.time() returns the seconds, here we need micro-seconds

def calDistance( nc1=[], nc2=[], Height=True):  # Height means whether we use height vector
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


def saveResult( outputfile = "", REdict = {}, hostRTT = {}, myselfname = ""):
	if(len(outputfile)==0):
		return False
	fd = open(outputfile, 'w')
	for k in REdict.keys():
		fd.write( k + "    " + str(REdict[k]) + "\n" )
	for k  in hostRTT.keys():
        	fd.write("[RTT] From    " + myselfname + " to  " + k +":    " + str(hostRTT[k]) + "\n")
	fd.close()
	return True

def saveNC( outfile = "" , ncDict = {}):
	if(len(outfile)==0):
		return False
	fd = open( outfile, 'w')
	for k in ncDict.keys():
		fd.write( "[NC DATA]	" + k + "    " + str(ncDict[k]) + "\n")
	fd.close()
	return True


if (__name__=="__main__"):
    #
    #This tool can caculate the CNAE, RE of the Vivaldi system
    #
    inputfile = "../../myGufinodes.txt"
    #inputfile = "../../pharosDebuglist.txt"
    out_re_file = "../evaluationResult/vivaldiRE.txt"
    out_err_file = "../evaluationResult/vivaldiNC.txt"
    out_cnae_file = "../evaluationResult/vivaldiCNAE.txt"   
    
    ncDict = {}
    reDict = {}
    hostRTT = {}
    
    myselfname = socket.gethostname()
    
    msg = "Vivaldi"
    
    # get the nc of myself
    mync = getNodeNCObj( myselfname, msg )
    if(mync==None):
        print "can not get NC of myself!"
        sys.exit(1)
    tl = list(mync.vec)
    tl.append(mync.height)
    ncDict[myselfname] = tl

    hosts = loadHost( inputfile )
    # shuffle the host, make sure the traffic is not converge to one node at the same time
    random.shuffle(hosts)
  
    refreshMe = 10
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
            tl = list(mync.vec)
            tl.append(mync.height)
            ncDict[myselfname] = tl	
        if(host==myselfname):
            continue
        ncobj = getNodeNCObj( host, msg )
        count = count + 1
        if ncobj==None:
            continue
        tl = list(ncobj.vec)
        tl.append(ncobj.height)
        ncDict[host] = tl	
        print host," NC:",ncDict[host]
        
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
        predicted_rtt = calDistance( ncDict[myselfname], ncDict[host] )
		
		# method 1 for re
        re = abs(rtt-predicted_rtt)/min(rtt,predicted_rtt)
		
		# method 2 for re
		#re = abs(rtt-predicted_rtt)/abs(rtt)
        reDict[k] = re
        print "RE result:",k,"=",re
        
        # the following is about the CNAE
        if(predicted_rtt<ncSmallestRTT):
            ncSmallestRTT = predicted_rtt
            ncOptHost = host
            ncOptRtt = rtt
        if(rtt<smallestRTT):
            smallestRTT = rtt
            nearestHost = host

    r = saveResult( out_re_file, reDict , hostRTT, myselfname )
    if(not r):
        print "save RE result fails!"
    r = saveNC( out_err_file, ncDict )
    if(not r):
        print "save node NC result fails!"
    # record the CNAE information
    cnaeout = open(out_cnae_file,'w')
    cnaeout.write("localhost	nearestPredictedHost	predictedRTT	ncOptRtt	realNearestHost	smallestRTT	CNAE\n")
    cnaeout.write(str(myselfname)+"	"+str(ncOptHost)+"	"+str(ncSmallestRTT)+"	"+str(ncOptRtt)+"	"+str(nearestHost)+"	"+str(smallestRTT)+"	"+str(ncOptRtt-smallestRTT)+"\n")
    cnaeout.close()
    
