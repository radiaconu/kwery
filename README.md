# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Kwery. Scalable reverse geocoding
Cloud-based

* Version
0.0

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Deployment instructions


The system is ready to use with default configuration: one peer, one proxy, one disp.
All run on localhost. 
```
#!bash
$cd disp
$python disp.py
$cd peer
$python peer.py
$cd proxy
$python proxy.py
```
To deploy multiple instances generate config files for disp, peers, and proxies. Edit the deploy_config.cfg file.
```
#!bash
$cd common
$python deploy.py
```
* How to run tests

The order is not mandatory
```
#!bash
$cd disp
$./start_disp.sh
$cd peer
$./start_peers.sh
$cd proxy
$./start_proxies.sh
```

### Who do I talk to? ###

* Raluca Diaconu (diaconu.raluca@gmail.com)