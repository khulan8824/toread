#! /usr/bin/env python
#coding=utf-8


import iperf
import time
import socket
import random
import sys
sys.path.append("..")
#import pickle
#import math
#from Pharos import PHAROS
from config import *
from tools import pyxidaGetRE
from tools import getPharosRE

# This option control the ping method, if it is True, it is TCP ping, else it is udp ping
TCP = False

if __name__=="__main__":
    #hostfile = "../../servers.txt"
    hostfile = "servers.txt"
    #pausetime = random.randint(0,500)
    #time.sleep(pausetime)
    hosts = getPharosRE.loadHost(hostfile)
    random.shuffle(hosts)
    rtts={}
    pyxidaRTTs = {}
    BWs = {}
# get the nc of myself
    myselfname = socket.gethostname()
    if myselfname in hosts:
        print "This is a candidate server....  exit the anycast process..."
        sys.exit(0)
    
    
    msg="PharosInfo"
    #if myselfname in hosts:
        #sys.exit(1)
    mync = pyxidaGetRE.getNC( myselfname )
    if(mync==None):
        print "can not get NC of myself!"
        sys.exit(1)
    
    
    refresh = 8
    count = 0
    
    for h in hosts:
        if count == refresh:
            print "[anycast evaluation] refreshing myself information!"
            mync = pyxidaGetRE.getNC( myselfname )
            if(mync==None):
                print "can not get NC of myself!"
                sys.exit(1)
            count = 0

        hnc = pyxidaGetRE.getNC( h )
        if hnc==None:
            print "Fail to get the Coor of ",h
            continue
        if not hnc==None:
            prtt = pyxidaGetRE.calDistance(mync, hnc)
            pyxidaRTTs[h] = prtt
            count = count + 1

        if TCP == True:
            rtt = getPharosRE.tcpPing(h)
        else:
            rtt = getPharosRE.udpPing(h)
        if rtt==-100:
            print "ping ",h," Error!"
            continue
        else:
            rtts[h] = rtt

        band = iperf.measureBWnum(h)
        if not band==None:
            BWs[h] = band

        st = random.randint(2,20)
        time.sleep(st)  # comment this when debugging
        print "sleep time:",st,"(s)"

    minrtt = 90000
    fullpinghost = None
    for k in rtts.keys():
        if k not in BWs.keys():
            continue
        if rtts[k]<minrtt:
            minrtt = rtts[k]
            fullpinghost = k
    minrtt = 900000
    pyxidahost = None
    for k in pyxidaRTTs.keys():
        if k not in BWs.keys():
            continue
        if pyxidaRTTs[k]<minrtt:
            minrtt = pyxidaRTTs[k]
            pyxidahost = k

    robinhost = BWs.keys()[random.randint(0,len(BWs.keys())-1)]
    bigBWhost = None
    tmpband = 0
    for k in BWs.keys():
        if BWs[k]>tmpband:
            tmpband = BWs[k]
            bigBWhost = k
    #print for debug
    print "pyxidaRTTs",pyxidaRTTs
    print "rtts",rtts
    print "BWs",BWs
    print "pyxidahost:",pyxidahost
    print "robinhost:",robinhost
    print "fullpinghost:",fullpinghost
    print "biggest bandwidth host:",bigBWhost

    fout = open("../evaluationResult/AnycastDATA.txt",'w')
    fout.write("pyxida-anycast-bandwidth(KB/sec)    "+ str(BWs[pyxidahost]) + "\n")
    fout.write("round-robin-anycast-bandwidth(KB/sec)    "+ str(BWs[robinhost]) + "\n")
    fout.write("full-ping-anycast-bandwidth(KB/sec)   "+ str(BWs[fullpinghost]) + "\n")
    fout.write("biggest-bandwidth(KB/sec)   "+ str(BWs[bigBWhost]) + "\n")
    fout.write("pyxida-anycast-rtt(ms)  "+ str(rtts[pyxidahost]) +"\n")
    fout.write("rrobin-anycast-rtt(ms)  "+ str(rtts[robinhost]) +"\n")
    fout.write("full-ping-anycast-rtt(ms)  "+ str(rtts[fullpinghost]) +"\n")
    if(fullpinghost==pyxidahost):
        r = 1
    else:
        r = 0
    fout.write("pyxida-hit-smallestRTT   "+ str(r) + "\n")
    if(bigBWhost==pyxidahost):
        r = 1
    else:
        r = 0
    fout.write("pyxida-hit-biggestBW   "+ str(r) + "\n")
    if(fullpinghost==robinhost):
        r = 1
    else:
        r = 0
    fout.write("rrobin-hit-smallestRTT   "+ str(r) + "\n")
    if(bigBWhost==robinhost):
        r = 1
    else:
        r = 0
    fout.write("rrobin-hit-biggestBW   "+ str(r) + "\n")   
    fout.close()



            




