#!/usr/bin/env python

import socket
import time

servers = [
    ["Local Network - Survival Peaceful", 25565],
    ["Local Network - Survival Normal", 25566],
    ["Local Network - Survival Hard with Diamonds", 25567],
]

# BROADCAST_IP = "255.255.255.255"
BROADCAST_IP = "224.0.2.60"
BROADCAST_PORT = 4445

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print "Broadcasting Minecraft servers to LAN..."

while 1:
    for server in servers:
        msg = "[MOTD]%s[/MOTD][AD]%d[/AD]" % (server[0], server[1])
        sock.sendto(msg, (BROADCAST_IP, BROADCAST_PORT))
    time.sleep(1.5)
