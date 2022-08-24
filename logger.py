from datetime import *

time = datetime.now()

def timeStamp(fd):
	time = datetime.now()

	if(fd==None):
		return time.strftime('%H:%M => ')
	else:
		fd.write(time.strftime('%H:%M => '))

def dateStamp(fd):
	time = datetime.now()
	fd.write(time.strftime('%Y.%m.%d '))

def datetimeStamp(fd):
	time = datetime.now()
	fd.write(time.strftime('Date %Y.%m.%d, Time %H:%M\n'))