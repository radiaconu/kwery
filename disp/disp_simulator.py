# -*- coding: utf-8 -*-
"""
Created on Mon May 11 15:20:51 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Simulates the dispatcher for a local visualiser
"""

from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketClientFactory, WebSocketServerProtocol, listenWS #
from disp2visual import Monitor, Disp2Monitor

import sys
sys.path.append('..')
from templates.runnable import Runnable

class Disp(Runnable):
    
    def __init__(self, _config_file='configDispDefault.cfg'):
        # singleton
        Disp.DISP = self
        
        
    def run(self):
        
        #connect to monitor websocket
        Monitor.disp = self
        socketurl = 'ws://localhost:9997'
        factory = WebSocketServerFactory(socketurl)
        factory.protocol = Monitor
        listenWS(factory)
        print "Websocket",socketurl,"ok ..."
        
        #Disp2Monitor(self)
        
        ############
        
        

if __name__ == '__main__':    
    from argparse import ArgumentParser, FileType
    
    argParser = ArgumentParser(description='Dispatcher.')
    argParser.add_argument('--c', type=FileType('rw'), default="configDispDefault.cfg", help='the configuration file, default configDispDefault.cfg')
    
    args = argParser.parse_args()
    
    print args.c.name
    
    disp = Disp(args.c.name)    
    disp.run()

    reactor.run()