import logging
from threading import Thread


def new_connect(address, socket):
    pass


class Listener(Thread):
    __slots__ = ['socket', 'new_connect', 'new_connect', 'logger']

    def __init__(self, socket, new_connect):
        self.logger = logging.getLogger('listener')
        self.socket = socket
        self.new_connect = new_connect
        Thread.__init__(self)

    def run(self):
        self.logger.info("Ожидание подключения")
        while self.isAlive():
            new_socket, address = self.socket.accept()
            new_socket.setblocking(0)
            self.logger.info("Установлено подключение")
            self.new_connect(address, new_socket)
