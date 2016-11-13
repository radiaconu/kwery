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
        self.sent = 0
        
        self.udpsocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
    def _send(self, data, (_addr, _port)):
        self.sent += 1
        self.udpsocket.sendto(json.dumps(data),(_addr, _port))
    
    def get_sent(self):
        sent = self.sent
        self.sent = 0
        return sent
        
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Node2Node_from(DatagramProtocol):
    """ All receiving functions ẗo all corresponding Node instances """
    
    def __init__(self):
        self.received = 0
        
        reactor.listenUDP(self._from_port, self)
        #DatagramProtocol.__init__(self) # no such method DON'T do it
        
    def datagramReceived(self, _msg, (_addr, _port)):
        self.received += 1
        msg = json.loads(_msg)
        getattr(self, 'received_'+msg[0])(*msg[1:])
        
    def get_received(self):
        received = self.received
        self.received = 0
        return received
        
class Node2Node(Node2Node_to, Node2Node_from):
    """ A common, unified interface for bi-directional communication """
    
    def __init__(self):
        #if hasattr(self,'_to_port'):
        Node2Node_to.__init__(self)
        if hasattr(self,'_from_port'):
            Node2Node_from.__init__(self)

