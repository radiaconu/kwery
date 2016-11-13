# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:56:18 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

*Entry* Config loading file.

Required correctly formatted input file. 
Default value: 'configNodeDefault.cfg'
"""

import sys
sys.path.append('..')
from templates.config import Config

class ConfigEntry(Config):
    def __init__(self, _file = 'configEntryDefault.cfg'):
        
        from ConfigParser import ConfigParser
        
        parser = ConfigParser()
        parser.read(_file)
        
        assert 'Network' in  parser.sections(), 'No Network section in %s file'%_file
        self.listenClientAddr = parser.get('Network', 'listenClientAddr')
        self.listenClientPort = parser.getint('Network', 'listenClientPort')
        
        self.listenProxyAddr = parser.get('Network', 'listenProxyAddr')
        self.listenProxyPort = parser.getint('Network', 'listenProxyPort')
                
        assert 'Timer' in  parser.sections(), 'No Timer section in %s file'%_file
        self.interval = parser.getint('Timer', 'interval')
        
    