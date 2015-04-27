# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 23:37:45 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Template for sending messages between generic nodes
Holds the logic of each type of connection
e.g., Disp2Proxy: 1 Disp opens a sock, many Proxies connect to it.
Manages message encoding and transmission
It needs to be called from a Runnable
"""

import socket
import json

class Node2Node_to(object):
    """ All sending functions ẗo all corresponding Node instances """
    
    def __init__(self):
        print "udpsocket"
        self.udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
    def _send(self, data, (_addr, _port)):
        #self.sent += 1
        print data, (_addr, _port)
        self.udpsocket.sendto(json.dumps(data),(_addr, _port))
        
        
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Node2Node_from(DatagramProtocol):
    """ All receiving functions ẗo all corresponding Node instances """
    
    def __init__(self):
        reactor.listenUDP(self._from_port, self)
        #DatagramProtocol.__init__(self) # no such method DON'T do it
        
    def datagramReceived(self, _msg, (_addr, _port)):
        msg = json.loads(_msg)
        getattr(self, 'received_'+msg[0])((_addr, _port), *msg[1:])
        
        
class Node2Node(Node2Node_to, Node2Node_from):
    """ A common, unified interface for bi-directional communication """
    
    def __init__(self):
        if hasattr(self,'_to_port'):
            Node2Node_to.__init__(self)
        if hasattr(self,'_from_port'):
            Node2Node_from.__init__(self)

