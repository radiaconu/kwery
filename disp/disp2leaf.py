# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:48:06 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Diaspatcher2leaf communication: ***one 2 many***

TODO: everything
"""
from templates.node2node import Node2Node, Node2Node_from, Node2Node_to

class Disp2Leaf_to(Node2Node_to):
    
    def received_update(self, _host, _port, _id, _value):
        if not self._all.get( (_host, _port) ):
            print "new leaf"
        self._all[(_host, _port)] = _value
        

class Disp2Leaf_from(Node2Node_from):
    def send_insert(self, _id, _value):
        msg = ('insert', self._to_addr, self._to_port, _id, _value)
        self._send(msg, (self._to_addr, self._to_port))
        
        
class Disp2Leaf(Node2Node, Disp2Leaf_from, Disp2Leaf_to):
    def __init__(self, _disp):       
        self.disp = _disp
        self._from_addr = _disp.config.listenLeafAddr # unimportant for now
        self._from_port = _disp.config.listenLeafPort
         
        self._all = dict()
        Node2Node.__init__(self)
#
#class Disp2Leaf(Node2Node):
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
#        getattr(self, 'from_leaf_'+msg[0])(host, port, *msg[1:]) 
#    
#    def from_leaf_update(self, _host, _port, _min_value, _max_value, _center):
#        Disp.DISP.leaves[(_host,_port)] = _min_value, _max_value, _center
#    