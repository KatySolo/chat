import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("message", help="message that you want to send", type=str)
parser.add_argument("--server", help="name of server to connect")
parser.add_argument("--port", help="number of port to connect", type=int)
args = parser.parse_args()

sock = socket.socket()
sock.connect((args.server, int(args.port)))
sock.send(args.message)

data = sock.recv(1024)
sock.close()

print(data)
