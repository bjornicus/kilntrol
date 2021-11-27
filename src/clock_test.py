import time
from clock import Clock
import unittest

class ClockTest(unittest.TestCase):
    def test_normal_speed_clock(self):
        clock = Clock()
        self.assertAlmostEqual(0, clock.now(), delta=0.01)
        time.sleep(0.1)
        self.assertAlmostEqual(0.1, clock.now(), delta=0.01)

    def test_normal_speed_clock_with_start_offset(self):
        clock = Clock(start_offset_seconds=10)
        self.assertAlmostEqual(10, clock.now(), delta=0.01)
        time.sleep(0.1)
        self.assertAlmostEqual(10.1, clock.now(), delta=0.01)

    def test_accelerated_clock(self):
        clock = Clock(clock_speed_factor=10)
        self.assertAlmostEqual(0, clock.now(), delta=0.01)
        time.sleep(0.1)
        self.assertAlmostEqual(1.0, clock.now(), delta=0.1)
    
    def test_accelerated_clock_with_start_offset(self):
        clock = Clock(start_offset_seconds=10,clock_speed_factor=10)
        self.assertAlmostEqual(10, clock.now(), delta=0.01)
        time.sleep(0.1)
        self.assertAlmostEqual(11.0, clock.now(), delta=0.1)

    def test_clock_seconds_to_world_seconds(self):
        normalClock = Clock()
        fastClock = Clock(clock_speed_factor=100)
        self.assertEqual(5, normalClock.world_seconds(5))
        self.assertEqual(0.05, fastClock.world_seconds(5))