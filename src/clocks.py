import time
import os.path
class BasicClock(object):
    def __init__(self, start_offset_seconds=0):
        self.start = time.time() + start_offset_seconds

    def now(self):
        return time.time() - self.start

class SimClock(object):
    def __init__(self, start_offset_seconds=0, simulation_speed=1):
        self.start = time.time() + start_offset_seconds
        self.simulation_speed = simulation_speed

    def now(self):
        return (time.time() - self.start) * self.simulation_speed
