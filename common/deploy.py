# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:38:29 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)
"""

import argparse, string
import os, stat
from ConfigParser import ConfigParser

import sys
sys.path.append('..')
from templates.runnable import Runnable


#unique ports
disp_listenPeerPort     = 8000
disp_listenProxyPort    = 8001

# starting ports
peer_listenProxyPort    = 7200
peer_listenDispPort     = 7300
peer_listenPeerPort     = 7400
proxy_listenProxyPort   = 7500
proxy_listenPeerPort    = 7600
proxy_listenDispPort    = 7700


configs_directory = './configs'

start_peers = '../peer/start_peer.sh'
start_proxies = '../proxy/start_proxies.sh'
start_disp = '../disp/start_disp.sh'

peer_config_files = []
proxy_config_files = []
disp_config_files = 'peer/config_disp'

config_fn_peers = 'peer/config_peer'
config_fn_proxies = 'peer/config_proxy'

timer = 2

class Node:    
    template_file = None
    def write_config(self):
        self.cfg.write(open(self.path+self.cfg_filename, 'w'))
        
    def make_start_file(self):
        # read template
        try: # reading templates
            template_start_str = open(self.__class__.template_file, 'r').read()
            start_file = open(self.__class__.start_file, 'w')
            autorestart_zone_file.write('#!/bin/sh\n')
        except Exception:
            print "Error reading templates"
            return
            
        if not os.path.exists(configs_directory):
            os.makedirs(configs_directory)
        
        # generate autorestart
        start_all_str = string.Template(template_start_str).safe_substitute(dict(
            name = self.cfg_filename))
        self.start_all_file.write(start_all_str)
        
        os.chmod(self.start_all_file, stat.S_IRWXU| stat.S_IEXEC)
        print "added", self.start_all_file
    
class Peer(Node):
    path = '../peer/'
    config_file = 'config_peer'
    start_file = 'start_peers.sh'
    template_file = 'template_start_peers.sh'
    
    def __init__(self, addr, listenDispPort, listenProxyPort, listenPeerPort):
        self.addr = addr
        self.listenDispPort = listenDispPort
        self.listenProxyPort = listenProxyPort
        self.listenPeerPort = listenPeerPort
        self.timer = timer
        self.cfg_filename = ' '
        
    def make_config(self):
        _cfg = ConfigParser.ConfigParser()
        _cfg.optionxform=str
        
        _cfg.add_section('Network')
        _cfg.set('Network', 'listenDispAddr',   str(self.addr) ) # local ip address of the peer
        _cfg.set('Network', 'listenDispPort',   str(self.listenDispPort) )
        _cfg.set('Network', 'connectDispAddr',  str(self.addr) )
        _cfg.set('Network', 'conectDispPort',   str(self.conectDispPort) )
        
        _cfg.set('Network', 'listenPeerAddr',   str(self.addr) )
        _cfg.set('Network', 'listenPeerPort',   str(self.listenPeerPort) )
        
        _cfg.set('Network', 'listenProxyAddr',  str(self.addr) )
        _cfg.set('Network', 'listenProxyPort',  str(self.listenProxyPort) )
        
        _cfg.add_section('Timer')
        _cfg.set('Timer',   'interval', str(self.timer))
        
        self.cfg = _cfg
    

class Proxy(Node): pass
class Disp(Node): pass
        

peer_addr = 'localhost'
disp_addr = 'localhost'
proxy_addr = 'localhost'
nb_peers = 0
nb_proxies = 0

def load_global_config(_config_file):
    """ Open the global config file and load all parameters
    """
    config = ConfigParser()
    config.read(_config_file)
    
    # reading arguments
    if 'Peer' in  config.sections():
        peer_addr = config.get('Peer','peer_addr')
        nb_peers = config.getint('Peer','nb_peers') 
    else:
        print 'No Peer section in %s file'%_config_file 
        
    if 'Proxy' in  config.sections():
        proxy_addr = config.get('Proxy','proxy_addr')
        nb_proxies = config.getint('Proxy','nb_proxies')
    else:
        print 'No Proxy section in %s file'%_config_file
    
    if 'Disp' in  config.sections():
        disp_addr = config.get('Disp','disp_addr')
    else:
        print 'No Disp section in %s file'%_config_file
    
    if 'Other' in  config.sections():
        interpreter = config.get('Other','interpreter')
        interval = config.get('Other','interval')
    

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Deploy multiple nodes and proxies")
    argParser.add_argument('-c','--config', default="deploy_config.cfg",  help="Global config file; default deploy_config.cfg")

    args = argParser.parse_args()

    load_global_config(args.config)
    
    
    peers = []
    for i in range(nb_peers):
        peers.append(Peer(peer_addr, 
                          peer_listenDispPort+i, 
                          peer_listenProxyPort+i, 
                          peer_listenPeerPort+i))
    proxies = []
    
    disp = None
    

        
