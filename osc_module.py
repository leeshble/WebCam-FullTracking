from pythonosc import udp_client

# Set OSC client
client = udp_client.SimpleUDPClient('127.0.0.1', 39570)


def osc_send(index, enable, timeoffset, px, py, pz, qx, qy, qz, qw):
    print(f"{index}, {enable}, {timeoffset}, {px}, {py}, {pz}, {qx}, {qy}, {qz}, {qw}")
    client.send_message("/VMT/Room/Unity", [index, enable, timeoffset, px, py, pz, qx, qy, qz, qw])
