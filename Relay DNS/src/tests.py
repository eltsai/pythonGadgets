#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#tests

from Server import*

def debug():
    print('::This is a relay DNS')
    print('::Enter: \'dnsrelay [-d][-dd] [dns-server-ipaddr] [filename]\' to obtain ip')
    print('::Enter: \'stop\' to stop program ')
    ip_list = 'dnsrelay.txt'
    #ip_list = 'new.txt'
    dns_server = input('DNS server: ')
    while 1:
        command = input('> ')
        if command ==  'stop':
            break
        command_seg = command.split(' ')
        if not command_seg:
            continue
        elif command_seg[0] != 'dnsrelay':
            print('::command not found')
        elif len(command_seg) > 1 and command_seg[1] == '-d':
            testL2()
        elif len(command_seg) > 1 and command_seg[1] == '-dd':
            testL3()
        else:
            for item in command_seg[1:]:
                if '.txt' in item:
                    ip_list = item
                else:
                    dns_server = item
            test(dns_server, ip_list)
    print('::byeeee :D')



def test(dns_server, ip_list):
    ip_cache = localTable(ip_list)
    while 1:
        name = input('search: ')
        if name == 'stop':
            break
        if name in ip_cache:
            if ip_cache[name] == '0.0.0.0':
                print('::Error: domain does not exist.')
            else:
                print('::',name,'ip:', ip_cache[name])
    print('::Test level-1 stopped')
