from . import data
import queue

class Dispatcher(object):
    serv_queue = queue.PriorityQueue()
    serv_size = 6
    pend_queue = queue.PriorityQueue()
    def __init__(self,serv_size=6):
        assert(self.serv_queue.empty())
        assert(self.pend_queue.empty())
        self.serv_size=serv_size

    def add(self, roomid):
        if self.serv_queue.qsize()<6:
            #lock
            data.rooms[roomid].lock.acquire()
            #put into serve queue
            self.serv_queue.put((-data.rooms[roomid].val.srv_time, data.rooms[roomid].val.speed, roomid))
            data.rooms[roomid].set_status((data.Room.RUNNING))
            #release
            data.rooms[roomid].lock.release()
        elif data.rooms[roomid].speed<=data.Room.MEDIUM:
            # lock
            data.rooms[roomid].lock.acquire()
            self.pend_queue.put((data.rooms[roomid].timer, roomid))
            data.rooms[roomid].set_status(data.Room.SUSPENDED)
            # release
            data.rooms[roomid].lock.release()
        else:
            pop_id = self.serv_queue.get()[-1]
            # lock
            data.rooms[pop_id].lock.acquire()
            data.rooms[pop_id].timer = data.Room.MAX_TIMER
            self.pend_queue.put((data.rooms[pop_id].timer, pop_id))
            data.rooms[pop_id].set_status(data.Room.SUSPENDED)
            # release
            data.rooms[pop_id].lock.release()
            # lock
            data.rooms[roomid].lock.acquire()
            self.serv_queue.put((-data.rooms[roomid].srv_time, data.rooms[roomid].speed, roomid))
            data.rooms[roomid].set_status(data.Room.RUNNING)
            # release
            data.rooms[roomid].lock.release()

# TODO: + end(roomid) + timeup(roomid) + upwind(roomid) + reach_target(roomid)