# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:26:23 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)

*Disp* Config loading file.

Required correctly formatted input file. 
Default value: 'configNodeDefault.cfg'

"""
import sys
sys.path.append('..')
from templates.config import Config

class ConfigDisp(Config):
    def __init__(self, _file = 'configDispDefault.cfg'):
        
        from ConfigParser import ConfigParser
        
        parser = ConfigParser()
        parser.read(_file)
        
        assert 'Network' in  parser.sections(), 'No Network section in %s file'%_file
        self.listenPeerAddr = parser.get('Network', 'listenPeerAddr')
        self.listenPeerPort = parser.getint('Network', 'listenPeerPort')
        
        self.listenProxyAddr = parser.get('Network', 'listenProxyAddr')
        self.listenProxyPort = parser.getint('Network', 'listenProxyPort')
        
        #self.listenVisualAddr = parser.get('Network', 'listenVisualAddr')
        #self.listenVisualPort = parser.getint('Network', 'listenVisualPort')
        
        #self.connectCoordAddr = parser.get('Network', 'connectCoordAddr')
        #self.connectCoordPort = parser.get('Network', 'connectCoordPort')
        
        assert 'Timer' in  parser.sections(), 'No Timer section in %s file'%_file
        self.interval = parser.getint('Timer', 'interval')
        
    