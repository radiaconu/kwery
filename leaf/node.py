# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:09:30 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)
"""

from twisted.internet.protocol import DatagramProtocol
import json

class Node2Disp(DatagramProtocol):    
    def __init__(self):
        self.rcvd_msgs = 0
    
    def send_print(self, _msg):
        self.udpsocket.sendto(json.dumps(_msg),(self.addr, self.port))
        
import sys
sys.path.append('..')
from templates.runnable import Runnable

class Node(Runnable):
    def __init__(self, _config = None):
        self.config = _config
    
    def run(self):
        print "running node on", self.config.addr, self.config.port
        


if __name__ == '__main__':
    #from twisted.internet import reactor
    from config import Config
    localconfig = Config()

    import socket
    import time
    
    _msg = ['print', 'yo']
    udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for _ in range(1):
        for i in range(100000):
            #udpsocket.sendto(json.dumps(_msg),(localconfig.connectDispAddr, localconfig.connectDispPort+1))
            udpsocket.sendto(json.dumps(_msg),(localconfig.connectDispAddr, localconfig.connectDispPort+1))
        
    
    #
    #node = Rect()
    #node.run
    
    #reactor.run()