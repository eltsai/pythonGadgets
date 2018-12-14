#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#read command
from Debug import *


if __name__ == '__main__':

    print(':: This is a relay DNS')
    print(':: Enter: \'dnsrelay [-d][-dd] [dns-server-ipaddr] [filename]\' to obtain ip')
    print(':: Enter: ctrl + c to stop program ')
    ip_list = 'dnsrelay.txt'
    #ip_list = 'new.txt'
    # dns_server = input('DNS server: ')
    while 1:
        command = input('> ')
        if not command:
            testL1()
        command_seg = command.split(' ')
        
            





        if command_seg[0] != 'dnsrelay':
            error()
        # test 2
        elif len(command_seg) > 1 and command_seg[1] == '-d':
            if len(command_seg) == 2:
                testL2("", "")
            # wrong commond, invalid ip 
            elif len(command_seg) != 4 or not checkIP(command_seg[2]):
                error()
            else:
                testL2(command_seg[2], command_seg[3])
        #test3
        elif len(command_seg) > 1 and command_seg[1] == '-dd':
            if len(command_seg) == 2:
                testL3("")
            if checkIP(command_seg[2]) and len(command_seg) == 3:
                testL3(command_seg[2])
            else:
                error()
        # test1
        else:
            testL1()
    print(':: byeeee :D')
    
