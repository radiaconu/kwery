# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:48:06 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Diaspatcher2Peer communication:
 * one 2 many
 * bi-directional

TODO: everything
"""
from templates.node2node import Node2Node, Node2Node_from, Node2Node_to

class Disp2Peer_to(Node2Node_to):
    
    def received_update(self, (_addr, _port), _value):
        if not self._peers.get( (_addr, _port) ):
            print "new peer",
        print "update", (_addr, _port), _value
        self._peers[(_addr, _port)] = _value
        

class Disp2Peer_from(Node2Node_from):
    def send_insert(self, _id, _value):
        msg = ('insert', self._to_addr, self._to_port, _id, _value)
        self._send(msg, (self._to_addr, self._to_port))
        
        
class Disp2Peer(Node2Node, Disp2Peer_from, Disp2Peer_to):
    class PeerList:
        pass
    
    def __init__(self, _disp):       
        self.disp = _disp
        self._from_addr = _disp.config.listenPeerAddr # unimportant for now
        self._from_port = _disp.config.listenPeerPort
         
        self._peers = dict()
        Node2Node.__init__(self)
#
#class Disp2Peer(Node2Node):
#    
#    def __init__(self):        
#        self.rcvd_msgs = 0
#        self.total_rcvd = 0
#    
#    def datagramReceived(self, _msg, (host, port)):
#        msg = json.loads(_msg)
#        self.rcvd_msgs +=1
#        self.total_rcvd += sys.getsizeof(_msg)
#        
#        print "from ", (host, port)
#        print "datagram no", self.rcvd_msgs, "total rcvd =", self.total_rcvd 
#        print "received:", msg
#        
#        getattr(self, 'from_peer_'+msg[0])(host, port, *msg[1:]) 
#    
#    def from_peer_update(self, _host, _port, _min_value, _max_value, _center):
#        Disp.DISP.peers[(_host,_port)] = _min_value, _max_value, _center
#    