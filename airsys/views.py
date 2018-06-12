from django.http import HttpRequest
from django.shortcuts import render

def index(request):
    ctx = {}
    a=50
    ctx['head1'] = 'World'
    ctx['head2'] = 'hello'
    ctx['body'] = a
    return render(request,'index.html',ctx)

def login(request):
    ctx = {}

def hotel_manager(request):
    pass

def ac_manage(request):
    pass

