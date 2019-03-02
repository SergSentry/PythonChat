import time
from Protocol.Fields import *


def presence_message(account_name):
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return message


def quit_message():
    message = {
        ACTION: QUIT,
    }
    return message


def user_message(from_user, to_user, message):
    message = {
        ACTION: MESSAGE,
        TIME: time.time(),
        FROM: from_user,
        TO: to_user,
        ENCODING: UTF8,
        MESSAGE: message
    }
    return message
