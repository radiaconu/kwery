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
        self.bc = (0,0)
        self.width = 0
        self.height = 0
        
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
     
    def barycenter(self):
        """ All indexed points barycenter """
        _value = (sum((v[0] for v in self.objects.values())),sum((v[1] for v in self.objects.values())))
        if self.objects:
            _value = (_value[0]/len(self.objects), _value[1]/len(self.objects))
        self.bc=_value
        return _value
    
    def get_bc(self):
        return self.bc
        
    def coverage(self):
        """ Returns the covered area as a tuple (_min_value, _max_value) """
        _min_value = (0,0)
        _max_value = (0,0)
        
        if self.objects:
            _min_value=(min(self.objects.values(), key=lambda o: o[0])[0], \
                        min(self.objects.values(), key=lambda o: o[1])[1])
            
            _max_value=(max(self.objects.values(), key=lambda o: o[0])[0],\
                        max(self.objects.values(), key=lambda o: o[1])[1])

        self.width = _max_value[0]-_min_value[0]
        self.height = _max_value[1]-_min_value[1]
        
        return (_min_value, _max_value)
    
    def get_width(self): return self.width
    def get_height(self): return self.height

    def is_covered(self, _value):
        """ Checks if _value is covered by the current area. """
        
        if len(self.objects)==0:
            return True
        
        _min_value, _max_value = self.coverage()
        
        if  _value[0] < _min_value[0] or \
            _value[1] < _min_value[1] or \
            _value[0] > _max_value[0] or \
            _value[1] > _max_value[1]:
                return False
        
        return True
    
    def is_indexed(self, _id):
        return self.objects.has_key(_id)
        
    def load(self):
        return len(self.objects)