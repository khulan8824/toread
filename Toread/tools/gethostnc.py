#!/usr/bin/env python


import socket
import sys
sys.path.append('..')
import pickle
import sys
import getNodeNCObj
from Vivaldi import Vivaldi
from Pharos import PHAROS


nodelist = "../..//debugNodes.txt"



def getVivaldiNC(filename):
	msg="Vivaldi"
	hosts = []
	fh = open(filename,'r')
	for eachLine in fh.readlines():
		eachLine=eachLine.strip()
		hosts.append(eachLine)
	fh.close()
	#print hosts
	for host in hosts:
		print host
		ncobj = getNodeNCObj.getNC( host, msg )
		if ncobj==None:
			continue
		print "hostname: ", host
		print "host ip:", ncobj.ip
		print "host nc:", ncobj.vec, "  height:", ncobj.height
		print "host error:", ncobj.error

def getPharosNC(filename):
	msg = "PharosInfo"
	hosts = []
	fh = open(filename,'r')
	for eachLine in fh.readlines():
		eachLine=eachLine.strip()
		hosts.append(eachLine)
	fh.close()
	#print hosts
	for host in hosts:
		print host
		ncobj = getNodeNCObj.getNC( host, msg )
		if ncobj==None:
			continue
		print "hostname: ", host
		print "host ip:", ncobj.ip
		print "global host nc:", ncobj.globalvec, "  height:", ncobj.globalheight
		print "cluster host nc:", ncobj.clustervec, "  height:", ncobj.clusterheight
		print "cluster ID:", ncobj.clusterID
		print "global host error:", ncobj.globalerror	
		print "cluster host error:", ncobj.clustererror

'''
class PharosInfo():
    ip = ""
    globalvec = []
    globalheight = 0
    clustervec = []
    clusterheight = 0
    clusterID = ""
    globalerror = 0
    clustererror = 0
'''





if (__name__=="__main__"):
	if (len(sys.argv)!=3):
		print '''usage: python gethostnc.py ncAlgorithm nodelistfile
		If you want to use default nodelistfile, use the command like this: python gethostnc.py ncAlgorithm default'''
		sys.exit(1)
	ncAlgorithm = sys.argv[1]
	nodelistfile = sys.argv[2]
	if nodelistfile.lower()!="default":
		nodelist = nodelistfile
	
	if ncAlgorithm.lower()=="vivaldi":
		getVivaldiNC(nodelist)
		
	if ncAlgorithm.lower()=="pharos":
		getPharosNC(nodelist)
