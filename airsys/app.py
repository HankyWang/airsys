import queue
import socket
import subprocess

from utils import dispatcher, data

def get_ip():
    return subprocess.check_output(
    	"ifconfig -a"
    	"|grep inet|"
    	"grep -v 127.0.0.1|"
    	"grep -v inet6|"
    	"awk '{print $2}'"
    	"|tr -d 'addr:'", shell=True).strip()

HOST = get_ip()

BUF_SIZE = 1024

class Handler(object):
    def __init__(self,RoomID,port):
        self.RoomID = RoomID
        self.port = port
    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('',self.port))
            s.listen(1)
            con, addr = s.accept()
            while True:
                msg = s.recv(BUF_SIZE)
                msg = msg.split(',')
                if msg[0] == 'request':
                    roomid = msg[1]
                    wind = msg[2] // 40
                    cur_temp = msg[3]
                    dispatcher.add(roomid)
                    if data.rooms[roomid].val.status == data.Room.RUNNING:
                        data.rooms[roomid].lock.acquire()
                        data.rooms[roomid].val.cur_temp = cur_temp
                        data.rooms[roomid].val.speed = wind
                        data.rooms[roomid].lock.release()
                        con.send('sev_allow')
                    else:
                        assert(data.rooms[roomid].val.status == data.Room.SUSPENDED)
                        con.send('wait')
                elif msg[0] == 'update':
                    roomid = msg[1]
                    wind = msg[2] // 40
                    targ_temp = msg[3]
                    cur_temp = msg[4]
                    if wind > data.Room.MEDIUM and data.rooms[roomid].val.status == data.Room.SUSPENDED:
                        dispatcher.upwind()
                        assert(data.rooms[roomid].val.status==data.Room.RUNNING)
                    data.rooms[roomid].lock.acquire()
                    data.rooms[roomid].val.cur_temp = cur_temp
                    data.rooms[roomid].val.speed = wind
                    data.rooms[roomid].val.targ_temp = targ_temp
                    data.rooms[roomid].lock.release()
                    con.send('wait')
                elif msg[0] == 'sychro':
                    roomid = msg[1]
                    con.send(data.rooms[roomid].val.synchro())
                elif msg[0] == 'end':
                    roomid = msg[1]
                    dispatcher.end(roomid)
                    con.send('end_allow')

servers = [Handler(data.ROOM_IDS[i],data.ROOM_PORT[i]) for i in range(len(data.ROOM_IDS))]

if __name__ == '__main__':
    servers[0].listen()





# def server(client):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind(('',PORT))
#     sock.listen(5)
#
#     while True:
#         connection, address = sock.accept()
#         handle_request(connection)

