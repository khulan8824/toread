
from time import time,sleep
from subprocess import check_output, PIPE, Popen
import csv
import simpleflock
import shlex
import os
import string
import random

EXP_TIME = 17.5*60
FILE = "final_exp_download"
USER = 'david.pinilla'
PASS = r'|Jn 5DJ\\7inbNniK|m@^ja&>C'

PROXY = "10.228.0.83"

URL = "http://ovh.net/files/1Mb.dat"

def get_cmd2(proxy=PROXY):
        cmd='curl -x '+proxy+':3128 -U '+USER+':\"'+PASS+'\" -m 180 -w \"%{time_total},%{http_code}\" -H \"Cache-control: private\" '+URL+' -o /dev/null -s'
        return cmd


def getVivaldiProxy():
	with simpleflock.SimpleFlock('/tmp/foolock1'):
		with open('proxy_route_table','r') as f:
			global PROXY
   			r = csv.reader(f,delimiter='\t')
			new_proxy = None
			for row in r:
				if row[5] == 'True':
					new_proxy = row[0]
					break
			PROXY = new_proxy

with open(FILE,"w") as f:
	f.write("time,speed_download,code,proxy\n")
VIVALDI_PERIOD = 10
last_vivaldi = 0
t=0
START = time()

getVivaldiProxy()

command = Popen(shlex.split(get_cmd2(PROXY)),stdout=PIPE, stderr=PIPE)
out = 0


while t < (EXP_TIME+60):
	sleep(0.9945)
	code = command.poll()
	t = time()-START
	if code is not None:
		if code==0 :
			out1, err = command.communicate()
			out = out1.split(',')[0]
			code = out1.split(',')[1]
		command = Popen(shlex.split(get_cmd2(PROXY)),stdout=PIPE, stderr=PIPE)
		with open(FILE,'a') as f:
			f.write("{0:.1f},{1},{2},{3}\n".format(t,out,code,PROXY))
		
	if (t-last_vivaldi) > VIVALDI_PERIOD:
		last_vivaldi = t
	getVivaldiProxy()

