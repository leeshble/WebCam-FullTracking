from pythonosc import dispatcher
from pythonosc import osc_server

IP = "127.0.0.1"
PORT = 39570
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/VMT/Joint/Unity", print)
dispatcher.map("/VMT/Room/Unity", print)

server = osc_server.ThreadingOSCUDPServer((IP, PORT), dispatcher)

print("Serving on {}".format(server.server_address))
server.serve_forever()