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
        
        self.loop_send_update = LoopingCall(self.peer2disp.send_update)
        self.loop_send_update.start(self.config.UPDATE_INTERVAL)

    def handle_put(self, _id, _value, _proxy_host):
        print "put", _id
        self.index.put(_id, _value)
        self.id2proxy[_id] = _proxy_host
        self.peer2proxy.send_notification([_id], _proxy_host)
    
    def handle_get(self, _query_id, _min_value, _max_value, _proxy_host):
        result = self.index.get(_min_value, _max_value)
        self.peer2proxy.send_query_answer(_query_id, result, _proxy_host)
        
if __name__ == '__main__':
    peer = Peer()
    peer.run()
    
    _msg = ['print', 'yo']
       
    reactor.run()