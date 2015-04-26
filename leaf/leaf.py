# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:09:30 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)
"""
    
from config import Config
from leaf2disp import Leaf2Disp
from leaf2proxy import Leaf2Proxy

import sys
sys.path.append('..')
from templates.runnable import Runnable

class Node(Runnable):
    def __init__(self, _config = None):
        self.config = _config
    
    def run(self):
        self.leaf2proxy = Leaf2Proxy()
        self.leaf2disp = Leaf2Disp()
        


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