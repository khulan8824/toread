from subprocess import PIPE, Popen
import shlex
import string
import random


USER = 'david.pinilla'
PASS = r'|Jn 5DJ\\7inbNniK|m@^ja&>C'
URL = "www.google.com"

def get_cmd(proxy):
	hash1 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(50))
	url = URL+'/'+hash1
	cmd='curl -x '+proxy+':3128 -U '+USER+':\"'+PASS+'\" -m 180 -w %{time_starttransfer} '+url+' -o /dev/null -s'
	return cmd

def queryProxy(proxy):
	command = Popen(shlex.split(get_cmd(proxy)),stdout=PIPE, stderr=PIPE)
	return command

