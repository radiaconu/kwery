# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 20:12:48 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Proxy: hanles objects 
For now it is just a generator

Listens for the Nodes
Connects to the Disp

TODO: everything
"""
from twisted.internet import reactor
from config_proxy import ConfigProxy
from proxy2disp import Proxy2Disp
from proxy2leaf import Proxy2Leaf

import sys
sys.path.append('..')
from templates.runnable import Runnable

class Proxy(Runnable):
    def __init__(self, _config_file='configProxyDefault.cfg'):
        # singleton 
        
        self.config = ConfigProxy(_file=_config_file)
    
    def run(self):    
        # effectively open connections
        self.proxy2disp = Proxy2Disp(self)
        #self.proxy2leaf = Proxy2Leaf(self)
        #self.proxy2proxy = Proxy2Proxy(self)
        
        # data management
        self.objects = dict()
        # listening for Leaves
        #reactor.listenUDP(self.config.listenLeafPort, self.proxy2leaf)
        #print "Listening for Leaves on", (self.config.listenLeafAddr, self.config.listenLeafPort)
    
    def generate_points(self):
        # generate some points:
        print "generate some points "
        from random import random
        for _id in range(100):
            self.proxy2disp.send_insert(_id, (random(), random()))
        print "done"
        
if __name__ == '__main__':
    proxy = Proxy()
    proxy.run()
    proxy.generate_points()
    reactor.run()