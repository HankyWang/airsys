from django.shortcuts import render
from django.http import HttpRequest
import subprocess
import os,sys
import socket
import queue

class Handler(object):
    inbuf = queue.Queue()
    def __init__(self,RoomID,port):
        self.RoomID = RoomID
        self.port = port
    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)
            s.bind('',self.tcp_port)
            while True:
                data, addr = s.recvfrom(1024)
                msg = data.split(',')
                if msg[0] == 'request':
                    pass
                elif msg[0] == 'update':
                    pass
                elif msg[0] == 'sychro':
                    pass
                elif msg[0] == 'end':
                    pass


def stats():
    ctx = {}
    # ctx[]

def get_ip():
    return subprocess.check_output(
    	"ifconfig -a"
    	"|grep inet|"
    	"grep -v 127.0.0.1|"
    	"grep -v inet6|"
    	"awk '{print $2}'"
    	"|tr -d 'addr:'", shell=True).strip()

HOST = get_ip()
PORT = 8880
BUF_SIZE = 1024



def handle_request(conn):
    data = conn.recv(BUF_SIZE)
    # conn.send(msg)         #to client
    msg = data.split(',')
    if msg[0] == 'request':
        pass
    elif msg[0] == 'update':
        pass
    elif msg[0] == 'sychro':
        pass
    elif msg[0] == 'end':
        pass


def server(client):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',PORT))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        handle_request(connection)

