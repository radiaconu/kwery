# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:33:51 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Entry2Proxy communication:
 * one 2 many
 * bi-directional

"""

from templates.node2node import Node2Node, Node2Node_from, Node2Node_to

class Entry2Proxy_from(Node2Node_from):

    def received_update(self, _proxy_host, _object_load, _cpu_load, _sent_received):
        """ Structure: 'update', (_proxy_addr, _proxy_port), _value(*) """
        self.entry.handle_update_proxy(_proxy_host, _object_load, _cpu_load, _sent_received)     
    
   
class Entry2Proxy_to(Node2Node_to):
            
    def send_join(self, _client_host, _proxy):
        """ Structure: 'join', (_client_addr, _client_port), (_proxy_addr, _proxy_port)"""
        msg = ('join', _client_host)
        self._send(msg, _proxy)
        
class Entry2Proxy(Node2Node, Entry2Proxy_from, Entry2Proxy_to):
    class ProxyList:
        pass
    
    def __init__(self, _entry):       
        self.entry = _entry
        self._from_addr = _entry.config.listenProxyAddr 
        self._from_port = _entry.config.listenProxyPort
         
        self._proxies = dict() # (_addr, _port) -> value
        Node2Node.__init__(self)
        