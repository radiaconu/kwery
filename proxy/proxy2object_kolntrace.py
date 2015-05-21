# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:03:08 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Parser for the dataset kolntrace (http://kolntrace.project.citi-lab.fr/)
Replaces the proxy2object communication
"""

from twisted.internet import reactor

import time

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
        #self.file.seek(0)
        cur_line = self.file.readline()
        cur_values = cur_line.split()
        cur_time = int(cur_values[0])
        
        sent = 0
        while sent < 100:
            try:
                _id = cur_values[1]
                if _id in ids:
                    lng = (float(cur_values[2])-3000)/25
                    lat = (float(cur_values[3])-800)/31.2
                    sent +=1 
                    self.proxy.handle_put(_id, (lng, lat))
                    
            except Exception, e:
                print e
            cur_line = self.file.readline()
            cur_values = cur_line.split()
            cur_time = int(cur_values[0])
        
        if cur_time < self.end_time:
            reactor.callLater(0.2, self.simulate, ids)
        
    
    def simulate_with_time(self, ids):
        cur_line = self.file.readline()
        cur_values = cur_line.split()
        cur_time = cur_values[0]
        
        
        all_lines = []
        print "loading all lines", cur_time
        while cur_time == cur_values[0]:
            last_pos = self.file.tell()
            if cur_values[1] in ids: all_lines.append(cur_line)
            
            cur_line = self.file.readline()
            cur_values = cur_line.split()
            if not cur_line: 
                self.file.seek(0)
        print "finished loading all lines", cur_values[0]
        
        self.file.seek(last_pos)
        
        nb  = len(all_lines)/10
        while all_lines:
            for i in range(nb):
                try:
                    cur_line = all_lines.pop()
                    cur_values = cur_line.split()
                    lng = (float(cur_values[2])-3000)/25
                    lat = (float(cur_values[3])-800)/31.2
                    _id = cur_values[1]
                    self.proxy.handle_put(_id, (lng, lat))
                except Exception, e:
                    break
            
            time.sleep(.01)
            
        self.simulate_with_time(ids)
        
        
    def pick_ids(self, nb_obj, nb_rounds):
        """ this is quick and dirty; to be revised. """
        self.file.seek(0)
        ids=set()
        
        nb = 0
        
        while nb < nb_rounds:
            nb +=1
            
            while len(ids) < nb*nb_obj:
                cur_line = self.file.readline()
                cur_values = cur_line.split()
                try:
                    ids.add(cur_values[1])
                except Exception:
                    if not cur_line:
                        print 'eof', nb, len(ids)
                        self.file.seek(0)
            
            
            time_1 = int(cur_values[0])
            
            while int(cur_values[0]) is time_1:
                cur_line = self.file.readline()
                cur_values = cur_line.split()
        
        self.file.seek(0)
        #print ids
        print len(ids)
        return ids
    
    def dump_ids(self, _ids=None, n=4):
        if not _ids:
            _ids = set()
            self.file.seek(0)
            cur_line = self.file.readline()
            while cur_line:
                cur_values = cur_line.split()
                _ids.add(cur_values[1])          
                cur_line = self.file.readline()
                
        print "done...", len(_ids)
        
        import random
        ids = [[] for _ in range(n)]
        print ids
        for i in _ids:
            random.choice(ids).append(i)
        for i in range(n):
            print len(ids[i])
            _file = open('ids_'+str(i), 'w')
            
            for _ in ids[i]:
                _file.write(u"%s\n" %_)
            
    def load_ids(self, _file):
        return set(l.split()[0] for l in _file.readlines())
    
    def search(self):
        self.file.seek(0)
        print "search"
        min_x = 100000
        min_y = 100000
        max_x = -100000
        max_y = -100000
        cur_line = self.file.readline()
        while cur_line:
            cur_values = cur_line.split()
            cur_x = float(cur_values[2])
            cur_y = float(cur_values[3])
            if cur_x<min_x:  min_x=cur_x
            if cur_y<min_y:  min_y=cur_y
            if cur_x>max_x:  max_x=cur_x
            if cur_y>max_y:  max_y=cur_y
            cur_line = self.file.readline()
            
        print (min_x, min_y),(max_x, max_y)
        self.file.seek(0)
    
    def count_time(self):
        self.file.seek(0)
        times = dict()
        
        cur_line = self.file.readline()
        while cur_line:
            cur_values = cur_line.split()
            if not times.get(cur_values[0]): times[cur_values[0]] = 0
            times[cur_values[0]] +=1
            cur_line = self.file.readline()
        
        print 'max', max(times.values())
        print 'min', min(times.values())
            
    def count_ids(self):
        self.file.seek(0)
        ids = set()
        nb_lines = 0
        
        
        cur_line = self.file.readline()
        while cur_line:
            cur_values = cur_line.split()
            if len(cur_values[1]) < 10:
                ids.add(cur_values[1])
            else:
                nb_lines +=1
            cur_line = self.file.readline()
        
        print "nb_ids ", len(ids)
        print "nb_lines weired", nb_lines
        print "avg_updates/id", nb_lines/len(ids)
#nb_secs        7201
#nb_ids         121164
#nb_short_ids   117484

#nb_lines       75882909
#nb_weired_lines 2087254
#avg_updates/id 626

#avg_ids/sec    10537

        
        
class Proxy2Object:
    def __init__(self, _proxy):
        self.proxy = _proxy
        
        parser = Parser()
        parser.proxy = _proxy
        
        print "loading file", _proxy.config.ids_file
        ids=parser.load_ids(open(_proxy.config.ids_file))
        print ids
        parser.refresh()
        parser.simulate_with_time(ids)

#        ids = parser.pick_ids(1000, 100)
#        parser.dump_ids()
        
        
#        parser.count_ids()
#        parser.count_time()