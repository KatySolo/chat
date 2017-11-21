from socket import *
import sys

host = 'localhost'
port = 9600
addr = (host,port)

udp_socket = socket(AF_INET, SOCK_DGRAM)


data = input('write to server: ')
if not data :
    udp_socket.close()
    sys.exit(1)

#encode - перекодирует введенные данные в байты, decode - обратно

data = str.encode(data)
udp_socket.sendto(data, addr)
data = bytes.decode(data)
data = udp_socket.recvfrom(1024)
print(data)


udp_socket.close()
