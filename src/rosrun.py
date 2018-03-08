#!/usr/bin/env python

import roslib; roslib.load_manifest('cloud_ros')
import rospy
from cloud_ros.srv import *
from pySpacebrew.spacebrew import Spacebrew
from std_msgs.msg import String
import rosgraph.masterapi
import time
import os
import subprocess
import threading

def rosrunFunctions(command, brew):
	global stop_
	stop_ = False

	commandSplit = command.split(" ")
	
	if len(commandSplit) == 3:
		data = {'commandRos':'rosrun', 'function':'rosrun', 'action':'send', 'package':commandSplit[1], 'executable':commandSplit[2], 'parameters':''}
		brew.publish("Publisher", data)
		rospy.logwarn("Command sent = "+command)
	elif len(comandoSplit) == 4:
		data = {'commandRos':'rosrun', 'function':'rosrun', 'action':'send', 'package':commandSplit[1], 'executable':commandSplit[2], 'parameters':commandSplit[3]}
		brew.publish("Publisher", data)
		rospy.logwarn("Command sent = "+command)
	else:
		rospy.logwarn("Incorrect command syntax")	
	
'''INICIO ROSRUN'''

def rosrun(brew, package, executable, parameters):

	aux = parameters.split("@")
	parameters = aux[0]
	for i in range(1, len(aux)-1):
		parameters+=":="+aux[i] 

	global proc
	if(parameters != ''):
		proc = subprocess.Popen(["rosrun " +package +" "+ executable+" "+parameters], stdout=subprocess.PIPE, shell=True)
	else:
		proc = subprocess.Popen(["rosrun " +package +" "+ executable], stdout=subprocess.PIPE, shell=True)

	data = {'datum':datum, 'title':'Package running ', 'action':'receive'}

	brew.publish("Publisher", data)

	thread1 = myThread(1, "Thread-1", 1)
	thread1.start()

'''FIM ROSRUN'''

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):

	global proc

        print "Starting " + self.name
	(datum, err) = proc.communicate()
        print "Exiting " + self.name


