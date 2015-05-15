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

from proxy2object_kolntrace import Proxy2Object

import sys
sys.path.append('..')
from templates.runnable import Runnable

from twisted.internet.task import LoopingCall

import time

class Proxy(Runnable):
    def __init__(self, _config_file='configProxyDefault.cfg'):
        # singleton 
        self.PROXY = self
        self.config = ConfigProxy(_file=_config_file)
    
    def run(self): 
        # effectively open connections
        self.proxy2disp = Proxy2Disp(self)
        self.proxy2peer = Proxy2Peer(self)
        self.proxy2object = None 
        #self.proxy2proxy = Proxy2Proxy(self)
        
        # data management
        self.objects = dict()
        self.id2peer = dict()
        self.id2last_notif = dict()
        self.queries = dict() # id -> objects
        # TODO: management of recent removals that continue to receive updates
        
        
        self.loop_cleanup = LoopingCall(self.cleanup)
        self.loop_cleanup.start(self.config.UPDATE_INTERVAL)
    
    def handle_put(self, _id, _value):
        """ From object """        
        _peer_host = self.id2peer.get(_id)
        if _peer_host:
            self.proxy2peer.send_put(_id, _value, _peer_host)
        else:
            self.proxy2disp.send_insert(_id, _value)
         
    def handle_query(self, _query_id, _min_value, _max_value):
        """ From client TODO """
        pass
    
    def handle_remove(self, _id):
        #if self.objects.get(_id):
        #    self.proxy2peer.send_remove()
            self.objects.pop(_id, None)
            self.id2peer.pop(_id, None)
            
    def handle_query_answer_peers(self, _query_id, _objects):
        """ From peer(s) """
        self.queries[_query_id] = _objects
    
    def handle_notification(self, _ids, _peer_host):
        """ From peer """
        
        for _id in _ids:
            if self.id2peer.get(_id) is not _peer_host:
                print "notif", _id, self.id2peer.get(_id), _peer_host
            self.id2peer[_id] = _peer_host
            self.id2last_notif[_id] = time.time()
    
    def cleanup(self):
        now = time.time()
        for _id, _last_notif in self.id2last_notif.items():
            if now-_last_notif > 2:
                print 'cleanup', _id
                self.id2peer.pop(_id, None)
                self.id2last_notif.pop(_id, None)
                #self.handle_remove(_id)
                
    def generate_points(self):
        # generate some points:
        print "generate some points "
        from random import random
        for _id in range(100):
            self.proxy2disp.send_insert(_id, (random(), random()))
        print "done"
        
if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    
    argParser = ArgumentParser(description='The Proxy.')
    argParser.add_argument('--c', type=FileType('rw'), default="configProxyDefault.cfg", help='the configuration file, default configProxyDefault.cfg')
    
    args = argParser.parse_args()
    
    print args.c.name
    proxy = Proxy(args.c.name)
    proxy.run()
    proxy.proxy2object = Proxy2Object(proxy)
    #proxy.generate_points()
    reactor.run()