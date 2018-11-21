#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#read command
from tests import *


if __name__ == '__main__':

    print('::This is a relay DNS')
    print('::Enter: \'dnsrelay [-d][-dd] [dns-server-ipaddr] [filename]\' to obtain ip')
    print('::Enter: \'stop\' to stop program ')
    ip_list = 'dnsrelay.txt'
    #ip_list = 'new.txt'
    # dns_server = input('DNS server: ')
    while 1:
        command = input('> ')
        if command ==  'stop':
            break
        command_seg = command.split(' ')
        if not command_seg:
            continue
        elif command_seg[0] != 'dnsrelay':
            error()
        elif len(command_seg) > 1 and command_seg[1] == '-d':
            if checkIP(command_seg[2]) and ".txt" in command_seg[3]:
                testL2(command_seg[2], command_seg[3])
            else:
                error()
        elif len(command_seg) > 1 and command_seg[1] == '-dd':
            if checkIP(command_seg[2]):
                testL3(command_seg[2])
            else:
                error()
        else:
            testL1()
    print('::byeeee :D')
    
