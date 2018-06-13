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

# def add(self, roomid):
    #     if self.serv_queue.qsize()<6:
    #         #lock
    #         data.rooms[roomid].lock.acquire()
    #         #put into serve queue
    #         self.serv_queue.put((-data.rooms[roomid].val.srv_time, data.rooms[roomid].val.speed, roomid))
    #         data.rooms[roomid].set_status((data.Room.RUNNING))
    #         #release
    #         data.rooms[roomid].lock.release()
    #     elif data.rooms[roomid].speed<=data.Room.MEDIUM:
    #         # lock
    #         data.rooms[roomid].lock.acquire()
    #         self.pend_queue.put((data.rooms[roomid].timer, roomid))
    #         data.rooms[roomid].set_status(data.Room.SUSPENDED)
    #         # release
    #         data.rooms[roomid].lock.release()
    #     else:
    #         pop_id = self.serv_queue.get()[-1]
    #         # lock
    #         data.rooms[pop_id].lock.acquire()
    #         data.rooms[pop_id].timer = data.Room.MAX_TIMER
    #         data.rooms[pop_id].srv_time = 0
    #         self.pend_queue.put((data.rooms[pop_id].timer, pop_id))
    #         data.rooms[pop_id].set_status(data.Room.SUSPENDED)
    #         # release
    #         data.rooms[pop_id].lock.release()
    #         # lock
    #         data.rooms[roomid].lock.acquire()
    #         self.serv_queue.put((-data.rooms[roomid].srv_time, data.rooms[roomid].speed, roomid))
    #         data.rooms[roomid].set_status(data.Room.RUNNING)
    #         # release
    #         data.rooms[roomid].lock.release()

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
    assert(data.rooms[roomid].speed>data.Room.MEDIUM)
    assert(data.rooms[roomid].status == data.Room.SUSPENDED)
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

# TODO: + end(roomid) + timeup(roomid) + upwind(roomid)