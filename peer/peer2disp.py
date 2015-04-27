# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 11:39:27 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Peer2Diaspatcher communication
 * one 2 one
 * bi-directional
"""
from templates.node2node import Node2Node, Node2Node_to, Node2Node_from


class Peer2Disp_to(Node2Node_to):
    def send_update(self):
        """ Structure: 'update', (_addr, _port), _value """
        _value = self.peer.index.aggregate()
        msg = ('update', (self.peer.config.listenDispAddr, self.peer.config.listenDispPort), _value)
        self._send(msg, (self._to_addr, self._to_port))
        
    def send_transfer(self, _id, _value):
        msg = ('transfer',self._to_addr, self._to_port, _id, _value)
        self._send(msg, (self._to_addr, self._to_port))
    
      
class Peer2Disp_from(Node2Node_from):
    def received_insert(self, _id, _value, (_proxy_addr, _proxy_port)):
        """ Structure: 'insert', _id, _value, (_proxy_addr, _proxy_port) """
        print "receive_insert", _id
        self.peer.index.put(_id, _value)


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
        
        Node2Node.__init__(self)