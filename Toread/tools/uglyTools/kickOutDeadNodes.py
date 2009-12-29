#!/usr/bin/env python
'''
this file can be used to kick out the dead nodes,which is in the deadnodelist, from the nodelist
'''
import sys

if (__name__=="__main__"):
	if len(sys.argv)!=4:
		print '''usage: python kickOutDeadNode.py nodelist deadnodelist resultlist'''
	nodelist = sys.argv[1]
	deadlist = sys.argv[2]
        resultlist = sys.argv[3]
        nfile = open(nodelist,'r')
        dfile = open(deadlist,'r')
        rfile = open(resultlist,'w')
        allnodes = []
        deadnodes = []
        for line in nfile.readlines():
            line = line.strip()
            allnodes.append(line)
        nfile.close()
        for line in dfile.readlines():
            line = line.strip()
            deadnodes.append(line)
        dfile.close()
        for node in deadnodes:
            try:
                allnodes.remove(node)
                print "Remove the host:",node
            except:
                print "The nodelist file does not contain the host:",node
        for node in allnodes:
            rfile.write(node+'\n')
        rfile.close()

	
