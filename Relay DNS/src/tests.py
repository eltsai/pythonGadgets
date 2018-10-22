#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#tests

def localTable(ip_list):
    '''
    :type ip_list: str
    :rtype: dict
    '''
    try:
        print('::Scanning local ip cache')
        ip_file = open(ip_list, 'r')
    except:
        print('::Error: can not open file:', ip_list)
        return
    ip_table = {}
    for line in ip_file.readlines():
        if line == '\n':
            continue
        ip = line.split(' ')[0]
        name = line.split(' ')[1][:-1]
        ip_table[name] = ip
    return ip_table


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
