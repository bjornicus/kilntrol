import time
import os.path
from heater_sim import TICKS_PER_SECOND


class BasicClock(object):
    def __init__(self, start_time=time.time()):
        self.start = start_time

    def now(self):
        return time.time() - self.start


class PersistantClock(BasicClock):
    def __init__(self, start_time_file_name='start_time.txt'):
        if os.path.isfile(start_time_file_name):
            print('loading start time from file ' + start_time_file_name)
            with open(start_time_file_name) as f:
                start_time = float(f.readline())
                super().__init__(start_time)
        else:
            print('no persisted start time found, starting from now.')
            start_time = time.time()
            with open(start_time_file_name, 'w') as f:
                f.write(str(start_time) + '\n')
            super().__init__(start_time)


class SpeedySimClock(object):
    def __init__(self, start_time=time.time()):
        self.start = start_time

    def now(self):
        return (time.time() - self.start) * TICKS_PER_SECOND
