from subprocess import PIPE, Popen
import shlex

USER = 'david.pinilla'
PASS = r'|Jn 5DJ\\7inbNniK|m@^ja&>C'

def get_cmd(proxy):
        cmd='curl -x '+proxy+':3128 -U '+USER+':\"'+PASS+'\" -m 180 -w %{time_starttransfer} www.google.com -o /dev/null -s'
        return cmd

def queryProxy(proxy):
	command = Popen(shlex.split(get_cmd(proxy)),stdout=PIPE, stderr=PIPE)
	return command

