#!/bin/bash

# This is a script to ping all or one kvm spider's by number. 
# Author: davidc
# Version 2.1; Release date 12/4/19
# Basic syntax to run output of script is:
# If no arguments are ran, then all KVM's are pinged that 
# are in the data center specified.
# If an argument is specified with a number, then ping that KVM.

# Variables for the kvm number and kvm list.
number=$1
list='listKVMs.txt'

# Variables for the kvm names.
firstKVM=1
lastKVM=44

# Variable for the data center; A for West and C for East.
dataCenter="(A)"

# Used to repeat the refresh rate of the KVM pings.
function repeatRefresh(){
# Variable used to refresh the time in minutes and seconds
refreshMinutes=7
refreshSeconds=0
}

# Function to check if kvm is in the data center specified
# And also check if kvm is pinging or not.
function kvmDC(){

  if [[ $line == *"$dataCenter"* ]]; then

   # Variables to cut the IP only from the $list string.
   kvmIPs=${line%-*}
   kvmIPs=${kvmIPs##*=}

    if ping -q -c 1 -W 1 $kvmIPs >/dev/null; then

     if [[ $line != *"ded"* ]] && [[ $line != *"cc"* ]]; then
      echo -e "$line = \e[1;33mUP\e[0m"
     else
      echo -e "$line = \e[1;32mUP\e[0m"   
     fi

    else

     if [[ $line != *"ded"* ]] && [[ $line != *"cc"* ]]; then
       echo -e "$line = \e[1;33mDOWN\e[0m"
     else
     echo -e "$line = \e[1;31mDOWN\e[0m"
     fi

    fi

  elif [[ $line != *"$dataCenter"* ]]; then
   echo -n ""
  else
    echo "$line IS NOT IN THIS DATA CENTER"
  fi
}

# Conditions to check whether an argument is called.
if [[ $# -eq 0 ]]; then
while true
do
 clear
 repeatRefresh
 echo; echo "PINGING ALL KVM'S FROM $PWD/$list IN THIS DATA CENTER."
 echo ""
  while read line
  do
    kvmDC
  done < $list
 echo ""
 sleep 1
 tput sc
 while [ $refreshMinutes -ge 0 ]; do
  while [ $refreshSeconds -ge 0 ]; do
   #tput rc
   echo -ne "REFRESHING IN $refreshMinutes MINUTES AND $refreshSeconds SECONDS\r"
   echo "PRESS <ctrl-c> TO EXIT"
   tput rc
   refreshSeconds=$((refreshSeconds-1))
   sleep 1
  done
  refreshSeconds=59
  refreshMinutes=$((refreshMinutes-1))
 done
done

elif [[ $number -ge $firstKVM ]] && [[ $number -le $lastKVM ]]; then
 line=$( grep kvmspider$number $list | head -1 )
 kvmDC
else
 echo "ERROR IN ARGUMENT OR KVM LIST TEXT FILE."
fi


