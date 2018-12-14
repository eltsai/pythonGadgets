#!/usr/bin/python3
#coding=utf-8
#__author__ = 'E-Tsai'
#tests

from Server import*

def error():
    """
    err prompt msg
    """
    print(":: Wrong cmd, please try again")

def checkIP(s):
        """
        :type s: str
        :rtype: bool
        """
        if s.count(".") != 3:
            return False
        num = ''
        for i in range(len(s)):
            if s[i] == '.':
                if num and (num == '0' or num[0] != '0') and int(num) < 256:
                    num = ''
                else:
                    return False
            elif s[i].isdigit():
                num += s[i]
            else:
                return False
        return num and (num == '0' or num[0] != '0') and int(num) < 256

def testL1():
    """
    debug level 1
    """
    #print(":: Entering debug level 1...")
    server = Server((server_114, 53), 1, local_addr)
    server.run()


def testL2(pub_sev, cache_addr):
    """
    :type pub_sev, cache_addr: str
    debug level 3
    """
    
    print(":: Entering debug level 2...")
    if not pub_sev:
        server = Server((server_114, 53), 2, local_addr)
    else:
        print(":: Selected public server: {}\n:: Selected local cache: {}".format(pub_sev, cache_addr))
        server = Server((pub_sev, 53), 2, cache_addr)

    server.run()

def testL3(pub_sev):
    """
    debug level 3
    """
    if not  pub_sev:
        print(":: Entering debug level 3...")
        server = Server((server_114, 53), 3, local_addr)
        
    else:
        print(":: Selected public server:", pub_sev)
        print(":: Entering debug level 3...")
        server = Server((pub_sev, 53), 3, local_addr)
    server.run()