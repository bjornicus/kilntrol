import time

class Clock(object):
    def __init__(self, start_offset_seconds=0, clock_speed_factor=1):
        self.start = time.time() - start_offset_seconds/clock_speed_factor
        self.clock_speed_factor = clock_speed_factor

    def now(self):
        return (time.time() - self.start) * self.clock_speed_factor
    
    def world_seconds(self, clock_seconds):
        return clock_seconds / self.clock_speed_factor
