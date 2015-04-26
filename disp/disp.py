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
from disp2leaf import Disp2Leaf
from disp2proxy import Disp2Proxy

from twisted.internet import reactor

import sys
sys.path.append('..')
from templates.runnable import Runnable

class Disp(Runnable):
    def __init__(self, _config_file='configDispDefault.cfg'):
        # singleton
        Disp.DISP = self
        
        self.config = ConfigDisp(_file=_config_file)
        
    def run(self):
        # effectively open connections
        self.disp2proxy = Disp2Proxy(self)
        #self.disp2leaf = Disp2Leaf(self)
        
        # data management
        self.leaves = dict()
        self.proxies = dict()
        
        
        
if __name__ == '__main__':    
    
    disp = Disp()    
    disp.run()

    reactor.run()

