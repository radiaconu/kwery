# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 00:32:07 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Leaf 2 all Proxy communication. *** one 2 many ***
"""
from templates.node2node import Node2Node, Node2Node_to, Node2Node_from

class Leaf2Proxy_to(Node2Node_to):
    pass

class Leaf2Proxy_from(Node2Node_from):
    pass

class Leaf2Proxy(Node2Node):
    
    def __init__(self, _leaf):
        self.leaf = _leaf
        
        self._from_addr = _leaf.config.listenDispAddr 
        self._from_port = _leaf.config.listenDispPort
        
        Node2Node.__init__(self)