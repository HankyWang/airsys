import queue
import socket
import subprocess
import threading
from utils import dispatcher, data, simulate

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
    def __init__(self,roomid,port):
        self.roomid = roomid
        self.port = port
    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('',self.port))
            s.listen(1)
            con, addr = s.accept()
            print('[LOG]recieve connection from',addr)
            while True:
                msg = con.recv(BUF_SIZE)
                msg = msg.decode()
                msg = msg.split(',')
                if msg[0] == 'request':
                    roomid = msg[1]
                    wind = int(msg[2]) // 40
                    cur_temp = float(msg[3])
                    print('[LOG]REQUEST', roomid, wind, cur_temp)
                    dispatcher.add(roomid)
                    if data.rooms[roomid].val.status == data.Room.RUNNING:
                        data.rooms[roomid].lock.acquire()
                        data.rooms[roomid].val.cur_temp = cur_temp
                        data.rooms[roomid].val.speed = wind
                        data.rooms[roomid].lock.release()
                        con.send('sev_allow'.encode())
                        print('[LOG]SERVICE START')
                    else:
                        assert(data.rooms[roomid].val.status == data.Room.SUSPENDED)
                        con.send('wait'.encode())
                        print('[LOG]SERVICE OVERLOAD. PENDING...')
                elif msg[0] == 'update':
                    roomid = msg[1]
                    wind = int(msg[2] // 40)
                    targ_temp = float(msg[3])
                    cur_temp = float(msg[4])
                    if wind > data.Room.MEDIUM and data.rooms[roomid].val.status == data.Room.SUSPENDED:
                        dispatcher.upwind()
                        assert(data.rooms[roomid].val.status==data.Room.RUNNING)
                    data.rooms[roomid].lock.acquire()
                    data.rooms[roomid].val.cur_temp = cur_temp
                    data.rooms[roomid].val.speed = wind
                    data.rooms[roomid].val.targ_temp = targ_temp
                    data.rooms[roomid].lock.release()
                    con.send('running'.encode())
                    print('[LOG]UPDATE',roomid,'TARGET TEMP:',targ_temp,'WINDSPEED', ('LOW','MEDIUM','HIGH')[wind])
                elif msg[0] == 'synchro':
                    roomid = msg[1]
                    con.send(data.rooms[roomid].val.synchro().encode())
                    print('[LOG]SYNCHRO COMPLETE')
                elif msg[0] == 'end':
                    roomid = msg[1]
                    dispatcher.end(roomid)
                    con.send('end_allow'.encode())
                    print('[LOG]SERVICE END')

servers = [Handler(data.ROOM_IDS[i],data.ROOM_PORT[i]) for i in range(len(data.ROOM_IDS))]

if __name__ == '__main__':

    print(get_ip().decode())
    servers_th_pool = [threading.Thread(target=server.listen,args=(),name='server '+server.roomid).start() for server in servers]

    simulate_th = threading.Thread(target=simulate.simulate(), args=(), name='update').start()





# def server(client):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind(('',PORT))
#     sock.listen(5)
#
#     while True:
#         connection, address = sock.accept()
#         handle_request(connection)

