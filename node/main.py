#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# author: Madhav-MKNC (https://github.com/madhav-mknc/p2p-chatroom)

import socket
import threading

from utils import *
from constants import *
from setup import HOST



import socket
import threading
import logging
import selectors
import signal
import collections

from constants import *
from setup import HOST


class Node:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(ROOM_LIMIT)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.socket, selectors.EVENT_READ, data=None)
        self.lock = threading.Lock()
        self.message_queue = collections.deque()
        self.running = True
        
        self.broadcast_thread = threading.Thread(target=self.broadcast_loop)
        self.broadcast_thread.start()
        
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        
    def __repr__(self):
        return f"Node({self.host}:{self.port})"
        
    def connect(self, node):
        try:
            sock = socket.create_connection(node, timeout=3)
            sock.setblocking(False)
            self.selector.register(sock, selectors.EVENT_READ, data=None)
            logging.info(f"Connected to {node}")
        except ConnectionRefusedError:
            logging.warning(f"Connection to {node} refused.")
        except socket.timeout:
            logging.warning(f"Connection to {node} timed out.")
        
    def disconnect(self, sock):
        addr = sock.getpeername()
        logging.info(f"Disconnected from {addr}")
        self.selector.unregister(sock)
        sock.close()
        
    def send(self, sock, message):
        try:
            sock.send(message.encode())
        except (ConnectionResetError, OSError):
            self.disconnect(sock)
        
    def broadcast(self, message):
        with self.lock:
            self.message_queue.append(message)
                
    def broadcast_loop(self):
        while self.running:
            try:
                message = self.message_queue.popleft()
            except IndexError:
                continue
            for key, _ in self.selector.get_map().items():
                if key.fileobj is not self.socket:
                    self.send(key.fileobj, message)
                
    def handle_connection(self, sock):
        addr = sock.getpeername()
        logging.info(f"Connected to {addr}")
        try:
            while self.running:
                data = sock.recv(BUFFERSIZE)
                if not data:
                    self.disconnect(sock)
                    break
                message = f"{addr[0]}:{addr[1]}: {data.decode(ENCODING)}"
                self.broadcast(message)
        except (ConnectionResetError, OSError):
            self.disconnect(sock)
    
    def start(self):
        while self.running:
            events = self.selector.select(timeout=1)
            for key, mask in events:
                if key.fileobj is self.socket:
                    conn, addr = self.socket.accept()
                    conn.setblocking(False)



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
