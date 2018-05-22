import threading


ROOM_NUM = 4
max_temp = 28
min_temp = 16
def_temp = 30

COOL = 0
HEAT = 1
mode = COOL


class Room:

    # Status
    IDLE = 0
    RUNNING = 1
    SUSPENDED = 2
    DISCONNECTED = 3

    # Wind Speed
    LOW = 0
    MEDIUM = 1
    HIGH = 2

    def __init__(
            self,
            id,
            is_checkin,
            is_connected,
            status,

    ):
        pass


