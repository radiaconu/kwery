# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 14:13:09 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Proxy2Peer communication: 
 * one 2 many
 * bi-directional : send put, receive query answer
"""
import sys
sys.path.append('..')

from templates.node2node import Node2Node, Node2Node_to, Node2Node_from

class Proxy2Peer_from(Node2Node_from):   
    def received_query_answer(self, _query_id, _objects):
        """ Structure: 'answer', _query_id, [( _id, _value)] """
        self.proxy.handle_query_answer_peers(_query_id, _objects)
    
    def received_notification(self, _ids, _peer_host):
        """ Structure: 'notification', _ids, (_peer_addr, _peer_port) """
        #print " here"
        self.proxy.handle_notification(_ids, _peer_host)
    
class Proxy2Peer_to(Node2Node_to):
    def send_put(self, _id, _value, _peer):
        """ Structure: 'put', _id, _value, (_proxy_addr, _proxy_port) """
        msg = ('put', _id, _value, self.host)
        self._send(msg, _peer)
    
        
class Proxy2Peer(Node2Node, Proxy2Peer_from, Proxy2Peer_to):
    def __init__(self, _proxy):
        self.proxy = _proxy
        
        self._from_addr = _proxy.config.listenPeerAddr
        self._from_port = _proxy.config.listenPeerPort
        self.host = (self._from_addr, self._from_port)
        Node2Node.__init__(self)