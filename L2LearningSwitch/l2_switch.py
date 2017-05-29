def act_like_switch (self, packet, packet_in):
 
    source_mac = packet.src
    destination_mac = packet.dst
    entry_port = packet_in.in_port
 
    if source_mac not in self.mac_to_port or entry_port != self.mac_to_port[source_mac]:
        log.debug("Lager ny regel as; {} gaar naa til {}".format(source_mac,entry_port))
        self.mac_to_port[source_mac] = entry_port
    
    if destination_mac in self.mac_to_port:
        log.debug("Sender fra {} til {} gjennom port {}".format(source_mac, destination_mac, entry_port))
        
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.buffer_id = packet_in.buffer_id
        msg.in_port = entry_port
        
        action = of.ofp_action_output(port = self.mac_to_port[destination_mac])
        msg.actions.append(action)
 
        self.connection.send(msg)
    else:
        log.debug("Flooder litt jeg, hehe.")
        msg = of.ofp_flow_mod()
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        msg.match = of.ofp_match.from_packet(packet)
        self.connection.send(msg)
