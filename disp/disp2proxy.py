# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:44:17 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Diaspatcher2Proxy communication: ***one 2 many, receive only***
"""

from templates.node2node import Node2Node, Node2Node_from

class Disp2Proxy_from(Node2Node_from):
    
    def received_insert(self, _host, _port, _id, _value):
        if not self._all.get( (_host, _port) ):
            print "new proxy"
            self._all[(_host, _port)] = _value
            
        print "insert", _host, _port, _id, _value
        
        
class Disp2Proxy(Node2Node, Disp2Proxy_from):
    def __init__(self, _disp):       
        
        self.disp = _disp
        self._from_addr = _disp.config.listenProxyAddr # unimportant for now
        self._from_port = _disp.config.listenProxyPort
         
        self._all = dict()
        Node2Node.__init__(self)