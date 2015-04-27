# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:26:23 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

*PRoxy* Config loading file.

Required correctly formatted input file. 
Default value: 'configProxyDefault.cfg'

TODO: Automatic config file generation
"""
import sys
sys.path.append('..')
from templates.config import Config

class ConfigProxy(Config):
    def __init__(self, _file = 'configProxyDefault.cfg'):
        
        from ConfigParser import ConfigParser
        
        parser = ConfigParser()
        parser.read(_file)
        
        assert 'Network' in  parser.sections(), 'No network section in %s file'%_file
        self.connectDispAddr = parser.get('Network', 'connectDispAddr')
        self.connectDispPort = parser.getint('Network', 'connectDispPort')
        
        self.listenPeerAddr = parser.get('Network', 'listenPeerAddr')
        self.listenPeerPort = parser.getint('Network', 'listenPeerPort')
        