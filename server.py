# сервер на транспортном уровне
# hostname hog18:12345

import socket
import sys
import configparser
import select
import argparse

from PyQt5.QtNetwork import QTcpSocket
from PyQt5.QtWidgets import QPushButton, QWidget, QMainWindow, QAction, QApplication, \
    QInputDialog, QLCDNumber, QSlider, QVBoxLayout, QMessageBox, QDockWidget, \
    QFileDialog, QLayout, QGridLayout, QLineEdit, QTextEdit

# bind in socket - means server, в него передается адрес хоста и порт
# select.select(list socketov chtoby chitat, pisat, oshibki?) - возвратит готовые для чтения сокеты
# socket accept - узнать кто подключился
# recv in socket - получить сообщ от клиента
# argparse

# sock = socket.create_connection(('hog18', 12345))
# sock.send(b'oooooooooooooooooooo!')


# sock = socket.socket()
# sock.connect(('hog18', 12345))
# sock.send(b'QWEQWEQWE\n\tttt\n\t\t\tggg\n\n')
# data = sock.recv(12345)
# sock.close()
# print(data)
#
# sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock2.connect(('hog18', 12345))
# sock2.send(b'QWERTYUIOP\n\nn\\t\tt\dfjskjk\n\n')

# host, port, messages
# SEND vs SENDALL  ????????????????????


# сериализация - сохранение состояния
# десериализация - загрузка состояние
# pickle
# dump, load
# def create_config(path):
#     config = configparser.ConfigParser()
#     config.add_section("SERVER")
#     config.set("SERVER", "Localhost", "localhost")
#     config.set("SERVER", "Port", "9600")
#
#     with open(path, "w") as config_file:
#         config.write(config_file)
#
#
# def get_config(path):
#     config = configparser.ConfigParser()
#     config.read(path)
#     return config
#
#
# def get_setting(path, section, setting):
#     config = get_config(path)
#     value = config.get(section, setting)
#     return value
#
# path = "settings.ini"
# create_config(path)
# localhost = get_setting(path, 'SERVER', 'Localhost')
# port = int(get_setting(path, 'SERVER', 'Port'))
#
# sock = socket.socket()
# sock.bind((localhost, port))
# sock.listen(1)
# conn, adr = sock.accept()
#
# print 'connected:', adr
#
# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     conn.send(data)
#
# conn.close()


def send_message(host, port, message=' '):
    mysock = socket.socket()
    mysock.connect((host, port))
    mysock.send(bytes(message, encoding='utf-8'))


# send_message('hog18', 12345, b'LISTEN!')

# parser = argparse.ArgumentParser(description='CHATIK')
# parser.print_help()
# parser.add_argument('host', type=str)
# parser.add_argument('port', type=int)
# parser.add_argument('--message', '-m', type=str)
# parser.print_help()
# args = parser.parse_args()
# print(args)
# send_message(args.host, args.port, args.message)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        self.resize(600, 600)
        self.setWindowTitle('Chat')
        _win = Window()
        self.setCentralWidget(_win)

        self._sock = QTcpSocket()
        self._sock.connected.connect(self._connected)
        self._sock.connectToHost('hog18', 12345)

        self.statusBar()
        self.show()

    def _connected(self):
        self.statusBar().showMessage('connected')


#         self._sock.write(text.encode())


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self._input = QLineEdit()
        _layout = QGridLayout()
        _layout.setSpacing(5)    # расстояние между виджетами
        _layout.addWidget(self._input, 1, 0, 1, 1)

        self._input.returnPressed.connect(self.send_message)
        self._input.textChanged.connect(self._switch_enable_button)

        self._button = QPushButton('send', self)

        self._button.clicked.connect(self.send_message)
        _layout.addWidget(self._button, 1, 1, 1, 1)

        self._messages = QTextEdit()
        self._messages.setReadOnly(True)
        _layout.addWidget(self._messages, 0, 0, 1, 2)

        self.setLayout(_layout)

    def send_message(self):
        text = self._input.text()
        if not text:
            return
        self._messages.append(text)
        self._input.setText('')
        self._input.setFocus()

    def _switch_enable_button(self):
        if self._input.text():
            self._button.setEnabled(True)
        else:
            self._button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ChatWindow()
    win.show()
    sys.exit(app.exec_())