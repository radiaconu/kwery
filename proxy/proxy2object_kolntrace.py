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
    
    def dump_ids(self, _ids, n):
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
        
class Proxy2Object:
    def __init__(self, _proxy):
        self.proxy = _proxy
        
        parser = Parser()
        parser.proxy = _proxy
        #parser.search()
        
#        ids = parser.pick_ids(1000, 100)
#        parser.dump_ids(ids, 5)
        
        ids=parser.load_ids(open(_proxy.config.ids_file))
        print ids
        parser.refresh()
        parser.simulate(ids)
        