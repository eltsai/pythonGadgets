#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#read command
from Debug import *
import argparse

parser = argparse.ArgumentParser(description='This is a relay DNS')
parser.add_argument("dnsrelay", nargs='?')
parser.add_argument("-d", help="Enter debug mode level 2", action="store_true")
parser.add_argument("-dd", help="Enter debug mode level 3", action="store_true")
args, unknown = parser.parse_known_args()
#print(args, unknown)



if __name__ == '__main__':

    if not args.dnsrelay:
        testL1(0)
    elif not args.d and not args.dd:
        testL1(1)
    elif args.d:
        if len(unknown) == 0:
            testL2("", "")
        elif len(unknown) == 2:
            testL2(unknown[0], unknown[1])
    elif args.dd:
        if len(unknown) == 0:
            testL3("")
        elif len(unknown) == 1:
            testL3(unknown[0])
    error()

    
