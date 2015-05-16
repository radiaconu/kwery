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

from disp2visual import Disp2Visual

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
        self.disp2visual = Disp2Visual(self)
        
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
        if not self.peers:
            return     
        
        def increases_area(_value, _peer):
            _min_value, _max_value = list(_peer[0][0]), list(_peer[0][1])            
            a1 = (_max_value[0]-_min_value[0]) * (_max_value[1]-_min_value[1])            
            if  _value[0] < _min_value[0]: _min_value[0] = _value[0]
            if  _value[1] < _min_value[1]: _min_value[1] = _value[1]
            if  _value[0] > _max_value[0]: _max_value[0] = _value[0]
            if  _value[1] > _max_value[1]: _max_value[1] = _value[1]            
            a2 = (_max_value[0]-_min_value[0]) * (_max_value[1]-_min_value[1])
            
            return a2-a1
        
        def product_metric(_value, _peer):
            distance = abs(_value[0]-_peer[1][0]) + abs(_value[1]-_peer[1][1])
            surface = increases_area(_value, _peer)
            number = _peer[2]
            
            #print _peer
            #print distance, surface, number
            #if not number: return number
            return number+distance
        
        
        def update_peer(_peer, _value):
            if  _value[0] < _peer[0][0][0]: _peer[0][0][0] = _value[0]
            if  _value[1] < _peer[0][0][1]: _peer[0][0][1] = _value[1]
            if  _value[0] > _peer[0][1][0]: _peer[0][1][0] = _value[0]
            if  _value[1] > _peer[0][1][1]: _peer[0][1][1] = _value[1]            
            
#        v= self.peers.keys()
#        print v
#        if _value[0] < 500:
#            if _value[1]<500:
#                peer =v[0]
#            else:
#                peer = v[1]
#        else:
#            if _value[1]<500:
#                peer = v[2]
#            else:
#                peer = v[3]
        peer = min(self.peers.keys(), key=lambda p: product_metric(_value, self.peers[p]))
        update_peer(self.peers[peer], _value)
        
#        all_increases = {p:increases_area(_value, self.peers[p]) for p in self.peers.keys()}
#        all_increases0 = {p:all_increases[p] for p in all_increases.keys() if all_increases[p]==0}
#        if all_increases0:
#            print '+0'
#            peer = min(all_increases0.keys(), key=lambda p:(abs(_value[0]-self.peers[p][1][0])+ abs(_value[1]-self.peers[p][1][1]) ))
#            #peer = min(all_increases0.keys(), key=lambda p:self.peers[p][2])
#        else:
#            print 'o'
#            peer = next((p for p in self.peers.keys() if self.peers[p][2]<10), None)
#        if not peer:
#            print 'min'
#            peer = min(all_increases.keys(), key=lambda p: all_increases[p])
           
        #peer = next((p for p in self.peers.keys() if self.peers[p][2]==0), None)
        #if peer is None:         
        #    peer = min(self.peers.keys(), key=lambda p: increases_area(_value, self.peers[p]))
            # abs(_value[0]-self.peers[p][1][0])**2+abs(_value[1]-self.peers[p][1][1])**2 )
        
        self.disp2peer.send_insert(_id, _value, _proxy_host, peer)
        
    def handle_update_peer(self, _coverage, _barycenter, _object_load, _peer_host):
        #print 'update peer'
        self.peers[tuple(_peer_host)] = (_coverage, _barycenter, _object_load)
        
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


    def cleanup(self):
        import time
        now = time.time()
        for (_id,_peer) in self.peers.items():
            if now - _peer[3] > self.config.interval:
                del _peer
                del self.peers[_id]
        
if __name__ == '__main__':    
    from argparse import ArgumentParser, FileType
    
    argParser = ArgumentParser(description='Dispatcher.')
    argParser.add_argument('--c', type=FileType('rw'), default="configDispDefault.cfg", help='the configuration file, default configDispDefault.cfg')
    
    args = argParser.parse_args()
    
    print args.c.name
    
    disp = Disp(args.c.name)    
    disp.run()

    reactor.run()

