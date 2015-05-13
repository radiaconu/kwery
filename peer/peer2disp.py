# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 11:39:27 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Peer2Diaspatcher communication
 * one 2 one
 * bi-directional
"""
from templates.node2node import Node2Node, Node2Node_to, Node2Node_from

class Peer2Disp_from(Node2Node_from):
    def received_insert(self, _id, _value, _proxy_host):
        """ Structure: 'insert', _id, _value, (_proxy_addr, _proxy_port) """
        self.peer.handle_insert(_id, _value, _proxy_host)
        
    def received_get(self, _query_id, _min_value, _max_value, _proxy_host):
        """ Structure: 'get', _query_id, _min_value, _max_value, (_proxy_addr, _proxy_port) """
        self.peer.handle_get(_query_id, _min_value, _max_value, _proxy_host)


class Peer2Disp_to(Node2Node_to):
    def send_update(self):
        """ Structure: 'update', (_addr, _port), _value """
        coverage = self.peer.index.coverage()
        barycenter = self.peer.index.barycenter()
        object_load = self.peer.index.load()
        #_value = (coverage, barycenter)
        
        msg = ('update', coverage, barycenter, object_load, self.host)
        self._send(msg, (self._to_addr, self._to_port))
        
    def send_transfer(self, _id, _value, _proxy_host):
        """ TODO: To be tested Structure: 'update', (_addr, _port), _value """
        msg = ('transfer', _id, _value, _proxy_host)
        self._send(msg, (self._to_addr, self._to_port))
      

class Peer2Disp(Node2Node, Peer2Disp_to, Peer2Disp_from):
    
    class DispObject:
        def __init__(self, _addr, _port):
            self.addr = _addr
            self.port = _port
    
    
    def __init__(self, _peer):
        self.peer = _peer
        self._to_addr = _peer.config.connectDispAddr
        self._to_port = _peer.config.connectDispPort
                
        self._from_addr = _peer.config.listenDispAddr 
        self._from_port = _peer.config.listenDispPort
        self.host = (self._from_addr, self._from_port)
        
        Node2Node.__init__(self)