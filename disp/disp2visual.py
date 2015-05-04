#!/usr/bin/env python
"""
Created on Sat Apr 30 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Diaspatcher2Monitor communication: 
 * one 2 one
 * uni-directional, sends data
"""

from templates.node2node import Node2Node, Node2Node_from, Node2Node_to

class Disp2Proxy_to(Node2Node_to):
    pass

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS #
from twisted.internet.task import LoopingCall
import json as json


class Monitor(WebSocketServerProtocol):
    
    def onConnect(self,request):
        print "monitor connected" 
        self.i=1
        try: self.refresh = float(request.params.get("r")[0])
        except: self.refresh = 2.0 # refresh data every 2 seconds
        LoopingCall(self.updateData).start(self.refresh,now=False)
        
    def get_report(self, peer_host):
        # self.peers[tuple(_peer_host)] = (_coverage, _barycenter)
        return dict(
                id = peer_host,
                x = self.disp[peer_host][0][0][0],
                y = self.disp[peer_host][0][0][1],
                width = self.disp[peer_host][0][1][0]-self.disp[peer_host][0][1][0],
                height = self.disp[peer_host][0][1][1]-self.disp[peer_host][0][1][1],
                bc_x = self.disp[peer_host][1][0],
                bc_y = self.disp[peer_host][1][1]
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
                bc_y = 0 #self.disp[peer_host][1][1]
                )
                            
    def updateData(self):
        #print "updata", self.__class__.report
        #report = [self.get_report(ph) for ph in  self.disp.peers.keys()]
        report = [self.get_empty_report('alpha', 20, 10), self.get_empty_report('beta', 100, 100)]
        self.sendMessage(json.dumps(report))
        report = []


from twisted.web import server, resource
from twisted.internet import reactor, fdesc
import os

class MonitorWebServer(resource.Resource):
    """ getproxy restfull call with jsonp
    """        
    isLeaf = True
    def render_GET(self, request):        
        getattr(self, request.args.get("action")[0])(request)
        
        returnvalue =  json.dumps(None)
        callback = request.args.get("callback")
        jsonp = request.args.get("jsonp")
        if callback or jsonp:
            if callback: callback = callback[0]
            else: callback = jsonp[0]
            
            returnvalue = "%s(%s)" % (callback, returnvalue )
        
        return returnvalue
    
    def clear(self, request):
        if os.path.exists('stats.dat'):
            os.remove('stats.dat')
        
        self.fd = open('stats.dat', 'w')
        fdesc.setNonBlocking(self.fd.fileno())
        fdesc.writeToFD(self.fd.fileno(), 'a, b, c, d, e, f, g, \n')        
        self.fd.close()
    
    def store(self, request):
        monitor_total_obj = float(request.args.get("obj")[0])
        
        self.fd = open('stats.dat', 'a')
        fdesc.setNonBlocking(self.fd.fileno())
        
        total_ticks = 0
        total_own_obj = 0
        total_nb_obj = 0
        min_ticks = 100
        
        for zone in self.dispatcher.zones.itervalues():
            total_ticks += zone.ticks
            total_own_obj += zone.own_obj
            total_nb_obj += zone.nb_obj
            if zone.ticks<min_ticks: min_ticks = zone.ticks
        
        
        nzones = len(self.dispatcher.zones)
        delay_avg = nzones/total_ticks
        delay_max = 1./min_ticks
        
        avg_own_obj = total_own_obj/nzones
        avg_nb_obj = total_nb_obj/nzones
        
        overlap = float(total_nb_obj)/total_own_obj
        fdesc.writeToFD(self.fd.fileno(), 
                        str(monitor_total_obj)+', '+str(nzones)+', '+str(delay_avg)+', '+str(delay_max)+\
                        ', '+str(avg_own_obj)+', '+str(avg_nb_obj)+', '+str(overlap)+', \n')
        
        self.fd.close()
        
class Disp2Monitor(object):
    def __init__(self, dispatcher):
        webserver = resource.Resource()
        mws = MonitorWebServer()
        mws.dispatcher = dispatcher
        webserver.putChild('',mws)
    
        site = server.Site(webserver)
        reactor.listenTCP(7357, site)
        print "Disp2Monitor running on, 7357 "
    