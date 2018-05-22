from django.shortcuts import render
from django.http import HttpRequest
import subprocess
import os,sys
import socket as soc

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