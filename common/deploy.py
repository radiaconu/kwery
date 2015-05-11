# -*- coding: utf-8 -*-
"""
Created on Tue May  5 11:38:29 2015

@author: Raluca Diaconu (diaconu.raluca@gmail.com)
"""

# TODO: kill all, kill some, template?

import argparse, string
import os, stat
from ConfigParser import ConfigParser

import sys
sys.path.append('..')


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


interval = 2

class Node(object): 
    _addr = 'localhost'     # default
    _nb = 0                 # default
    
    interpreter = 'pypy'
    def write_config(self, _cfg):
        Node = self.__class__
        
        if not os.path.exists(Node.path + Node.configs_path):
            os.makedirs(Node.path + Node.configs_path)
            
        _cfg.write(open(Node.path + Peer.configs_path + self.config_file, 'w'))
        print "added config file", Node.path + Peer.configs_path + self.config_file
    
    @classmethod
    def make_start_file(Node):
        # read template
        try: # reading templates
            template_start_str = open(Node.template_file, 'r').read()
            start_ = open(Node.path + Node.start_file, 'w') # add path
            start_.write('#!/bin/sh\n')
        except Exception:
            print "Error reading templates"
            return
        
        # generate autorestart
        for p in Node._all:
            start_all_str = string.Template(template_start_str).safe_substitute(dict(
                name = Node.configs_path + p.config_file,
                interpreter = Node.interpreter))
            start_.write(start_all_str)
        
        os.chmod(Node.path + Node.start_file, stat.S_IRWXU| stat.S_IEXEC)
        print "added start file", start_
        print
    
class Peer(Node):
    path = '../peer/'
    configs_path = 'configs/'
    config_file = 'config_peer'
    start_file = 'start_peers.sh'
    template_file = 'template_start_peer'
    
    _all = list()
    
    def __init__(self, addr, i):
        self.addr = addr
        self.listenDispPort = peer_listenDispPort+i
        self.listenProxyPort = peer_listenProxyPort+i
        self.listenPeerPort = peer_listenPeerPort+i
        self.interval = interval
        self.config_file = Peer.config_file + str(i) + '.cfg'
        
        Peer._all.append(self)
        
    def make_config(self):
        _cfg = ConfigParser()
        _cfg.optionxform=str
        
        _cfg.add_section('Network')
        _cfg.set('Network', 'listenDispAddr',   str(self.addr) ) # local ip address of the peer
        _cfg.set('Network', 'listenDispPort',   str(self.listenDispPort) )
        _cfg.set('Network', 'connectDispAddr',  str(Disp._addr) )
        _cfg.set('Network', 'connectDispPort',   str(Disp.listenPeerPort) )
        
        _cfg.set('Network', 'listenPeerAddr',   str(self.addr) )
        _cfg.set('Network', 'listenPeerPort',   str(self.listenPeerPort) )
        
        _cfg.set('Network', 'listenProxyAddr',  str(self.addr) )
        _cfg.set('Network', 'listenProxyPort',  str(self.listenProxyPort) )
        
        _cfg.add_section('Timer')
        _cfg.set('Timer',   'interval', str(self.interval))
        
        self.write_config(_cfg)
        
    
class Disp(Node): 
    listenPeerPort = disp_listenPeerPort
    listenProxyPort = disp_listenProxyPort
    
    path = '../disp/'
    configs_path = 'configs/'
    config_file = 'config_disp'
    start_file = 'start_disp.sh'
    template_file = 'template_start_disp'
    
    _all = list()
    
    def __init__(self):
        self.addr = Disp._addr
        self.listenProxyPort = disp_listenProxyPort
        self.listenPeerPort = disp_listenPeerPort
        self.interval = interval
        self.config_file = Disp.config_file + '.cfg'
        
        Disp._all.append(self)
    
    def make_config(self):
        _cfg = ConfigParser()
        _cfg.optionxform=str
        
        _cfg.add_section('Network')
        
        _cfg.set('Network', 'listenPeerAddr',   str(self.addr) )
        _cfg.set('Network', 'listenPeerPort',   str(self.listenPeerPort) )
        
        _cfg.set('Network', 'listenProxyAddr',  str(self.addr) )
        _cfg.set('Network', 'listenProxyPort',  str(self.listenProxyPort) )
        
        _cfg.add_section('Timer')
        _cfg.set('Timer',   'interval', str(self.interval))
        
        self.write_config(_cfg)
        
