# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 11:39:27 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Proxy2Diaspatcher communication
"""
import sys
sys.path.append('..')

from templates.node2node import Node2Node, Node2Node_to


class Proxy2Disp_to(Node2Node_to):
    def send_insert(self, _id, _value):
        msg = ('insert', self._to_addr, self._to_port, _id, _value)
        self._send(msg, (self._to_addr, self._to_port))
        

class Proxy2Disp(Node2Node, Proxy2Disp_to):
    def __init__(self, _proxy):
        self.proxy = _proxy
        self._to_addr = _proxy.config.connectDispAddr # unimportant for now
        self._to_port = _proxy.config.connectDispPort
        
        Node2Node.__init__(self)