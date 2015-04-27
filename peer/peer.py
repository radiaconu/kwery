# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:09:30 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)
"""
    
from config import Config
from peer2disp import Peer2Disp
from peer2proxy import Peer2Proxy

import sys
sys.path.append('..')
from templates.runnable import Runnable

class Node(Runnable):
    def __init__(self, _config = None):
        self.config = _config
    
    def run(self):
        self.peer2proxy = Peer2Proxy()
        self.peer2disp = Peer2Disp()
        


if __name__ == '__main__':
    #from twisted.internet import reactor
    localconfig = Config()

    import time
    
    _msg = ['print', 'yo']
    udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for _ in range(1):
        for i in range(100000):
            #udpsocket.sendto(json.dumps(_msg),(localconfig.connectDispAddr, localconfig.connectDispPort+1))
            udpsocket.sendto(json.dumps(_msg),(localconfig.connectDispAddr, localconfig.connectDispPort+1))
        
    reactor.run()