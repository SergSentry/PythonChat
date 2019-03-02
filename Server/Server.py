import logging
from socket import *

from Protocol.Fields import *
from Protocol.Response import good_response
from Tools.Connection import Connection
from Config.Constants import MAX_CLIENTS
from Server.Listener import Listener
from Server.ServerHandle import server_handshake


class Server:
    __slots__ = ['address', 'socket', 'clients', 'listener', 'connection', 'logger']

    def __init__(self, address):
        self.logger = logging.getLogger('server')
        self.address = address
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.bind(address)
            self.socket.listen(MAX_CLIENTS)
            self.clients = {}
            self.listener = Listener(self.socket, self.new_connect)
            self.listener.start()
        except error:
            self.logger.error("Ошибка инициализации сервера: %s", error)

    def __del__(self):
        self.listener.join(1000)
        self.clients.clear()
        self.socket.close()

    def received_data_handler(self, connection, message):
        if ACTION in message and message[ACTION] == PRESENCE:
            self.clients[connection] = message[USER][ACCOUNT_NAME]
            connection.send(good_response())
            return
        if ACTION in message and message[ACTION] == QUIT:
            self.clients.pop(connection)
            return
        if ACTION in message and message[ACTION] == MESSAGE:
            if message[TO] == ALL_USER:
                for client in self.clients.keys():
                    if client != connection:
                        client.send(message)
            else:
                for client in self.clients.keys():
                    if client != connection and self.clients[client] == message[TO]:
                        client.send(message)
            return

    def new_connect(self, address, socket):
        connection = Connection(address, socket, self.received_data_handler)
        self.clients.setdefault(connection, '')
        connection.start()
        self.logger.info("Подключен клиент: %s ", address)
        server_handshake(connection)

    def get_clients(self):
        return self.clients
