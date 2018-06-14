from django.http import HttpResponse
from django.shortcuts import render
from utils import data

windspeed = ['Low','Medium','High']



def index(request):
    ctx = {}
    a=50
    ctx['head1'] = data.rooms['501'].val.id
    ctx['head2'] = data.rooms['501'].val.fee
    return render(request,'index.html',ctx)

def dashboard(request):
    ctx = {}

def room(request):
    request.encoding = 'utf-8'
    ctx={}
    if request.GET:
        roomid = request.GET['id']
        ctx['id']=roomid
        ctx['speed'] = data.rooms[roomid].val.speed
        ctx['cur_temp'] = data.rooms[roomid]

    return HttpResponse(str(roomid))

def login(request):
    ctx = {}

def client(request):
    ctx = request.POST


def hotel_manager(request):
    pass

def ac_manage(request):
    pass

