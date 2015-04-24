# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 20:12:48 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Proxy: hanles objects 
For now it is just a generator

Listens for the Nodes
Connects to the Disp

TODO: everything
"""
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import json
from config_proxy import ConfigProxy

class Proxy2Node(DatagramProtocol):
    def datagramReceived(self, _msg, (host, _port)):
        msg = json.loads(_msg)
        getattr(self, 'from_proxy_'+msg[0])(*msg[1:])

class Proxy:
    def __init__(self, _config_file='configProxyDefault.cfg'):
        self.config = ConfigProxy(_file=_config_file)
        self.objects = dict()
    
    def run(self):
        # listening for Nodes
        reactor.listenUDP(self.config.listenNodePort, Proxy2Node())
        print "Listening for Nodes on", (self.config.listenNodeAddr, self.config.listenNodePort)
        
        
if __name__ == '__main__':
    proxy = Proxy()
    proxy.run()
    reactor.run()