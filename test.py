"""kilntrol unit tests"""
import unittest
from kilntrol import KilnTrol

import time

class TestClock(object):
    def __init__(self):
        self.start = time.time()
    def now(self):
        return time.time() - self.start

class TestKiln(object):
    def __init__(self, startingTemperature):
        self.temperature = startingTemperature
    def get(self):
        return self.temperature
    def on(self):
        self.temperature += 3
    def off(self):
        self.temperature -= 2

class TestProfile(object):
    def __init__(self, profile):
        self.profile = profile
        self.last_time = profile[-1][0]

    def temperature_at(self, time):
        if self.is_finished(time):
            return 0

        next_point_index = 0
        while self.profile[next_point_index][0] < time:
            next_point_index +=1
        if next_point_index == 0:
            return self.profile[0][1]
        last_point = self.profile[next_point_index -1]
        next_point = self.profile[next_point_index]
        duration = next_point[0] - last_point[0]
        temperature_delta = next_point[1] - last_point[1]
        slope = temperature_delta/duration
        time_since_last_point = time - last_point[0]
        return last_point[1] + slope*time_since_last_point

    def is_finished(self, time):
        return self.last_time < time

class KilnTrolTests(unittest.TestCase):
    # def setUp(self):
    #     self.subject = kilntrol()

    # def tearDown(self):
    #     self.widget.dispose()
    def test_profile(self):
        profile = TestProfile([
            [1, 8],
            [2,12],
            [3,15],
            [4,12],
            [5,10]
        ])
        self.assertEqual(profile.temperature_at(1), 8)
        self.assertEqual(profile.temperature_at(3), 15)
        self.assertEqual(profile.temperature_at(5), 10)

        self.assertEqual(profile.temperature_at(1.5), 10)
        self.assertEqual(profile.temperature_at(3.5), 13.5)

        self.assertEqual(profile.temperature_at(6), 0)        

    def test_run_to_completion(self):
        """
            create a kilntrol and run to completion
            kilntrol takes (temperature, heater, clock, target_profile, tick_interval=5):
        """
        kiln = TestKiln(10)
        clock = TestClock()
        profile = TestProfile([
            [0.1, 8],
            [0.2,12],
            [0.3,15],
            [0.4,12],
            [0.5,10]
        ])
        subject = KilnTrol(kiln, kiln, clock, profile, tick_interval=0.05 )
        subject.run()

        self.assertTrue(profile.is_finished(clock.now()))

