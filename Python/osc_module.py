from pythonosc import udp_client

# Set OSC client
client = udp_client.SimpleUDPClient('127.0.0.1', 39570)


def osc_send(index, enable, timeoffset, px, py, pz, qx, qy, qz, qw):
    print(f"{index}, {enable}, {timeoffset}, {px}, {py}, {pz}, {qx}, {qy}, {qz}, {qw}")
    client.send_message("/VMT/Room/Unity", [index, enable, timeoffset, px, py, pz, qx, qy, qz, qw])


def osc_send2(index, enable, timeoffset, px, py, pz, qx, qy, qz, qw, serial):
    print(f"{index}, {enable}, {timeoffset}, {px}, {py}, {pz}, {qx}, {qy}, {qz}, {qw}, {serial}")
    client.send_message("/VMT/Joint/Driver", [index, enable, timeoffset, px, py, pz, qx, qy, qz, qw, serial])
