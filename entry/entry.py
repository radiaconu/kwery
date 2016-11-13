# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:10:59 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Entry point for incoming moving objects and queries.
Dynamically maintains a balanced load among proxies.

TODO: Is it possible to connect directly to a proxy?
TODO: Which is the best connection type? UDP / TCP / WebSock? 
"""

from config_entry import ConfigEntry
from entry2proxy import Entry2Proxy
from entry2visual import Entry2Visual

import sys
sys.path.append('..')
from templates.runnable import Runnable

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

import time

from templates.runnable import Runnable


class Entry(Runnable):
    
    def __init__(self, _config_file='configEntryDefault.cfg'):        
        self.config = ConfigEntry(_file=_config_file)

    
    def run(self):
        self.entry2proxy = Entry2Proxy(self)
        self.entry2visual = Entry2Visual(self)
        #self.entry2client = Entry2Client(self)
        self.proxies = dict() # host -> value
    
    def handle_update_proxy(self, _proxy_host, _object_load, _cpu_load, _sent_received):
        self.proxies[tuple(_proxy_host)] = [_object_load, _cpu_load, _sent_received]
        

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType
    
    argParser = ArgumentParser(description='The Entry.')
    argParser.add_argument('--c', type=FileType('rw'), default="configEntryDefault.cfg", help='the configuration file, default configEntryDefault.cfg')
    
    args = argParser.parse_args()
    
    print args.c.name
    entry = Entry(args.c.name)
    entry.run()
    
       
    reactor.run()