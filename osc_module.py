from pythonosc import udp_client

client = udp_client.SimpleUDPClient('127.0.0.1', 39570)


class Transform:
    def __init__(self, position_x=0., position_y=0., position_z=0., rotate_x=0., rotate_y=0., rotate_z=0., w=0.):
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z
        self.rotate_x = rotate_x
        self.rotate_y = rotate_y
        self.rotate_z = rotate_z
        self.w = w


# Tracking device
class Device:
    def __init__(self, index=1, enable=1, serial=''):
        self.index = index
        self.enable = enable
        self.serial = serial    #Device Name

        self.Transform = Transform()

    def send_osc(self):
        timeoffset = 0.
        client.send_message('/VMT/Joint/Unity', [self.index, self.enable, timeoffset,
                                                 self.Transform.position_x,
                                                 self.Transform.position_y,
                                                 self.Transform.position_z,
                                                 self.Transform.rotate_x,
                                                 self.Transform.rotate_y,
                                                 self.Transform.rotate_z,
                                                 self.Transform.w,
                                                 self.serial])

    def set_transform(self, position_x, position_y, position_z, rotate_x, rotate_y, rotate_z, w):
        self.Transform.position_x = position_x
        self.Transform.position_y = position_y
        self.Transform.position_z = position_z
        self.Transform.rotate_x = rotate_x
        self.Transform.rotate_y = rotate_y
        self.Transform.rotate_z = rotate_z
        self.Transform.w = w

class Room:
    def __init__(self, index, enable, transform, serial):
        self.index = index
        self.enable = enable
        self.transform = transform
        self.serial = serial

    def send_osc(self):
        client.send_message('/VMT/Room/Unity', [self.index, self.enable, 0., self.serial])
