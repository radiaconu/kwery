# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:44:17 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Diaspatcher2Proxy communication: 
 * one 2 many
 * uni-directional, only receive inserts & queries 
"""

from templates.node2node import Node2Node, Node2Node_from

class Disp2Proxy_from(Node2Node_from):
    
    def received_insert(self, _id, _value, _proxy):
        """ Structure: 'insert', _id, _value, (_proxy_addr, _proxy_port) """
        self.disp.disp2peer.select_and_insert(_id, _value, _proxy)
        
        
class Disp2Proxy(Node2Node, Disp2Proxy_from):
    def __init__(self, _disp):       
        
        self.disp = _disp
        self._from_addr = _disp.config.listenProxyAddr # unimportant for now
        self._from_port = _disp.config.listenProxyPort
         
        self._all = dict()
        Node2Node.__init__(self)
