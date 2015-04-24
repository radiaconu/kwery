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
from twisted.internet.protocol import DatagramProtocol
import json

from twisted.internet import reactor

class Disp2Node(DatagramProtocol):
    
    def __init__(self):        
        self.rcvd_msgs = 0
        self.total_rcvd = 0
    
    def datagramReceived(self, _msg, (host, port)):
        msg = json.loads(_msg)
        self.rcvd_msgs +=1
        self.total_rcvd += sys.getsizeof(_msg)
        
        print "from ", (host, port)
        print "datagram no", self.rcvd_msgs, "total rcvd =", self.total_rcvd 
        print "received:", msg
        
        getattr(self, 'from_node_'+msg[0])(host, port, *msg[1:]) 
    
    def from_node_update(self, _host, _port, _min_value, _max_value, _center):
        Disp.DISP.nodes[(_host,_port)] = _min_value, _max_value, _center
    

class Disp2Proxy(DatagramProtocol):
    def datagramReceived(self, _msg, (host, port)):
        msg = json.loads(_msg)
        getattr(self, 'from_proxy_'+msg[0])(*msg[1:])
        
    def from_proxy_insert(self, _host, _port, _id, _value):
        pass
    

import sys
sys.path.append('..')
from templates.runnable import Runnable

class Disp(Runnable):
    def __init__(self, _config_file='configDispDefault.cfg'):
        # singleton
        Disp.DISP = self
        
        self.config = ConfigDisp(_file=_config_file)
        self.nodes = dict()
        #self.config.load()
        
    def run(self):
        # listening for Nodes
        reactor.listenUDP(self.config.listenNodePort, Disp2Node())
        print "Listening for Nodes on", (self.config.listenNodeAddr, self.config.listenNodePort)
        
        # listening for Proxies
        reactor.listenUDP(self.config.listenProxyPort, Disp2Proxy())
        print "Listening for Proxies on", (self.config.listenNodeAddr, self.config.listenProxyPort)
        
if __name__ == '__main__':
    
    
    disp = Disp()    
    disp.run()

    reactor.run()
