# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:09:30 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

TODO: put constans in config loading
TODO: proxies are in dict. all object params are in disct. shameful.
"""
INTERVAL = 2
from config_peer import ConfigPeer
from peer2disp import Peer2Disp
from peer2proxy import Peer2Proxy

from index import LocalIndex as Index

import sys
sys.path.append('..')
from templates.runnable import Runnable

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import time, os

class Peer(Runnable):
    def __init__(self, _config_file = 'configPeerDefault.cfg'):
        # singleton
        Peer.PEER = self
        self.config = ConfigPeer(_file= _config_file)
    
    def run(self):
        self.peer2proxy = Peer2Proxy(self)
        self.peer2disp = Peer2Disp(self)
        
        self.index = Index()
        self.id2proxy = dict() # obj id -> proxy_host
        self.id2last_update = dict() # obj id -> time
        self.id2last_insert = dict() # obj id -> time
        
        self.loop_send_update = LoopingCall(self.peer2disp.send_update)
        self.loop_send_update.start(self.config.UPDATE_INTERVAL/4)
        
        self.loop_cleanup = LoopingCall(self.cleanup)
        self.loop_cleanup.start(self.config.UPDATE_INTERVAL)
        # self.cpu_loop.start(10, now=False)
    
    def handle_insert(self, _id, _value, _proxy_host):
        print "insert", _id
        now = time.time()
        
        self.index.put(_id, _value)
        self.id2proxy[_id] = _proxy_host
        self.id2last_insert[_id] = now
        self.id2last_update[_id] = now
        self.peer2proxy.send_notification([_id], _proxy_host)

    def handle_put(self, _id, _value, _proxy_host):
        if not self.id2last_insert.get(_id):
            return
            
        now = time.time()
        put = True
        
        self.index.coverage()
        bc=self.index.get_bc()
        w = self.index.get_width()
        h = self.index.get_height()
            
        if self.index.is_indexed(_id) and not self.index.is_covered(_value) and self.index.load()>10:
            if now - self.id2last_insert[_id] > 2:
                put=False
        #elif abs(_value[0]-bc[0]) > w*.8 or abs(_value[1]-bc[1]) > h*.8:
        #    put = False
            
        if put: 
            self.index.put(_id, _value)
            self.id2proxy[_id] = _proxy_host
            self.id2last_update[_id] = now
            self.peer2proxy.send_notification([_id], _proxy_host)
        else:
            print "transfer", _id
            self.index.remove(_id)
            self.id2last_insert.pop(_id, None)
            self.id2last_update.pop(_id, None)
            self.id2proxy.pop(_id, None)
            self.peer2disp.send_transfer(_id, _value, _proxy_host)
    
    def handle_get(self, _query_id, _min_value, _max_value, _proxy_host):
        result = self.index.get(_min_value, _max_value)
        self.peer2proxy.send_query_answer(_query_id, result, _proxy_host)
        
    def cleanup(self):
        now = time.time()
        for _id, _last_update in self.id2last_update.items():
            if now-_last_update > 2:
                #print "cleanup", _id
                self.index.remove(_id)
                self.id2last_insert.pop(_id)
                self.id2last_update.pop(_id)
                self.id2proxy.pop(_id)
    
#    def cpu_time(self):
#        t = os.times()
#        pt = self.lastProcTime
#        passed = t[4]-pt[4]
#        
#        self.ticks = self.count_ticks/passed
#        #print "ticks", self.ticks, len(self.objects), len(self.localZone.objects)
#        self.count_ticks = 0
#        self.localZone.cpu = round( (t[0]+t[1]-pt[0]-pt[1])*100/passed , 2 )
#        self.lastProcTime = t
        
if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    
    argParser = ArgumentParser(description='The Peer.')
    argParser.add_argument('--c', type=FileType('rw'), default="configPeerDefault.cfg", help='the configuration file, default configPeerDefault.cfg')
    
    args = argParser.parse_args()
    
    print args.c.name
    peer = Peer(args.c.name)
    peer.run()
    
       
    reactor.run()