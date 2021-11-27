import unittest
from target_profile import TargetProfile, createProfile, loadProfile, hhmmss_to_sec

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
    
    def test_hhmmss_to_sec(self):
        self.assertEqual(hhmmss_to_sec("00:00:00"), 0)
        self.assertEqual(hhmmss_to_sec("00:00:01"), 1)
        self.assertEqual(hhmmss_to_sec("00:01:00"), 60)
        self.assertEqual(hhmmss_to_sec("01:00:00"), 60*60)
        self.assertEqual(hhmmss_to_sec("01:02:03"), 60*60 + 2*60 + 3)
    
    def test_parse_profile(self):
        # use 1 degree per second heating for eazy asserts
        profileData = [
            ["00:00:00", 0],
            ["00:00:01", 1],
            ["00:01:00", 60],
            ["00:02:00", 60*2],
            ["01:00:00", 60*60]
        ]
        profile = createProfile(profileData)

        self.assertEqual(profile.temperature_at(1), 1)
        self.assertEqual(profile.temperature_at(30), 30)
        self.assertEqual(profile.temperature_at(90), 90)

    def test_load_profile_from_file(self):
        f = open('test-profile.json')
        profile = loadProfile(f)
        f.close()

        self.assertEqual(profile.temperature_at(0), 60)
        self.assertEqual(profile.temperature_at(30*60), 90) # 00:00:30
        self.assertEqual(profile.temperature_at(1*60*60), 120) # 01:00:00
        self.assertEqual(profile.temperature_at(1*60*60 + 30*60), 120 + 50 ) # 01:30:00
        self.assertEqual(profile.temperature_at(2*60*60), 220) # 02:00:00
        self.assertEqual(profile.temperature_at(3*60*60), 220) # 03:00:00
        self.assertEqual(profile.temperature_at(4*60*60), 100) # 04:00:00
