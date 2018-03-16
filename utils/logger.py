# -*- coding: utf-8 -*-
from time import localtime, strftime
from logging import FileHandler
import os
import logging

ROOT = ''  # ${ROOT_PATH} for production mode

LOG_PATH = ''


def get_handler():
    handler = FileHandler(filename=LOG_PATH,
                          encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s]: %(levelname)s - ' +
                                  '%(module)s - ' +
                                  '%(funcName)s - %(message)s')
    handler.setFormatter(formatter)
    return handler


def setup(r):
    global ROOT, LOG_PATH
    ROOT = r
    LOG_PATH = ROOT + 'log/mainu.log'
    try:
        log = open(LOG_PATH, 'a')
    except FileNotFoundError:
        if not os.path.exists(os.path.dirname(LOG_PATH)):
            os.makedirs(os.path.dirname(LOG_PATH))
        log = open(LOG_PATH, 'w')

    log.write("##############################################\n")
    log.write("MainU -- mainu.eus -- %s\n"
              % strftime("%Y-%m-%d %H:%M:%S", localtime()))
    log.write("Telegram Bot\n")
    log.write("##############################################\n")
    log.close()

    logging.basicConfig(level=logging.DEBUG,
                        handlers=[get_handler()])
