#!/usr/bin/env python
"""
Created on Sat Apr 30 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Diaspatcher2Monitor communication: 
 * one 2 one
 * uni-directional, sends data
"""

#from templates.node2node import Node2Node, Node2Node_from, Node2Node_to

#from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS #
#from twisted.internet.task import LoopingCall
import json as json


class Disp2Visual_to(WebSocketServerProtocol):
    
    def onConnect(self,request):
        print "monitor connected" 
        self.i=1
        try: self.refresh = float(request.params.get("r")[0])
        except: self.refresh = 2.0 # refresh data every 2 seconds
        LoopingCall(self.updateData).start(self.refresh,now=False)
        
    def get_report(self, peer_host):
        # self.peers[tuple(_peer_host)] = (_coverage, _barycenter)
        peer=self.disp.peers[peer_host]
        return dict(
                id = peer_host,
                x = peer[0][0][0], # (peer[0][0][0]-3000)/25,
                y = peer[0][0][1], # (peer[0][0][1]-800)/31.2,
                width = (peer[0][1][0]-peer[0][0][0]), # /25,
                height = (peer[0][1][1]-peer[0][0][1]), #/31.2,
                bc_x = peer[1][0], # (peer[1][0]-3000)/25,
                bc_y = peer[1][1], # (peer[1][1]-800)/31.2,
                object_load = peer[2]
                )
    
    def get_empty_report(self, _id, x,y):
        # self.peers[tuple(_peer_host)] = (_coverage, _barycenter)
        
        self.i+=1
        return dict(
                id = _id,
                x = x+100, #self.disp[peer_host][0][0][0],
                y = y, #self.disp[peer_host][0][0][1],
                width = 60, # self.disp[peer_host][0][1][0]-self.disp[peer_host][0][1][0],
                height = 20, #self.disp[peer_host][0][1][1]-self.disp[peer_host][0][1][1],
                bc_x = 0, #self.disp[peer_host][1][0],
                bc_y = 0, #self.disp[peer_host][1][1]
                object_load = 0 #self.disp[peer_host][1][1]
                )
                            
    def updateData(self):
        report = [self.get_report(ph) for ph in  self.disp.peers.keys()]
        #report = [self.get_empty_report('alpha', 20, 10), self.get_empty_report('beta', 100, 100)]
        
        self.sendMessage(json.dumps(report))
        report = []


class Disp2Visual_to_file():
    def __init__(self, _disp):
        self.disp = _disp
        print "Disp2Visual_to_file started" 
        self.i=1
        self.refresh = 2.0 # refresh data every 2 seconds
        self.out_file = open('results', 'w')
        
        LoopingCall(self.updateData).start(self.refresh,now=False)
    
    def get_report(self, peer_host):
        peer=self.disp.peers[peer_host]
        return dict(
                id = peer_host,
                x = peer[0][0][0], # (peer[0][0][0]-3000)/25,
                y = peer[0][0][1], # (peer[0][0][1]-800)/31.2,
                width = (peer[0][1][0]-peer[0][0][0]), # /25,
                height = (peer[0][1][1]-peer[0][0][1]), #/31.2,
                bc_x = peer[1][0], # (peer[1][0]-3000)/25,
                bc_y = peer[1][1], # (peer[1][1]-800)/31.2,
                object_load = peer[2]
                )
                            
    def updateData(self):
        #print "updata", self.__class__.report
        report = [self.get_report(ph) for ph in  self.disp.peers.keys()]
        self.out_file.write(json.dumps(report))
        self.out_file.write('\n')

class Disp2Visual_from_file(WebSocketServerProtocol):
    def onConnect(self,request):
        print "Disp2Visual_from_file connected" 
        self.refresh = 2.0 # refresh data every 2 seconds
        self.in_file = open('results', 'r')
        
        LoopingCall(self.updateData).start(self.refresh,now=False)
    
#    def get_report(self, peer_host):
#        peer = json.loads(self.in_file.readline())
#        print peer
        
    def updateData(self):
        self.sendMessage(self.in_file.readline())
        
class Disp2Visual:
    def __init__(self, _disp):
        self.disp = _disp
        
        # to file, no visualiser
        Disp2Visual_to_file(_disp)
        return
        
#        # from file, only visual
#        Disp2Visual_from_file.disp = _disp
#        socketurl = 'ws://localhost:9997'
#        factory = WebSocketServerFactory(socketurl)
#        factory.protocol = Disp2Visual_from_file
#        listenWS(factory)
#        print "Websocket",socketurl,"ok ..."
#        return
#        
#        # live, connect to monitor websocket
#        Disp2Visual_to.disp = _disp
#        socketurl = 'ws://localhost:9997'
#        factory = WebSocketServerFactory(socketurl)
#        factory.protocol = Disp2Visual_to
#        listenWS(factory)
#        print "Websocket",socketurl,"ok ..."
        