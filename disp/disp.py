# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:19:21 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

The Disp forwards queries to concerning Nodes
The Coord assigns Proxy objects to coresponding Nodes

It listens for Proxies and Nodes

TODO: separate Disp from Coord
"""

from config_disp import ConfigDisp
from disp2peer import Disp2Peer
from disp2proxy import Disp2Proxy

from twisted.internet import reactor

import sys
sys.path.append('..')
from templates.runnable import Runnable
from templates.simulator import Simulator
#from templates.events import EventType

class Event(object):
    def __init__(self, **kw):
        assert kw.has_key('type'), 'Event must have a type'
        self._dict = kw

    def __getattr__(self, key):
        return self._dict[key]

class EventType:
    InsertObject = 0
    UpdatePeer = 1
    
class Disp(Runnable):
    
    def __init__(self, _config_file='configDispDefault.cfg'):
        # singleton
        Disp.DISP = self
        
        self.config = ConfigDisp(_file=_config_file)
        
    def run(self):
        
        # effectively open connections
        self.disp2proxy = Disp2Proxy(self)
        self.disp2peer = Disp2Peer(self)
        
        # the event-driven simulator
        self.sim = Simulator()
        handlers = {
            EventType.InsertObject :    self.disp2peer.select_and_insert,
            EventType.UpdatePeer :      self.disp2peer.received_update,
        }
        self.sim.setHandler(lambda event: handlers.get(event.type, None)(event))
        
        
        # data management
        self.peers = dict()
        #self.proxies = dict() # not used, proxies are not stored 
        
        
        
if __name__ == '__main__':    
    
    disp = Disp()    
    disp.run()

    reactor.run()

