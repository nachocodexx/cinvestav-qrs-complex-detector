from calendar import timegm
import time


class TimerUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def currentTime():
        return timegm(time.gmtime())
