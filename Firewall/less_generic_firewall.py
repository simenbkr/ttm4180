#!/usr/bin/python
from pox.core import core
from time import time
log = core.getLogger()
block_ip_src = set()
block_ip_dst = set()
h1 = "10.0.0.1"
hosts_pinged = {}
def block_handler (event):
  pakka = event.parsed
  ip_pakka = pakka.find('ipv4')
  if not ip_pakka:
    log.debug("Ikke en IP-pakke.")
    return
 
  if h1 not in [str(ip_pakka.srcip), str(ip_pakka.dstip)]:
    #Ikke lov ifht reglene fra ppt.
    event.halt = True
    log.debug("Stoppet en pakke fra {} til {}".format(ip_pakka.srcip, ip_pakka.dstip))
    return
 
  if h1 == str(ip_pakka.srcip):
    hosts_pinged[str(ip_pakka.dstip)] = time()
    log.debug("Slipper igjen en pakke fra {}".format(h1))
    return
 
  if h1 == str(ip_pakka.dstip) and str(ip_pakka.srcip) in hosts_pinged and time() - hosts_pinged[str(ip_pakka.srcip)] < 60:
    log.debug("Slapp igjennom en respons til h1 fra {}".format(ip_pakka.srcip))
    log.debug(hosts_pinged)
    return
  else:
    log.debug("Stoppet en pakke fra {} til {}".format(ip_pakka.srcip, ip_pakka.dstip))
    event.halt = True
 
def unblock_src (*iper):
  block_ip_src.difference_update(iper)
 
def block_src (*iper):
  block_ip_src.update(iper)
 
def block_dst(*iper):
  block_ip_dst.update(iper)
 
def unblock_dst(*iper):
  block_ip_dst.difference_update(iper)
 
def launch (iper = ''):
  core.Interactive.variables['block_src'] = block_src
  core.Interactive.variables['unblock_src'] = unblock_src
 
  core.Interactive.variables['block_dst'] = block_dst
  core.Interactive.variables['unblock_dst'] = unblock_dst
 
  h1 = '10.0.0.1'
  block_src('10.0.0.2','10.0.0.3')
  block_dst('10.0.0.2','10.0.0.3')
 
  core.openflow.addListenerByName("PacketIn", block_handler)
