import os
import time
import cv2


def send2pd(message=''):
	# Send a message to pd
	os.system("echo '" + message + "' | pdsend 3000")

def audioOn():
	message = '0 1;'
	send2pd(message)

def audioOff():
	message = '0 0 ;'
	send2pd(message)

def setVolume(vol = 50):
	message = '1 ' + str(vol) + ' ;'
	send2pd(message)

setVolume(0)

audioOn()


setVolume(1)
time.sleep(5)
setVolume(0)
time.sleep(1)
audioOff()

print "done";