import sys
import logging

from Client.Client import Client
from Config.Constants import SERVER_PORT, ENCODING
from Protocol.Messages import *
from Protocol.Response import *

if __name__ == '__main__':
    logger_path = 'Logs\client.log'

    logging.basicConfig(filename=logger_path, filemode='w',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        format='<%(asctime)s> <%(levelname)s> <%(name)s> %(message)s',
                        level=logging.DEBUG)

    logger = logging.getLogger('app')

    try:
        address = sys.argv[1]
    except IndexError:
        address = 'localhost'

    try:
        port = int(sys.argv[2])
    except IndexError:
        port = SERVER_PORT
    except ValueError:
        logger.error("Порт должен быть целым числом")
        sys.exit(0)

    logger.info("Инициализация программы клиента: адрес '%s', порт '%s'", address, port)
    own_user_name = str(input("Введите имя: "))

    client = Client((address, port), own_user_name)
    client.send(presence_message(own_user_name))

    while True:
        input_msg = str(input("\n\nВведите сообщение в формате: \n"
                              "\tник сообщение  - для отправки собщения для указанного ника\n" 
                              "\t# сообщение    - для отправки собщения всем\n" 
                              "\tq              - для выхода\n"
                              ">"))
        if input_msg == 'q':
            client.send(quit_message())
            print("\nПока")
            break
        else:
            user_name_index = input_msg.index(' ', 0)
            other_user_name = input_msg[0:user_name_index].strip()
            message = input_msg[user_name_index:].strip()

            if other_user_name == ALL_USER:
                client.send(user_message(own_user_name, ALL_USER, message))
            else:
                client.send(user_message(own_user_name, other_user_name, message))

    del client
