def act_like_switch (self, packet, packet_in):
    source_mac = packet.src
    destination_mac = packet.dst
    entry_port = packet_in.in_port
    self.mac_to_port[source_mac] = entry_port
 
    if destination_mac in self.mac_to_port:
        self.resend_packet(packet_in, self.mac_to_port[destination_mac])
        log.debug("""Forwarding. \nSource mac: {}\nDest mac:
        {}\nEntry port: {}""".strip().format(source_mac, destination_mac,
            entry_port))
 
    else:
        log.debug("""Flooding. \nSource mac: {}\nDest mac{}\nIn_port =
                {}""".strip().format(source_mac,destination_mac,entry_port))
        self.resend_packet(packet_in, of.OFPP_ALL)
