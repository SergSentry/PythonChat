import sys
import logging

from logging.handlers import TimedRotatingFileHandler
from Server.Server import Server
from Config.Constants import *


if __name__ == '__main__':
    logger_path = 'Logs\server.log'

    logger = logging.getLogger('app')
    logging.basicConfig(filename=logger_path, filemode='w',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        format='<%(asctime)s> <%(levelname)s> <%(name)s> %(message)s',
                        level=logging.DEBUG)

    handler = TimedRotatingFileHandler(logger_path,
                                       when="D",
                                       interval=1,
                                       backupCount=5)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    try:
        address = sys.argv[1]
    except IndexError:
        address = ''

    try:
        port = int(sys.argv[2])
    except IndexError:
        port = SERVER_PORT
    except ValueError:
        logger.error("Порт должен быть целым числом")
        sys.exit(0)

    logger.info("Инициализация программы сервера: адрес '%s', порт '%s'", address, port)
    server = Server((address, port))
