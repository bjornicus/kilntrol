import time


class BasicClock(object):
    def __init__(self, start_time=time.time()):
        self.start = start_time

    def now(self):
        return time.time() - self.start
