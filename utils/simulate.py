import time
from utils import data,dispatcher

stats=['','RUNNING','IDLE','END','SUSPENDED']

def print_status():
    print(' '.join([stats[room.val.status] for room in data.rooms.values()]))

def simulate():
    while True:
        for roomid,room in data.rooms.items():
            room.lock.acquire()
            if room.val.status == data.Room.RUNNING:
                room.val.update()
            if room.val.status == data.Room.SUSPENDED:
                room.val.tick()
            room.lock.release()

            if room.val.is_reached() and (room.val.status != data.Room.IDLE or room.val.status != data.Room.END):
                dispatcher.reached(roomid)
            if room.val.is_timeup() and room.val.status == data.Room.SUSPENDED:
                dispatcher.timeup(roomid)

            print_status()
            time.sleep(data.TIME_SLOT)