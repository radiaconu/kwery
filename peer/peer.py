# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:09:30 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

TODO: put constans in config loading
"""
INTERVAL = 2
from config_peer import ConfigPeer
from peer2disp import Peer2Disp
from peer2proxy import Peer2Proxy

from index import LocalIndex as Index

import sys
sys.path.append('..')
from templates.runnable import Runnable

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

class Peer(Runnable):
    def __init__(self, _config_file = 'configPeerDefault.cfg'):
        # singleton
        Peer.PEER = self
        self.config = ConfigPeer(_file= _config_file)
    
    def run(self):
        self.peer2proxy = Peer2Proxy(self)
        self.peer2disp = Peer2Disp(self)
        
        self.index = Index()
        
        self.loop_send_update = LoopingCall(self.peer2disp.send_update)
        self.loop_send_update.start(self.config.UPDATE_INTERVAL)

if __name__ == '__main__':
    peer = Peer()
    peer.run()
    
    _msg = ['print', 'yo']
       
    reactor.run()