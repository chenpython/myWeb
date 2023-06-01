# -*- coding: utf-8
# time: 2022/10/17 15:51
# file: logger.py
# author: kevin_wang

import datetime
import logging
import os

from . import scrapy_settings

file_log = scrapy_settings.FILE_LOG
log_path = scrapy_settings.LOG_PATH

DEFAULT_FMT = '%(asctime)s [%(name)s %(levelname)s]: %(message)s'
DEFAULT_DATEFMT = '%Y-%m-%d %H:%M:%S'
DEFAULT_LOGLEVEL = 'INFO'


class Logger:

    def __init__(self, name='logger'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(DEFAULT_LOGLEVEL)
        if file_log:
            file_handler = self.get_handler(file_log)
            self.logger.addHandler(file_handler)
        stream_handler = self.get_handler()
        self.logger.addHandler(stream_handler)

    @staticmethod
    def get_handler(file=None):

        if file:
            if not os.path.exists(log_path):
                os.mkdir(log_path)
            log_file = f'{log_path}/log_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")}.log'
            handler = logging.FileHandler(log_file, mode='a', encoding='utf8')
        else:
            handler = logging.StreamHandler()

        formatter = logging.Formatter(fmt=DEFAULT_FMT, datefmt=DEFAULT_DATEFMT)
        handler.setFormatter(formatter)
        handler.setLevel(DEFAULT_LOGLEVEL)

        return handler

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)
