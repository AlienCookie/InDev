import os
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.WARNING
)

def get_log_level():
    l = os.environ.get('GP_LOG_LEVEL', 'info')

    if l == 'debug':
        return logging.DEBUG
    elif l == 'info':
        return logging.INFO
    elif l == 'warning':
        return logging.WARNING

    return logging.WARNING


def get_env(name):
    if name not in os.environ:
        raise Exception("%s not set" % name)
    return os.environ[name]


def get_logger(name):
    l = logging.getLogger(name)
    l.setLevel(get_log_level())
    return l
