from utils import data
import queue

MAX_SIZE=6

# class Dispatcher(object):
#     serv_queue = queue.PriorityQueue()
#     serv_size = 6
#     pend_queue = queue.PriorityQueue()
#     def __init__(self,serv_size=6):
#         assert(self.serv_queue.empty())
#         assert(self.pend_queue.empty())
#         self.serv_size=serv_size


def add(roomid):
    serv_queue = queue.PriorityQueue()
    for id, room in data.rooms.items():
        if room.val.status == data.Room.RUNNING:
            serv_queue.put((-room.val.srv_time,room.val.speed, id))
    if serv_queue.qsize() < MAX_SIZE:
        data.rooms[roomid].lock.acquire()
        data.rooms[roomid].val.set_status((data.Room.RUNNING))
        data.rooms[roomid].val.timer = data.Room.MAX_TIMER
        data.rooms[roomid].val.srv_time = 0
        data.rooms[roomid].lock.release()

    elif data.rooms[roomid].val.speed <= data.Room.MEDIUM:
        data.rooms[roomid].lock.acquire()
        data.rooms[roomid].val.set_status(data.Room.SUSPENDED)
        data.rooms[roomid].val.timer = data.Room.MAX_TIMER
        data.rooms[roomid].val.srv_time = 0
        data.rooms[roomid].lock.release()

    else:
        pop_id = serv_queue.get()[-1]
        data.rooms[pop_id].lock.acquire()
        data.rooms[pop_id].val.set_status(data.Room.SUSPENDED)
        data.rooms[pop_id].val.timer = data.Room.MAX_TIMER
        data.rooms[pop_id].lock.release()

        data.rooms[roomid].lock.acquire()
        data.rooms[roomid].val.set_status(data.Room.RUNNING)
        data.rooms[roomid].val.srv_time = 0
        data.rooms[roomid].lock.release()

def end(roomid):
    data.rooms[roomid].lock.acquire()
    data.rooms[roomid].val.set_status(data.Room.END)
    data.rooms[roomid].val.srv_time = 0
    data.rooms[roomid].lock.release()

    pend_queue = queue.PriorityQueue()
    for id, room in data.rooms.items():
        if room.val.status == data.Room.SUSPENDED:
            pend_queue.put((room.val.timer, id))

    if not pend_queue.empty():
        pend_id = pend_queue.get()[-1]
        data.rooms[pend_id].lock.acquire()
        data.rooms[pend_id].val.set_status(data.Room.RUNNING)
        data.rooms[pend_id].val.srv_time = 0
        data.rooms[pend_id].lock.release()

def timeup(roomid):
    serv_queue = queue.PriorityQueue()
    for id, room in data.rooms.items():
        if room.val.status == data.Room.RUNNING:
            serv_queue.put((-room.val.srv_time,room.val.speed, id))
    pop_id = serv_queue.get()[-1]
    data.rooms[pop_id].lock.acquire()
    data.rooms[pop_id].val.set_status(data.Room.SUSPENDED)
    data.rooms[pop_id].val.timer = data.Room.MAX_TIMER
    data.rooms[pop_id].lock.release()

    data.rooms[roomid].lock.acquire()
    data.rooms[roomid].set_status(data.Room.RUNNING)
    data.rooms[roomid].srv_time = 0
    data.rooms[roomid].lock.release()

def upwind(roomid):
    assert(data.rooms[roomid].val.speed>data.Room.MEDIUM)
    assert(data.rooms[roomid].val.status == data.Room.SUSPENDED)
    serv_queue = queue.PriorityQueue()
    for id, room in data.rooms.items():
        if room.val.status == data.Room.RUNNING:
            serv_queue.put((-room.val.srv_time,room.val.speed, id))

    pop_id = serv_queue.get()[-1]
    data.rooms[pop_id].lock.acquire()
    data.rooms[pop_id].val.set_status(data.Room.SUSPENDED)
    data.rooms[pop_id].val.timer = data.Room.MAX_TIMER
    data.rooms[pop_id].lock.release()

    data.rooms[roomid].lock.acquire()
    data.rooms[roomid].val.set_status(data.Room.RUNNING)
    data.rooms[roomid].val.srv_time = 0
    data.rooms[roomid].lock.release()

def reached(roomid):
    assert(data.rooms[roomid].val.status == data.Room.RUNNING)
    data.rooms[roomid].lock.acquire()
    data.rooms[roomid].val.set_status(data.Room.IDLE)
    data.rooms[roomid].val.srv_time = 0
    data.rooms[roomid].lock.release()

    pend_queue = queue.PriorityQueue()
    for id, room in data.rooms.items():
        if room.val.status == data.Room.SUSPENDED:
            pend_queue.put((room.val.timer, id))

    if not pend_queue.empty():
        pend_id = pend_queue.get()[-1]
        data.rooms[pend_id].lock.acquire()
        data.rooms[pend_id].val.set_status(data.Room.RUNNING)
        data.rooms[pend_id].val.srv_time = 0
        data.rooms[pend_id].lock.release()

