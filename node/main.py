#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# author: Madhav-MKNC (https://github.com/madhav-mknc/p2p-chatroom)

import socket
import threading

from collections import deque
from queue import Queue

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
        self.connections = deque()
        self.lock = threading.Lock()
        self.message_queue = Queue()
        self.threads = []
        self.running = True
        
        self.broadcast_thread = threading.Thread(target=self.broadcast_loop)
        self.broadcast_thread.start()
        
    def connect(self, node):
        try:
            sock = socket.create_connection(node, timeout=3)
            with self.lock:
                self.connections.append(sock)
                thread = threading.Thread(target=self.handle_connection, args=(sock,))
                self.threads.append(thread)
                thread.start()
        except ConnectionRefusedError:
            print(f"Connection to {node} refused.")
        except socket.timeout:
            print(f"Connection to {node} timed out.")
        
    def disconnect(self, node):
        with self.lock:
            for sock in self.connections:
                if sock.getpeername() == node:
                    self.connections.remove(sock)
                    sock.close()
                    break
        
    def send(self, node, message):
        for sock in self.connections:
            if sock.getpeername() == node:
                sock.send(message.encode())
                break
        
    def broadcast(self, message):
        self.message_queue.put(message)
                
    def broadcast_loop(self):
        while self.running:
            try:
                message = self.message_queue.get(timeout=1)
            except:
                continue
            with self.lock:
                for conn in self.connections:
                    try:
                        conn.send(message.encode())
                    except:
                        self.disconnect(conn.getpeername())
                
    def handle_connection(self, conn):
        with conn:
            while self.running:
                try:
                    data = conn.recv(BUFFERSIZE)
                except:
                    self.disconnect(conn.getpeername())
                    break
                if not data:
                    self.disconnect(conn.getpeername())
                    break
                message = f"{conn.getpeername()[0]}:{conn.getpeername()[1]}: {data.decode(ENCODING)}"
                self.broadcast(message)
    
    def start(self):
        while self.running:
            conn, addr = self.socket.accept()
            with self.lock:
                self.connections.append(conn)
                thread = threading.Thread(target=self.handle_connection, args=(conn,))
                self.threads.append(thread)
                thread.start()
    
    def stop(self):
        self.running = False
        with self.lock:
            for conn in self.connections:
                conn.close()
            for thread in self.threads:
                thread.join()



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
