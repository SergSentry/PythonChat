import logging
import traceback
from functools import wraps


class Log:
    def __init__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            func(*args, **kwargs)
            logger = logging.getLogger('FUNC')
            logger.info('Метод/функция "' + str(func.__name__) + '" вызван/а из ' + traceback.format_stack()[0].strip())
            return

        return decorated
