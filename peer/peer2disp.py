# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 11:39:27 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Proxy2Diaspatcher communication
"""
from templates.node2node import Node2Node, Node2Node_to


class Peer2Disp_to(Node2Node_to):
    def send_update(self, _id, _value):
        msg = ('update', self._to_addr, self._to_port, _id, _value)
        self._send(msg, (self._to_addr, self._to_port))
        

class Peer2Disp(Node2Node, Peer2Disp_to):
    def __init__(self, _peer):
        self.peer = _peer
        self._to_addr = _peer.config.connectDispAddr # unimportant for now
        self._to_port = _peer.config.connectDispPort
        
        self._from_addr = _peer.config.listenDispAddr 
        self._from_port = _peer.config.listenDispPort
        
        Node2Node.__init__(self)