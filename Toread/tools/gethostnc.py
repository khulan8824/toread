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



def getVivaldiNC(filename, outfile):
	msg="Vivaldi"
	hosts = []
	fh = open(filename,'r')
	for eachLine in fh.readlines():
		eachLine=eachLine.strip()
		hosts.append(eachLine)
	fh.close()
	#print hosts
	ofh = open(outfile,'w')
	ofh.write("hostname#host-ip#host-nc#height#error\n")
	for host in hosts:
		print host
		ncobj = getNodeNCObj.getNC( host, msg )
		if ncobj==None:
			continue
		print "hostname: ", host
		print "host ip:", ncobj.ip
		print "host nc:", ncobj.vec, "  height:", ncobj.height
		print "host error:", ncobj.error
		ncstr=""
		for v in ncobj.vec:
			if len(ncstr)==0:
				ncstr = ncstr + str(v)
			else:
				ncstr = ncstr + " " + str(v)
		ofh.write(str(host)+ "#" + str(ncobj.ip) + "#" + ncstr + "#" + str(ncobj.height) + "#" + str(ncobj.error) + "\n")
	ofh.close()

def getPharosNC(filename, outfile):
	msg = "PharosInfo"
	hosts = []
	fh = open(filename,'r')
	for eachLine in fh.readlines():
		eachLine=eachLine.strip()
		hosts.append(eachLine)
	fh.close()
	#print hosts
	ofh = open(outfile,'w')
	ofh.write("hostname#host-ip#globalnc#globalHeight#globalError#clusterID#clusterNC#clusterHeight#clusterError\n")
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
		ncinfo = formatPharosString(host, ncobj)
		ofh.write(ncinfo + '\n')
	ofh.close()

def formatPharosString(hostname, ncobj):
	res = hostname + "#" + str(ncobj.ip)
	gncstr=""
	for v in ncobj.globalvec:
		if len(gncstr)==0:
			gncstr = gncstr + str(v)
		else:
			gncstr = gncstr + " " + str(v)
	res = res + "#" + gncstr + "#" + str(ncobj.globalheight) + "#" + str(ncobj.globalerror) + "#" + ncobj.clusterID
	cncstr = ""
	for v in ncobj.clustervec:
		if len(cncstr)==0:
			cncstr = cncstr + str(v)
		else:
			cncstr = cncstr + " " + str(v)
	res = res + "#" + cncstr + "#" + str(ncobj.clusterheight) + "#" + str(ncobj.clustererror)
	return res
	
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
	if (len(sys.argv)!=4):
		print '''usage: python gethostnc.py ncAlgorithm nodelistfile NCinfoFile
		If you want to use default nodelistfile, use the command like this: python gethostnc.py ncAlgorithm default NCinfoFile'''
		sys.exit(1)
	ncAlgorithm = sys.argv[1]
	nodelistfile = sys.argv[2]
	ncinfofile = sys.argv[3]
	if nodelistfile.lower()!="default":
		nodelist = nodelistfile
	
	if ncAlgorithm.lower()=="vivaldi":
		getVivaldiNC(nodelist, ncinfofile)
		
	if ncAlgorithm.lower()=="pharos":
		getPharosNC(nodelist, ncinfofile)
