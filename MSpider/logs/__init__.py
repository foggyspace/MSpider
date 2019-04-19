'''
from functools import wraps
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)


def print_logging(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        logging.info(f'{"execute =>", func.__name__}')
        func(*args, **kwargs)
        logging.info(f'{"execute =>", func.__name__}')
        return decorator


class Monitor(object):
    pass
'''