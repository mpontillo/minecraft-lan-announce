#!/usr/bin/env python

import re
import sys
import select
import socket
import struct
import time

port = 4445
bufferSize = 1500
timeout = 6.5
MCAST_GRP = '224.0.2.60'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
s.bind(('', port))
s.setblocking(0)

servers = set()
start_time = time.time()

while True:
    current_time = time.time()
    (read, written, exceptions) = select.select([s],[],[s], 0.5)
    for r in read:
        msg, peer = r.recvfrom(bufferSize) 
        # address is an (address, port) tuple
        address = peer[0]
        matches = re.findall(r'\[MOTD\](.+?)\[/MOTD\]\[AD\](\d+)\[/AD\]', msg)
        for title, port in matches:
            server = address + ":" + port + ' ' + repr(title)
            if server not in servers:
                servers.add(server)
                print("[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"),  server))
    if len(exceptions) > 0 or current_time < start_time:
        sys.exit(1)
    if current_time >= start_time + timeout:
        sys.exit(0)
