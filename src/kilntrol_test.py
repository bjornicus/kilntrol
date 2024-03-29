"""kilntrol unit tests"""
import unittest
from kilntrol import KilnTrol
from target_profile import TargetProfile

import time


class TestClock(object):
    def __init__(self):
        self.start = time.time()

    def now(self):
        return time.time() - self.start


class TestLogger(object):
    def __init__(self):
        pass

    def log(self, t_sec, temp, target):
        pass


class TestKiln(object):
    def __init__(self, startingTemperature, clock, heating_rate=50, cooling_rate=40):
        self.temperature = startingTemperature
        self.clock = clock
        self.is_on = False
        self.last_update = clock.now()
        self.heating_rate = heating_rate
        self.cooling_rate = cooling_rate

    def get(self):
        self.update()
        nowish = round(self.clock.now(), 2)
        temp = round(self.temperature, 1)
        state = "on" if self.is_on else "off"
        return self.temperature

    def on(self):
        self.update()
        self.is_on = True

    def off(self):
        self.update()
        self.is_on = False

    def update(self):
        now = self.clock.now()
        time_delta = now - self.last_update
        self.last_update = now
        if self.is_on:
            self.temperature += self.heating_rate * time_delta
        else:
            self.temperature -= self.cooling_rate * time_delta


class KilnTrolTests(unittest.TestCase):
    # def setUp(self):
    #     self.subject = kilntrol()

    # def tearDown(self):
    #     self.widget.dispose()
    # @unittest.skip("reason for skipping")



    # @unittest.skip("reason for skipping")a
    def test_run_to_completion(self):
        """
            create a kilntrol and run to completion
            kilntrol takes (temperature, heater, clock, target_profile, tick_interval=5):
        """
        clock = TestClock()
        kiln = TestKiln(8, clock)
        profile = TargetProfile([
            [0.1, 8],
            [0.2, 12],
            [0.3, 15],
            [0.4, 12],
            [0.5, 10]
        ])
        subject = KilnTrol(kiln, kiln, clock, profile,
                           TestLogger(), tick_interval=0.005)
        subject.run()

        self.assertTrue(profile.is_finished(clock.now()))

        # self.maxDiff = None
        # self.assertEqual(kiln.log, [])
