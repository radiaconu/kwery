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

class Disp2Peer_from(Node2Node_from):

    def received_update(self, _coverage, _barycenter, _object_load, _peer_host):
        """ Structure: 'update', (_peer_addr, _peer_port), _value """
        self.disp.handle_update_peer(_coverage, _barycenter, _object_load, _peer_host)     
    
    def received_transfer(self, _id, _value, _proxy_host):
        """ Structure: 'insert', _id, _value, (_proxy_addr, _proxy_port) """
        print "transfer", _value
        self.disp.handle_insert_object(_id, _value, _proxy_host)
    

class Disp2Peer_to(Node2Node_to):
            
    def send_insert(self, _id, _value, _proxy, _peer):
        """ Structure: 'insert', _id, _value, (_proxy_addr, _proxy_port) """
        msg = ('insert', _id, _value, _proxy)
        self._send(msg, _peer)
    
    def send_query(self, _query_id, _min_value, _max_value, _proxy_host, _peer):
        """ Structure: 'get', _query_id, _min_value, _max_value, (_proxy_addr, _proxy_port) """
        msg = ('get', _query_id, _min_value, _max_value, _proxy_host)
        self._send(msg, _peer)
        
class Disp2Peer(Node2Node, Disp2Peer_from, Disp2Peer_to):
    class PeerList:
        pass
    
    def __init__(self, _disp):       
        self.disp = _disp
        self._from_addr = _disp.config.listenPeerAddr # unimportant for now
        self._from_port = _disp.config.listenPeerPort
         
        self._peers = dict() # (_addr, _port) -> value
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