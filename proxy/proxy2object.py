# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:03:08 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)
"""

class Proxy2Object_from(Node2Node_from):
    pass

class Proxy2Object_to(Node2Node_to):
    pass

class Proxy2Object(Node2Node, Proxy2Object_from, Proxy2Object_to):
    def __init__(self, _proxy):
        self.proxy = _proxy
        
        self._from_addr = _proxy.config.listenObjectAddr
        self._from_port = _proxy.config.listenObjectPort
        self.host = (self._from_addr, self._from_port)
        Node2Node.__init__(self)