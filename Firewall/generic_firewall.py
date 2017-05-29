#!/usr/bin/python
from pox.core import core
 
log = core.getLogger()
block_ips = set()
 
def block_handler (event):
  pakka = event.parsed
  ip_pakka = pakka.find('ipv4')
  if not ip_pakka:
    log.debug("Ikke en IP-pakke.")
    return
 
  if str(ip_pakka.srcip) in block_ips:
    log.debug("{} er en blokkert IP. Stoppes.".format(ip_pakka.srcip))
    event.halt = True
    return
  if str(ip_pakka.dstip) in block_ips:
    log.debug("{} er en blokkert IP. Snakkes.".format(ip_pakka.dstip))
    event.halt = True
    return
  log.debug("gjorde ingenting med pakka fra {} til {}".format(ip_pakka.srcip,ip_pakka.dstip))
 
 
def unblock (*iper):
  block_ips.difference_update(iper)
 
def block (*iper):
  block_ips.update(iper)
 
def launch (iper = ''):
  core.Interactive.variables['block'] = block
  core.Interactive.variables['unblock'] = unblock
 
  block('10.0.0.2')
 
  core.openflow.addListenerByName("PacketIn", block_handler)
