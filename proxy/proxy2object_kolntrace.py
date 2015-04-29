# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:03:08 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Parser for the dataset kolntrace (http://kolntrace.project.citi-lab.fr/)
Replaces the proxy2object communication
"""

from twisted.internet import reactor

class Parser:
    def __init__(self):
        self.file = open('kolntrace', 'r')
        self.ids = set()
        self.sim_time = 21600
        self.end_time = 22605
        
        self.cur_line = None # the last line read fom the 
        self.values = dict() # 
        
    def refresh(self):        
        self.file.seek(0)
        
    def simulate(self, ids):
        cur_line = self.file.readline()
        cur_values = cur_line.split()
        cur_time = int(cur_values[0])
        
        sent = 0
        while sent < 10:
            try:
                _id = cur_values[1]
                if _id in ids:
                    lng = float(cur_values[2])
                    lat = float(cur_values[3])
                    sent +=1 
                    self.proxy.handle_put(_id, (lng, lat))
                    
            except Exception, e:
                print e
            cur_line = self.file.readline()
            cur_values = cur_line.split()
            cur_time = int(cur_values[0])
        
        if cur_time < self.end_time:
            reactor.callLater(0.02, self.simulate, ids)
        
            
            

    def pick_ids(self, nb):
        self.file.seek(0)
        ids = set()
        
        while len(ids)<nb:
            cur_line = self.file.readline()
            cur_values = cur_line.split()
            ids.add(cur_values[1])
        
        
        self.file.seek(0)
        return ids
        
class Proxy2Object:
    def __init__(self, _proxy):
        self.proxy = _proxy
        
        parser = Parser()
        parser.proxy = _proxy
        ids = parser.pick_ids(1000)
        parser.simulate(ids)
        