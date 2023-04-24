#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# author: Madhav-MKNC (https://github.com/madhav-mknc/p2p-chatroom)

import socket
import threading

from utils import *
from constants import *



def Server():
    def __init__(self, addr=('localhost',3000)):
        self.addr = addr
        self.other_nodes = dict()

    def up(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print("[!] Failed to create a socket")
            print("[error]", str(e))

        self.sock.bind((self.ip))
        self.sock.listen(ROOM_LIMIT)
        print(f"[+] Waiting for Connections at {self.HOSTIP}:{self.PORT}")
        
        while True:
            client_sock, addr = self.sock.accept()
            client = Client(client_sock, addr)
            print(f"[+] New client connected from {addr}")
            threading.Thread(target=self.send_data, daemon=True, args=(client,)).start()
            # threading.Event().wait()
        
    def send_data(self, client):
        pass


    # # if type(self.other_nodes) == list()
    # def add_node(self, addr):
    #     if addr not in self.other_nodes and len(self.other_nodes) <= ROOM_LIMIT:
    #         self.other_nodes.append(addr)


    # Client(): INNER Class

    class Client:
        def __init__(self, client_sock, addr):
            self.sock = client_sock
            self.addr = addr
            self.name = ""
            self.other_nodes[self.sock] = self.addr
        
        def exists(self, name):
            # check the username if already active on the server (INNER CLASS implementation will fix this)
            return False

        def set_username(self):
            response = self.recv()
            if len(response)>0 and self.exists(response)==False:
                self.name = response
            else:
                self.name = get_username()
                self.send(f"[{self.HOSTNAME}] Username Invalid! You are {self.name}")
        
        def send_banner(self):
            banner = f"[ ---------- WELCOME TO THE '{self.HOSTNAME}' CHATROOM ---------- ]"
            self.send(banner)

        def send(self, message):
            try:
                self.sock.send(message.encode(ENCODING))
            except ConnectionError:
                print(f"[<{self.name}> DISCONNECTED!]")
                self.sock.close()

        def recv(self):
            try:
                data = self.sock.recv(BUFFERSIZE).decode(ENCODING)
                return data
            except ConnectionError:
                print(f"[<{self.name}> DISCONNECTED!]")
                self.sock.close()
        
        def send_messages(self):
            try:
                while True:
                    print(f"<{self.HOSTNAME} *> ",end="")
                    message = input().strip()
                    if len(message)==0: continue
                    if message=="shutdown":
                        print("[shutdown!]")
                        self.sock.close()
                        return
                    message = f"<{self.HOSTNAME} *> "+message
                    self.send(message)
            except Exception as e:
                print("[error]",str(e))
                self.sock.close()
                return 

        def recv_messages(self):
            try:
                while True:
                    data = self.recv()
                    if data: print(data)
            except Exception as e:
                print("[error]",str(e))
                self.sock.close()
                return


