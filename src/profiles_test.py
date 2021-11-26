import unittest
from target_profile import TargetProfile

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

class ProfilesTests(unittest.TestCase):
    def test_profile(self):
        profile = TargetProfile([
            [1, 8],
            [2, 12],
            [3, 15],
            [4, 12],
            [5, 10]
        ])
        self.assertEqual(profile.temperature_at(1), 8)
        self.assertEqual(profile.temperature_at(3), 15)
        self.assertEqual(profile.temperature_at(5), 10)

        self.assertEqual(profile.temperature_at(1.5), 10)
        self.assertEqual(profile.temperature_at(3.5), 13.5)

        self.assertEqual(profile.temperature_at(6), 0)
    
    def test_get_sec(self):
        self.assertEqual(get_sec("00:00:00"), 0)
        self.assertEqual(get_sec("00:00:01"), 1)
        self.assertEqual(get_sec("00:01:00"), 60)
        self.assertEqual(get_sec("01:00:00"), 60*60)
        self.assertEqual(get_sec("01:02:03"), 60*60 + 2*60 + 3)
    
    def test_parse_profile(self):
        # use 1 degree per second heating for eazy asserts
        data = [
            ["00:00:00", 0],
            ["00:00:01", 1],
            ["00:01:00", 60],
            ["00:02:00", 60*2],
            ["01:00:00", 60*60]
        ]
