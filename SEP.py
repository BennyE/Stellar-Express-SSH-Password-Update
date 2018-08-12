#!/usr/bin/env python3

#
# Imports
#
import sys
import argparse
import re
from getpass import getpass

# SSH
# In this release, paramiko is a mandatory requirement
try:
    import paramiko
except ImportError as ie:
    print(ie)
    sys.exit("Please install paramiko!")

# This implements our own WarningPolicy, as we know that the host keys are unknown.
class NoWarningPolicy (paramiko.client.MissingHostKeyPolicy):
    pass

def find_cluster_access_points(primary_virtual_controller_ip, sshpassword):
    client = paramiko.client.SSHClient()
    print("Note: This tool doesn't validate SSH host keys today! Setting Paramiko WarningPolicy accordingly.")
    client.set_missing_host_key_policy(NoWarningPolicy)
    try:
        client.connect(hostname=primary_virtual_controller_ip, username="support", password=sshpassword)
    except paramiko.ssh_exception.AuthenticationException as ae:
        print(ae)
        sys.exit("SSH password incorrect!")
    stdin, stdout, stderr = client.exec_command("show_cluster")
    aps = stdout.read()
    aps = aps.decode("UTF-8")
    aps = aps.splitlines()
    client.close()
    return aps

def build_access_point_list(aps):
    aplist = []
    for ap in aps:
        candidate = ap.split()
        if candidate[0] == "mac":
            continue
        if candidate[3] != "3":
            print("Stellar {0} with MAC address {1} and IP address {2} is not online and the password will NOT be changed!".format(candidate[6], candidate[0], candidate[1]))
            continue
        aplist.append(ap.split())
    print("\nThis is the list of Stellar Express APs on which the password will be updated:")
    for ap in aplist:
        print("Stellar {0} with MAC address {1} and IP address {2}".format(ap[6], ap[0], ap[1]))
    return aplist

def set_new_ssh_password(aps, sshpassword, new_ssh_password):
    for ap in aps:
        print("Attempting to set password on Stellar {0} with MAC/IP {1} / {2}".format(ap[6], ap[0], ap[1]))
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(NoWarningPolicy)
        try:
            client.connect(hostname=ap[1], username="support", password=sshpassword)
        except paramiko.ssh_exception.AuthenticationException as ae:
            print(ae)
            print("Old SSH password incorrect! Moving on to next AP ...")
            client.close()
            continue
        channel = client.get_transport().open_session()
        channel.get_pty()
        channel.setblocking(1)
        channel.exec_command("ssudo passwd")

        while channel.active:
            if channel.recv_ready():
                stdout = channel.recv(4096)
                if re.search("[Pp]assword:", stdout.decode("UTF-8")):
                    channel.send(new_ssh_password + "\n")

                elif re.search("for support changed by root", stdout.decode("UTF-8")):
                    print("The password was updated successfully on Stellar {0} MAC / IP {1} / {2}".format(ap[6], ap[0], ap[1]))
                    channel.active = 0
                    channel.close()

                elif re.search("password for support is unchanged", stdout.decode("UTF-8")):
                    print("The password was overwritten with the previous on Stellar {0} MAC / IP {1} / {2}".format(ap[6], ap[0], ap[1]))
                    channel.active = 0
                    channel.close()
        client.close()

def main():
    print("\nStellar Wireless Express password change tool for \"support\" user")
    print("Written by Benny Eggerstedt in 2018")
    print("This is free software not provided/shipped by Alcatel-Lucent Enterprise. Use it at your own risk!\n")

    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--primary-virtual-controller-ip", help="IPv4 address of the Primary Virtual Controller (PVC) of the Stellar Express cluster", required=True)
    args = parser.parse_args()

    print("You're about to connect via SSH to {0}".format(args.primary_virtual_controller_ip))
    sshpassword = getpass("Please enter the current \"support\" user password: ")

    aps = find_cluster_access_points(args.primary_virtual_controller_ip, sshpassword)
    aps = build_access_point_list(aps)

    new_ssh_password = getpass("\nPlease enter the new password for the \"support\" user: ")
    validate_new_ssh_password = getpass("Please type the password again: ")
    if new_ssh_password == validate_new_ssh_password:
        pass
    else:
        sys.exit("The passwords don't match!")

    set_new_ssh_password(aps, sshpassword, new_ssh_password)

    print("Work is done!")

if __name__ == "__main__":
    main()