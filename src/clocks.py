import time
from heater_sim import TICKS_PER_SECOND


class BasicClock(object):
    def __init__(self, start_time=time.time()):
        self.start = start_time

    def now(self):
        return time.time() - self.start


class SpeedySimClock(object):
    def __init__(self, start_time=time.time()):
        self.start = start_time

    def now(self):
        return (time.time() - self.start) * TICKS_PER_SECOND
