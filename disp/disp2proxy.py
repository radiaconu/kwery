# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:44:17 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Diaspatcher2Proxy communication: 
 * one 2 many
 * bi-directional, receive inserts & queries, replies empty query answers (??)
"""

from templates.node2node import Node2Node, Node2Node_from, Node2Node_to

class Disp2Proxy_to(Node2Node_to):
    def send_empty_answer(self, _query_id, _proxy_host):
        """ Structure: 'answer', _query_id, [] """
        msg = ('answer', _query_id, [])
        self._send(msg, _proxy_host)
    
class Disp2Proxy_from(Node2Node_from):
    
    def received_insert(self, _id, _value, _proxy_host):
        """ Structure: 'insert', _id, _value, (_proxy_addr, _proxy_port) """
        print "insert", _id
        self.disp.handle_insert_object(_id, _value, _proxy_host)
    
    def received_get(self, _query_id, _min_value, _max_value, _proxy_host):
        """ Structure: 'get',  _query_id, _min_value, _max_value, (_proxy_addr, _proxy_port) """
        self.disp.handle_received_query(_query_id, _min_value, _max_value, _proxy_host)
        
class Disp2Proxy(Node2Node, Disp2Proxy_from, Disp2Proxy_to):
    def __init__(self, _disp):       
        
        self.disp = _disp
        self._from_addr = _disp.config.listenProxyAddr # unimportant for now
        self._from_port = _disp.config.listenProxyPort
         
        self._all = dict()
        Node2Node.__init__(self)
