# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:26:23 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

*Node* Config loading file.

Required correctly formatted input file. 
Default value: 'configNodeDefault.cfg'

TODO: Automatic config file generation
TODO: automatic port selection if it's not working
TODO: check if listen ports are open
"""
import sys
sys.path.append('..')
from templates.config import Config

class ConfigPeer(Config):
    def __init__(self, _file='configNodeDefault.cfg'):
        
        from ConfigParser import ConfigParser
        
        parser = ConfigParser()
        parser.read(_file)
        
        assert 'Network' in  parser.sections(), 'No network section in %s file'%_file
        self.connectDispAddr = parser.get('Network', 'connectDispAddr')
        self.connectDispPort = parser.getint('Network', 'connectDispPort')
        
        self.listenDispAddr = parser.get('Network', 'listenDispAddr')
        self.listenDispPort = parser.getint('Network', 'listenDispPort')
        
        self.listenProxyAddr = parser.get('Network', 'listenProxyAddr')
        self.listenProxyPort = parser.getint('Network', 'listenProxyPort')
        
        # Other variales. SYSTEM GLOBAL 
        self.UPDATE_INTERVAL = 2
        