# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 13:48:06 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Diaspatcher2leaf communication: ***one 2 many***

TODO: everything
"""

import sys
sys.path.append('..')
from templates.node2node import Node2Node, Node2Node_from, Node2Node_to

class Disp2Leaf(Node2Node):
    
    def __init__(self, _disp):
        # listening for Leaves
        reactor.listenUDP(self.config.listenLeafPort, self.disp2leaf._from)
        print "Listening for Leaves on", (self.config.listenLeafAddr, self.config.listenLeafPort)
        
        self.disp = _disp
        self._from = Disp2Leaf_from()
        self._to = Disp2Leaf_to()

class Disp2Leaf_to(Node2Node_to):
    pass

class Disp2Leaf_from(Node2Node_from):
    pass
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