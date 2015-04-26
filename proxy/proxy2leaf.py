# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 14:13:09 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Proxy2Leaf communication: ***one 2 many***
"""
import sys
sys.path.append('..')

from templates.node2node import Node2Node, Node2Node_to, Node2Node_from


class Proxy2Leaf(Node2Node):
    def __init__(self, _proxy):
        self.proxy = _proxy
        self.addr = _proxy.config.connectDispAddr
        self.port = _proxy.config.connectDispPort
        
        self._from = Proxy2Leaf_from()
        self._to = Proxy2Leaf_to()
        self._all = dict()

class Proxy2Leaf_to(Node2Node_to):
    def send_insert(self, _id, _value):
        msg = ('insert', self.proxy.config.listenLeafAddr, self.proxy.config.listenLeafPort, _id, _value)

        self._send(msg, self.proxy2disp)


class Proxy2Leaf_from(Node2Node_from):
        
    def from_leaf_notiffication(self, _host, _port, _id, _msg):
        print "from", _host, _port
        print "notiffication", _id, _msg
        
