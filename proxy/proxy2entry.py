# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:30:04 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Proxy2Entry communication
 * one(many) 2 one
 * bi-directional: send regular updates; receive clinet joins
 
"""
from templates.node2node import Node2Node, Node2Node_to, Node2Node_from

class Proxy2Entry_from(Node2Node_from):
    
    def received_join(self, _client_host):
        """ Structure: 'join', (_client_addr, _client_port)"""
        self.peer.handle_join(_client_host)


class Proxy2Entry_to(Node2Node_to):
    def send_update(self):
        """ Structure: 'update', (_proxy_addr, _proxy_port), _value(*) """
        object_load = len(self.proxy.objects)
        sent_received = (self.proxy.proxy2peer.get_sent(), self.proxy.proxy2peer.get_received(),\
                        self.proxy.proxy2disp.get_sent(), self.proxy.proxy2disp.get_received())
        cpu_load = (0, 0) # TODO: 
        
        msg = ('update', self.host, object_load, cpu_load, sent_received)
        self._send(msg, (self._to_addr, self._to_port))
        

class Proxy2Entry(Node2Node, Proxy2Entry_to, Proxy2Entry_from):
    
    class DispObject:
        def __init__(self, _addr, _port):
            self.addr = _addr
            self.port = _port