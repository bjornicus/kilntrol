import unittest
from target_profile import TargetProfile

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