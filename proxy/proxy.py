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
from proxy2peer import Proxy2Peer

import sys
sys.path.append('..')
from templates.runnable import Runnable

class Proxy(Runnable):
    def __init__(self, _config_file='configProxyDefault.cfg'):
        # singleton 
        self.PROXY = self
        self.config = ConfigProxy(_file=_config_file)
    
    def run(self): 
        # effectively open connections
        self.proxy2disp = Proxy2Disp(self)
        self.proxy2peer = Proxy2Peer(self)
        #self.proxy2proxy = Proxy2Proxy(self)
        
        # data management
        self.objects = dict()
        self.queries = dict() # id -> objects
    
    def handle_query_answer_peers(self, _query_id, _objects):
        self.queries[_query_id] = _objects
        
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