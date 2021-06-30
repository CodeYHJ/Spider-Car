import logging
import datetime
import re


class Log(object):
    @staticmethod
    def createLog(name):
        configDict = Log.createLogConfig(name)
        logging.basicConfig(filename=configDict.get('filename'), encoding=configDict.get('encoding'), level=configDict.get('level'), format=configDict.get('format'))
        return logging

    @staticmethod
    def createLogConfig(name):
        to_day = datetime.datetime.now()
        log_file_path = "{}/scrapy_{}_{}_{}.log".format(name, to_day.year, to_day.month, to_day.day)
        filename = log_file_path
        encoding = 'utf-8'
        level = "WARNING"
        log_format = "%(levelname)s %(asctime)s %(message)s %(filename)s %(funcName)s"
        return {filename: filename, encoding: encoding, level: level, format: log_format}


class ContentFilter(logging.Filter):
    def filter(self, record):
        match = re.search(r'', record.message)
        return True