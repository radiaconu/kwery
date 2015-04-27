# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 18:53:15 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

LocalIndex indexes objects in 2 dimensions

TODO: use Rtrees, something faster
TODO: multiple dimensions
TODO: define an interface and change file names
"""

class LocalIndex(object):
    def __init__(self, _dim=2):
        self.dim = _dim
        self.objects = dict()
        
    def put(self, _id, _value):
        """ Updates or creates an object. """
        
        self.objects[_id] = _value
    
    def get(self, _min_value, _max_value):
        """ Returns all objects between _min_value and _max_value. """
        
        result = dict()
        for k in self.objects.keys():
            if  self.objects[k][0] >= _min_value[0] and\
                self.objects[k][1] >= _min_value[1] and\
                self.objects[k][0] < _max_value[0] and \
                self.objects[k][1] < _max_value[1]:
                    result[k]=self.objects[k]
        return result
    
    def remove(self, _id):
        """ Removes an object if it exists """
        if self.objects.get(_id):
            self.objects.pop(_id)
        
    def outside(self, _value):
        """ Checks if _value is outside the covered area. """
        
        if len(self.objects)==0:
            return False
        _min_value = (0,0)
        _max_value = (0,0)
        _min_value[0] = min(self.objects.values(), key=lambda o: o[0])
        _min_value[1] = min(self.objects.values(), key=lambda o: o[1])
        
        _max_value[0] = max(self.objects.values(), key=lambda o: o[0])
        _max_value[1] = max(self.objects.values(), key=lambda o: o[1])
        
        if  _value[0] < _min_value[0] or \
            _value[1] < _min_value[1] or \
            _value[0] > _max_value[0] or \
            _value[1] > _max_value[1]:
                return False
        
        return True
    
    def aggregate(self):
        _value = (sum((v[0] for v in self.objects.values())),sum((v[1] for v in self.objects.values())))
        if self.objects:
            _value = (_value[0]/len(self.objects), _value[1]/len(self.objects))
        return _value