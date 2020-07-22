#!/usr/bin/env python
# This Python script is for pinging all of the KVM's in our data centers.
# Author: davidc
# Version: 1.1
# Release date: 1/16/20

# You might have to install the natsort module with pip.
# pip install natsort

import os, sys, time, natsort
from collections import OrderedDict

# Variables used in the description of the kvm location.
deds = "ded"
ccs = "cc"

# This function is used to define the refresh time.
def refreshTime(minute, second):
 minute = 5
 second = 0

 return minute, second

# This function is used to define the state of the KVM's.
def kvmState():
 for kvms in natsort.natsorted(kvmList):
# Splitting the items for IP's and locations.
  kvmIPs, kvmLocations = kvmList[kvms].split("=")
# Variable to evalute a KVM connection. 
  kvmPinged = os.system("ping -c 1 " + kvmIPs + ">/dev/null")

  if kvmPinged == 0:

   if deds in kvmLocations or ccs in kvmLocations:
    print(kvms + "=" + kvmList[kvms] + " = " + "[\x1b[1;32;40m UP \x1b[0m]")
   else:
    print(kvms + "=" + kvmList[kvms] + " = " + "[\x1b[1;33;40m UP \x1b[0m]")

  else:

   if deds in kvmLocations or ccs in kvmLocations:
    print(kvms + "=" + kvmList[kvms] + " = " + "[\x1b[1;31;40m DOWN \x1b[0m]")
   else:
    print(kvms + "=" + kvmList[kvms] + " = " + "[\x1b[1;33;40m DOWN \x1b[0m]")

# This is a dictionary for the KVM names, their IP addresses, and locations.
# Mark the KVM's string in the dictionary in this format:
# "kvmspiderNUMBER": "KVMIPADDRESS=SERVERNAME/LOCATION/PSC"

lastUpdate = "6/25/20" # Modify this variable with the date when the kvmList is updated.

kvmList = {
 "kvm1": "8.8.8.8=ded4555/cab41/pdu4",
 "kvm2": "8.8.8.8=cc5008/cab88/pdu84",
 "kvm3": "8.8.8.8=server58/cab42/pdu24",
 "kvm4": "8.8.8.8=cab23/cab32/pdu23"
}

# Try/Catch block; CTRL+C to exit out.
try:
 while True:
  os.system("clear")
  minute, second = refreshTime(0, 0)
  print
  print("PINGING ALL KVM'S IN ALL DATA CENTERS. LAST UPDATED ON " + lastUpdate)
  print
  kvmState()
  print
  # This loop is used to setup the refresh state of the program.
  while minute >= 0:
   while second >= 0: 
    print '\rREFRESHING IN %s MINUTES AND %s SECONDS. PRESS <ctrl-c> TO EXIT. ' % (minute, second),
    sys.stdout.flush()
    second = second - 1
    time.sleep(1)
   second = 59
   minute = minute - 1
except KeyboardInterrupt:
 print
 print('EXITING')

