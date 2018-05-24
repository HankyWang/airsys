from django.shortcuts import render
from django.http import HttpRequest
import subprocess
import os,sys
import socket
import queue

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

def resolve(msg):
    item = msg.split(',')
    if item[0] == 'request':
        pass
    elif item[0] == 'update':
        pass
    elif item[0] == 'synchro':
        pass
    elif item[0] == 'end':
        pass
    else:
        pass


def handle_request(conn):
    msg = conn.recv(BUF_SIZE)
    # conn.send(msg)         #to client


def server(client):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST,PORT))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        handle_request(connection)


