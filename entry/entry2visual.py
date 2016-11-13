# -*- coding: utf-8 -*-
"""
Created on Thu May 21 12:17:41 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Entry2Monitor communication: 
 * one 2 one
 * uni-directional, sends data
 
"""



#from templates.node2node import Node2Node, Node2Node_from, Node2Node_to

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS #
from twisted.internet.task import LoopingCall
import json as json


class Entry2Visual_to(WebSocketServerProtocol):
    
    def onConnect(self,request):
        print "monitor connected" 
        self.i=1
        try: self.refresh = float(request.params.get("r")[0])
        except: self.refresh = 2.0 # refresh data every 2 seconds
        LoopingCall(self.updateData).start(self.refresh,now=False)
        
    def get_report(self, proxy_host):
        # self.proxies[tuple(_proxy_host)] = (_coverage, _barycenter)
        proxy=self.entry.proxies[proxy_host]
        return dict(
                id = proxy_host,
                object_load = proxy[2],
                proxy_sent      = peer[3][0],
                proxy_received  = peer[3][1],
                disp_sent       = peer[3][2],
                disp_received   = peer[3][3]
                )
    
                      
    def updateData(self):
        report = [self.get_report(ph) for ph in  self.entry.proxies.keys()]
        
        self.sendMessage(json.dumps(report))
        report = []


class Entry2Visual_to_file():
    def __init__(self, _entry):
        self.entry = _entry
        print "Entry2Visual_to_file started" 
        self.i=1
        self.refresh = 2.0 # refresh data every 2 seconds
        self.out_file = open('results', 'w')
        
        LoopingCall(self.updateData).start(self.refresh,now=False)
    
    def get_report(self, proxy_host):
        proxy=self.entry.proxies[proxy_host]
        return dict(
                id = proxy_host,
                object_load = proxy[2],
                proxy_sent      = peer[3][0],
                proxy_received  = peer[3][1],
                disp_sent       = peer[3][2],
                disp_received   = peer[3][3]
                )
                            
    def updateData(self):
        #print "updata", self.__class__.report
        report = [self.get_report(ph) for ph in  self.entry.proxies.keys()]
        self.out_file.write(json.dumps(report))
        self.out_file.write('\n')

class Entry2Visual_from_file(WebSocketServerProtocol):
    def onConnect(self,request):
        print "Entry2Visual_from_file connected" 
        self.refresh = 2.0 # refresh data every 2 seconds
        self.in_file = open('results', 'r')
        
        LoopingCall(self.updateData).start(self.refresh,now=False)
    
        
    def updateData(self):
        self.sendMessage(self.in_file.readline())
        
class Entry2Visual:
    def __init__(self, _entry):
        self.entry = _entry
        
        # to file, no visualiser
#        Entry2Visual_to_file(_entry)
#        return
        
#        # from file, only visual
#        Entry2Visual_from_file.entry = _entry
#        socketurl = 'ws://localhost:9997'
#        factory = WebSocketServerFactory(socketurl)
#        factory.protocol = Entry2Visual_from_file
#        listenWS(factory)
#        print "Websocket",socketurl,"ok ..."
#        return
#        
        # live, connect to monitor websocket
        Entry2Visual_to.entry = _entry
        socketurl = 'ws://localhost:9997'
        factory = WebSocketServerFactory(socketurl)
        factory.protocol = Entry2Visual_to
        listenWS(factory)
        print "Websocket",socketurl,"ok ..."
        