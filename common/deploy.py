# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:38:29 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)
"""

import argparse, ConfigParser, string
import os, stat

import sys
sys.path.append('..')
from templates.runnable import Runnable


addresses = dict(
    localhost = "127.0.0.1"
)

# starting ports
z2z = 7200
z2p = 7300
z2d = 7400
z2m = 7500

configs_directory = './configs'

start_peers = 'peer/start_peer.sh'
start_proxies = 'proxy/start_proxies.sh'
start_disp = 'disp/start_disp.sh'

peer_config_files = []
proxy_config_files = []
disp_config_files = 'peer/config_disp'

config_fn_peers = 'peer/config_peer'
config_fn_proxies = 'peer/config_proxy'

timer = 2

class Node:    
    template = None
    def write_config(self):
        self.cfg.write(open(self.cfg_filename, 'w'))
        
    def make_start_file(self):
        # generate autorestart
        start_all_str = string.Template(self.template_file).safe_substitute(dict(
            name = self.cfg_filename))
        self.start_all_file.write(start_all_str)
        
        os.chmod(self.start_all_file, stat.S_IRWXU| stat.S_IEXEC)
        print "added", self.start_all_file
    
class Peer(Node):
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
    config = ConfigParser()
    config.read(_config_file)
    
    # reading arguments
    if 'Peer' in  config.sections():
        peer_addr = config.get('Peer','peer_addr')
        nb_peers = config.getint('Peer','nb_peers') 
    else:
        print 'No Peer section in %s file'%_config_file 
        
    if 'Proxy' in  config.sections():
        proxy_addr = config.get('Proxy','disp_addr')
        nb_proxies = config.getint('Proxy','nb_proxies')
    else:
        print 'No Proxy section in %s file'%_config_file
    
    if 'Disp' in  config.sections():
        disp_addr = config.get('Disp','disp_addr')
    else:
        print 'No Disp section in %s file'%_config_file
    

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Deploy multiple nodes and proxies")
    argParser.add_argument('-c','--config', default="config.cfg",  help="Global config file; default config.cfg")

    args = argParser.parse_args().config

    load_global_config()
    peers = []
    for i in range(nb_peers):
        peers.append(Peer(peer_addr, 
                          peer_listenDispPort+i, 
                          peer_listenProxyPort+i, 
                          peer_listenPeerPort+i))
    proxies = []
    
    disp = None
    
    try: # reading templates
        template_autorestart_zone = open('template_autorestart_zone.sh', 'r').read()
        autorestart_zone_file = open(autorestart_zone, 'w')
        autorestart_zone_file.write('#!/bin/sh\n')
    except Exception:
        print "Error reading templates"
        exit
        
    if not os.path.exists(configs_directory):
        os.makedirs(configs_directory)
    

        
