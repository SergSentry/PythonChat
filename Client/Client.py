import logging
from socket import *

from Protocol.Fields import *
from Protocol.Response import GOOD_RESPONSE_COD
from Tools.Connection import Connection


class Client:
    __slots__ = ['address', 'user_name', 'socket', 'connection', 'logger']

    def __init__(self, address, user_name):
        self.logger = logging.getLogger('client')
        self.address = address
        self.user_name = user_name
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.connect(address)
            self.socket.setblocking(0)
            self.connection = Connection(self.address, self.socket, self.received_data)
            self.connection.start()
        except error:
            self.logger.error("Ошибка инициализации клиента: %s", error)

    def __del__(self):
        self.connection.join(1000)
        self.socket.close()

    def received_data(self, connection, data):
        if RESPONSE in data and data[RESPONSE] == GOOD_RESPONSE_COD:
            print("\nРегистрация выполнена")
            return
        if MESSAGE in data and data[TO] == self.user_name:
            print("\nВходящее сообщение от " + str(data[FROM]).strip() + ': ' + str(data[MESSAGE]).strip())
            return
        if MESSAGE in data and data[TO] == ALL_USER:
            print("\nВходящее общее сообщение: " + str(data[MESSAGE]).strip())
            return

    def send(self, message):
        self.connection.send(message)
