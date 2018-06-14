from django.http import HttpResponse
from django.shortcuts import render
from utils import data

windspeed = ['Low','Medium','High']
stats = ['','RUNNING','IDLE','END','SUSPENDED']




def dashboard(request):
    ctx={}
    for id, room in data.rooms.items():
        ctx['fee_'+id] = room.val.fee
        ctx['ener_'+id] = room.val.ener
        ctx['cur_temp_'+id] = room.val.cur_temp
        ctx['status_'+id] = stats[room.val.status]
        ctx['targ_temp_'+id] = room.val.targ_temp if room.val.status != data.Room.END else '-'
        ctx['srv_time_'+id] = room.val.srv_time if room.val.status == data.Room.RUNNING else '-'
        ctx['wait_time_'+id] = room.val.timer if room.val.status == data.Room.SUSPENDED else '-'

    return render(request,'dashboard.html',ctx)

def room(request):
    request.encoding = 'utf-8'
    ctx={}
    if request.GET:
        roomid = request.GET['id']
        for id in data.ROOM_IDS:
            if id==roomid:
                ctx['room'+str(roomid)] = 'active'
            else:
                ctx['room'+str(id)] = ''
        ctx['id']=roomid
        ctx['speed'] = windspeed[data.rooms[roomid].val.speed]
        ctx['cur_temp'] = data.rooms[roomid].val.cur_temp
        ctx['status'] = stats[data.rooms[roomid].val.status]
        ctx['fee'] = data.rooms[roomid].val.fee
        ctx['ener'] = data.rooms[roomid].val.ener
        ctx['targ_temp'] = data.rooms[roomid].val.targ_temp if data.rooms[roomid].val.status != data.Room.END else '-'
        ctx['srv_time'] = data.rooms[roomid].val.srv_time if data.rooms[roomid].val.status == data.Room.RUNNING else '-'
        ctx['wait_time'] = data.rooms[roomid].val.timer if data.rooms[roomid].val.status == data.Room.SUSPENDED else '-'
        ctx['logs'] = ''
    return render(request, '../templates/room.html', ctx)

def login(request):
    ctx = {}

def client(request):
    ctx = request.POST


def hotel_manager(request):
    pass

def ac_manage(request):
    pass

