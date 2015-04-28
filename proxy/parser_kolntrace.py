# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 12:05:55 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

Parser for the dataset kolntrace (http://kolntrace.project.citi-lab.fr/)
"""
from time import time

class Parser:
    def __init__(self):
        self.file = open('kolntrace', 'r')
        self.ids = set()
        self.time = 22600
        
    
    def __iter__(self):
        while (True):
            line = self.file.readline() # _time, _oid, _lng, _lat, _speed 
            values = line.split()
            #print line
            
            try:
                values[0] = int(values[0])
                values[2] = float(values[2])
                values[3] = float(values[3])
            except Exception:
                continue
            
            _time = values[0]
            if _time>self.time:
                print "done"
                #time.sleep(1)
                self.time=_time
                break
            self.ids.add(values[1])
                
            yield values
#        return values


if __name__ == '__main__':
    p = Parser()
    for _ in p:
        print _
    print(len(p.ids))