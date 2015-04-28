# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:19:21 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

The Disp forwards queries to concerning Nodes
The Coord assigns Proxy objects to coresponding Nodes

It listens for Proxies and Nodes

TODO: separate Disp from Coord
TOTO: add various parameters in update_peer
"""

from config_disp import ConfigDisp
from disp2peer import Disp2Peer
from disp2proxy import Disp2Proxy

from twisted.internet import reactor

import sys
sys.path.append('..')
from templates.runnable import Runnable
#from templates.simulator import Simulator
#from templates.events import EventType

class Event(object):
    def __init__(self, **kw):
        assert kw.has_key('type'), 'Event must have a type'
        self._dict = kw

    def __getattr__(self, key):
        return self._dict[key]

#class EventType:
#    InsertObject = 0
#    UpdatePeer = 1
#    QueryReceived = 3
#    EmptyQuery = 4
    
class Disp(Runnable):
    
    def __init__(self, _config_file='configDispDefault.cfg'):
        # singleton
        Disp.DISP = self
        
        self.config = ConfigDisp(_file=_config_file)
        
    def run(self):
        # effectively open connections
        self.disp2proxy = Disp2Proxy(self)
        self.disp2peer = Disp2Peer(self)
        
        # data management
        self.peers = dict() # host -> value
        #self.proxies = dict() # not used, proxies are not stored 
        
        # the event-driven simulator ###
#        self.sim = Simulator()
#        handlers = {
#            EventType.InsertObject :    handle_insert_object,
#            EventType.UpdatePeer :      handle_update_peer,
#            EventType.QueryReceived :   handle_query_received,
#            EventType.EmptyQuery :      handle_empty_query,
#        }
#        self.sim.setHandler(lambda event: handlers.get(event.type, None)(event))
        
        
        
     
    def handle_insert_object(self, _id, _value, _proxy_host):
        print "handle_insert_object", _id
        if not self.peers:
           return         
        peer = min(self.peers.keys(), key=lambda p: abs(_value[0]-self.peers[p][1][0])+abs(_value[1]-self.peers[p][1][1]) )
        self.disp2peer.send_insert(_id, _value, _proxy_host, peer)
        
    def handle_update_peer(self, _coverage, _barycenter, _peer_host):
        print _peer_host, _barycenter
        self.peers[tuple(_peer_host)] = (_coverage, _barycenter)
        
    def handle_query_received(self, _query_id, _min_value, _max_value, _proxy_host):
        inters_peers = []
        for peer_host in self.peers.keys():
            p_min_value, p_max_value = self.peers[peer_host].value[0]
            if ((_min_value[0]>p_min_value[0] and _min_value[0]<p_max_value[0]) or \
                (_max_value[0]>p_min_value[0] and _max_value[0]<p_max_value[0])) and\
               ((_min_value[1]>p_min_value[1] and _min_value[1]<p_max_value[1]) or \
                (_max_value[1]>p_min_value[1] and _max_value[1]<p_max_value[1])):
                    inters_peers.append(peer_host)
                    
        if not inters_peers:
            self.disp2proxy.send_empty_answer(_query_id, _proxy_host)
        else:
            for peer_host in inters_peers:
                self.disp2peer.send_query(_query_id, _min_value, _max_value, _proxy_host, peer_host)
        
    def handle_empty_query(self):
            pass

        
if __name__ == '__main__':    
    
    disp = Disp()    
    disp.run()

    reactor.run()

