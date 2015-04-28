# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 00:32:07 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Peer 2 all Proxy communication. *** one 2 many ***
"""
from templates.node2node import Node2Node, Node2Node_to, Node2Node_from

class Peer2Proxy_to(Node2Node_to):
    def send_query_answer(self, _query_id, _objects, _proxy_host):
        """ Structure: 'answer', _query_id, [( _id, _value)] """
        msg = ('answer', _query_id, _objects)
        self._send(msg, _proxy_host)

class Peer2Proxy_from(Node2Node_from):
    def received_put(self,_id, _value, _proxy_host):
        """ Structure: 'put', _id, _value, (_proxy_addr, _proxy_port) """
        self.peer.handle_put(_id, _value, _proxy_host)

class Peer2Proxy(Node2Node):
    
    def __init__(self, _peer):
        self.peer = _peer
        
        self._from_addr = _peer.config.listenProxyAddr 
        self._from_port = _peer.config.listenProxyPort
        
        Node2Node.__init__(self)