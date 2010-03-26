#! /usr/bin/env python
#coding=utf-8
'''
    this script gets the Pyxida NC information of myself
'''

import pyxidaGetRE
import socket
import sys

def vecToStr(vec):
    s = ""
    for v in vec:
        if len(s)==0:
            s = s + str(v)
        else:
            s = s + '\t' + str(v)
    return s



myselfname = socket.gethostname()
mync = pyxidaGetRE.getNC( myselfname )
if(mync==None):
    print "can not get NC of myself!"
    sys.exit(1)

out_file = "../evaluationResult/myPyxidaNC.nc"
# save the result
# Format : "hostname    NC"
ofh = open(out_file, 'w')
ofh.write(str(myselfname) + '\t' + vecToStr(mync) + '\n')
ofh.close()
