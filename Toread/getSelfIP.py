#! /usr/bin/env python
#coding=utf-8

''' get my ip service writen in python'''

import re,urllib2
class getSelfIP():
    def getip(self):
        try:
            myip = self.visit("http://www.ip138.com/ip2city.asp")
        except:
            try:
                myip = self.visit("http://www.bliao.com/ip.phtml")
            except:
                try:
                    myip = self.visit("http://www.whereismyip.com/")
                except:
                    print "Error occurs when getting myself IP"
                    myip = None
        return myip
    
    def visit(self,url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)        

''' unit test code

if __name__=="__main__":
    test = getSelfIP()
    print test.getip()
    
    '''