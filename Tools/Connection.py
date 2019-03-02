import json
import logging

from socket import *
from threading import Thread
from Config.Constants import ENCODING, RECEIVE_BUFFER_SIZE
from Decorators.LogDecorator import Log


class Connection(Thread):
    __slots__ = ['address', 'socket', 'received', 'logger', 'received_data']

    def __init__(self, address, socket, received):
        self.logger = logging.getLogger('connection')
        self.received_data = ""
        self.socket = socket
        self.address = address
        self.received = received
        Thread.__init__(self)

    def get_address(self):
        return self.address

    @Log()
    def send(self, data):
        try:
            send_data = str(json.dumps(data)).encode(ENCODING)
            self.socket.send(send_data)
            self.logger.debug("Передача: %s", send_data)
            return True
        except error:
            self.logger.error("Ошибка передачи: %s", error)
            return False

    def run(self):
        while self.isAlive():
            try:
                raw_data = []
                raw_data = self.socket.recv(RECEIVE_BUFFER_SIZE)
                if raw_data:
                    self.received_data += raw_data.decode(ENCODING)
            except error:
                if self.received_data != "":
                    json_frame = json.loads(self.received_data)
                    self.logger.debug("Прием: %s", self.received_data)
                    self.received(self, json_frame)
                    self.received_data = ""
