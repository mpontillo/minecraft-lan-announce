#!/usr/bin/env python

import socket
import time
import sys
from scapy.all import *

conf.verb = 0

servers = [
    ["192.168.0.2", "Faraway Land - Testing", 25565],
]

MULTICAST_GROUP = "224.0.2.60"
MINECRAFT_PORT = 4445

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print "Broadcasting Minecraft servers to LAN..."

while True:
    for server in servers:
        packet = (
            IP(dst=MULTICAST_GROUP, src=server[0]) / 
            UDP(dport=MINECRAFT_PORT, sport=MINECRAFT_PORT) / 
            "[MOTD]{name}[/MOTD][AD]{port}[/AD]".format(
                name=server[1], port=server[2])
        )
        send(packet)
    time.sleep(1.5)
