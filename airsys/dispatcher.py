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
            self.serv_queue.put((-data.rooms[roomid].srv_time, data.rooms[roomid].speed, roomid))
            data.rooms[roomid].set_status((data.Room.RUNNING))
        elif data.rooms[roomid].speed<=data.Room.MEDIUM:
            self.pend_queue.put((data.rooms[roomid].timer, roomid))
            data.rooms[roomid].set_status(data.Room.SUSPENDED)
        else:
            pop_id = self.serv_queue.get()[-1]
            data.rooms[pop_id].timer = data.Room.MAX_TIMER
            self.pend_queue.put((data.rooms[pop_id].timer, pop_id))
            data.rooms[pop_id].set_status(data.Room.SUSPENDED)
            self.serv_queue.put((-data.rooms[roomid].srv_time, data.rooms[roomid].speed, roomid))
            data.rooms[roomid].set_status(data.Room.RUNNING)

