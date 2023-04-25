#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# author: Madhav-MKNC (https://github.com/madhav-mknc/p2p-chatroom)

import socket
import threading

from utils import *
from constants import *
from setup import HOST


class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(ROOM_LIMIT)
        self.connections = []
        self.lock = threading.Lock()
        
    def connect(self, node):
        self.socket.connect(node)
        self.connections.append(self.socket)
        
    def broadcast(self, message):
        with self.lock:
            for conn in self.connections:
                conn.send(message.encode())
    
    def handle_connection(self, conn, addr):
        with conn:
            while True:
                data = conn.recv(BUFFERSIZE)
                if not data:
                    break
                message = f"{addr}: {data.decode(ENCODING)}"
                self.broadcast(message)
    
    def start(self):
        while True:
            conn, addr = self.socket.accept()
            threading.Thread(target=self.handle_connection, args=(conn, addr)).start()

nodes = [
    Node("localhost", 3000),
    Node("localhost", 3001),
    Node("localhost", 3002),
    Node("localhost", 3003),
    Node("localhost", 3004)
]

for i, node in enumerate(nodes):
    for j in range(i+1, len(nodes)):
        node.connect((nodes[j].host, nodes[j].port))
        nodes[j].connect((node.host, node.port))

for node in nodes:
    threading.Thread(target=node.start).start()
