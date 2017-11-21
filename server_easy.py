import socket
import configparser

path = "settings.ini"


def create_config(path):
    config = configparser.ConfigParser()
    config.add_section("SERVER")
    config.set("SERVER", "Localhost", "localhost")
    config.set("SERVER", "Port", "9600")

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    config = get_config(path)
    value = config.get(section, setting)
    return value


create_config(path)
localhost = get_setting(path, 'SERVER', 'Localhost')
port = int(get_setting(path, 'SERVER', 'Port'))

sock = socket.socket()
sock.bind((localhost, port))
sock.listen(1)
conn, adr = sock.accept()

print('connected:', adr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.send(data)

conn.close()