class Proxy(Node): 
    path = '../proxy/'
    configs_path = 'configs/'
    config_file = 'config_proxy'
    start_file = 'start_proxies.sh'
    template_file = 'template_start_proxy'
    
    _all = list()
    
    def __init__(self, addr, i):
        self.addr = addr
        self.listenDispPort = proxy_listenDispPort+i
        self.listenProxyPort = proxy_listenProxyPort+i
        self.listenPeerPort = proxy_listenPeerPort+i
        self.interval = interval
        self.config_file = Proxy.config_file + str(i) + '.cfg'
        
        Proxy._all.append(self)
        
    def make_config(self):
        _cfg = ConfigParser()
        _cfg.optionxform=str
        
        _cfg.add_section('Network')
        _cfg.set('Network', 'listenDispAddr',   str(self.addr) ) # local ip address of the peer
        _cfg.set('Network', 'listenDispPort',   str(self.listenDispPort) )
        _cfg.set('Network', 'connectDispAddr',  str(Disp._addr) )
        _cfg.set('Network', 'connectDispPort',   str(Disp.listenProxyPort) )
        
        _cfg.set('Network', 'listenPeerAddr',   str(self.addr) )
        _cfg.set('Network', 'listenPeerPort',   str(self.listenPeerPort) )
        
        _cfg.set('Network', 'listenProxyAddr',  str(self.addr) )
        _cfg.set('Network', 'listenProxyPort',  str(self.listenProxyPort) )
        
        _cfg.add_section('Timer')
        _cfg.set('Timer',   'interval', str(interval))
        
        self.write_config(_cfg)
    

# TODO
class GlobalConfig(object):
    pass
    
def load_global_config(_config_file):
    """ Open the global config file and load all parameters
    """
    config = ConfigParser()
    config.read(_config_file)
    
    # reading arguments
    if 'Peer' in  config.sections():
        Peer._addr = config.get('Peer','peer_addr')
        Peer._nb = config.getint('Peer','nb_peers') 
    else:
        print 'No Peer section in %s file'%_config_file 
        
    if 'Proxy' in  config.sections():
        Proxy._addr = config.get('Proxy','proxy_addr')
        Proxy._nb = config.getint('Proxy','nb_proxies')
    else:
        print 'No Proxy section in %s file'%_config_file
    
    if 'Disp' in  config.sections():
        Disp._addr = config.get('Disp','disp_addr')
    else:
        print 'No Disp section in %s file'%_config_file
    
    if 'Other' in  config.sections():
        Peer.interpreter = Proxy.interpreter = Disp.interpreter = config.get('Other','interpreter')
        interval = config.get('Other','interval')
    

if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Deploy multiple nodes and proxies")
    argParser.add_argument('-c','--config', default="deploy_config.cfg",  help="Global config file; default deploy_config.cfg")

    args = argParser.parse_args()

    load_global_config(args.config)
    
    # disp
    Disp().make_config()
    
    Disp.make_start_file()
    
    # peers
    [Peer(Peer._addr, i) for i in range(Peer._nb)]    
    [p.make_config() for p in Peer._all]       
        
    Peer.make_start_file()
    
    # proxies
    [Proxy(Proxy._addr, i) for i in range(Proxy._nb)]    
    [p.make_config() for p in Proxy._all]       
        
    Proxy.make_start_file()
    
    

        
