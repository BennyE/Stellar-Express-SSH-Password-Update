# Stellar-Express-SSH-Password-Update
Small tool to allow the update of the "support" user password for a given cluster

# Usage (-h)
```
$ python3 SEP.py -h

Stellar Wireless Express password change tool for "support" user
Written by Benny Eggerstedt in 2018
This is free software not provided/shipped by Alcatel-Lucent Enterprise. Use it at your own risk!

usage: SEP.py [-h] -ip PRIMARY_VIRTUAL_CONTROLLER_IP

optional arguments:
  -h, --help            show this help message and exit
  -ip PRIMARY_VIRTUAL_CONTROLLER_IP, --primary-virtual-controller-ip PRIMARY_VIRTUAL_CONTROLLER_IP
                        IPv4 address of the Primary Virtual Controller (PVC)
                        of the Stellar Express cluster
 ```
 
 # Example output for a Stellar Express cluster with two APs
 
 ```
$ python3 SEP.py -ip 192.168.15.104

Stellar Wireless Express password change tool for "support" user
Written by Benny Eggerstedt in 2018
This is free software not provided/shipped by Alcatel-Lucent Enterprise. Use it at your own risk!

You're about to connect via SSH to 192.168.15.104
Please enter the current "support" user password: 
Note: This tool doesn't validate SSH host keys today! Setting Paramiko WarningPolicy accordingly.

This is the list of Stellar Express APs on which the password will be updated:
Stellar AP-18:E0 with MAC address 34:e7:0b:00:18:e0 and IP address 192.168.15.104
Stellar AP-12:70 with MAC address 34:e7:0b:00:12:70 and IP address 192.168.15.100

Please enter the new password for the "support" user: 
Please type the password again: 
Attempting to set password on Stellar AP-18:E0 with MAC/IP 34:e7:0b:00:18:e0 / 192.168.15.104
The password was updated successfully on Stellar AP-18:E0 MAC / IP 34:e7:0b:00:18:e0 / 192.168.15.104
Attempting to set password on Stellar AP-12:70 with MAC/IP 34:e7:0b:00:12:70 / 192.168.15.100
The password was updated successfully on Stellar AP-12:70 MAC / IP 34:e7:0b:00:12:70 / 192.168.15.100
Work is done!
```
