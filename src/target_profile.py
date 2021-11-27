import json

def hhmmss_to_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def createProfile(profileData):
    def toPoint(e):
        return [hhmmss_to_sec(e[0]), e[1]]

    points = list(map(toPoint, profileData))
    return TargetProfile(points)

def loadProfile(file):
    profileData = json.load(file)
    return createProfile(profileData)

class TargetProfile(object):
    def __init__(self, points):
        self.points = points
        self.last_time = points[-1][0]

    def temperature_at(self, time):
        if self.is_finished(time):
            return 0

        next_point_index = 0
        while self.points[next_point_index][0] < time:
            next_point_index += 1
        if next_point_index == 0:
            return self.points[0][1]
        last_point = self.points[next_point_index - 1]
        next_point = self.points[next_point_index]
        duration = next_point[0] - last_point[0]
        temperature_delta = next_point[1] - last_point[1]
        slope = temperature_delta/duration
        time_since_last_point = time - last_point[0]
        return last_point[1] + slope*time_since_last_point

    def is_finished(self, time):
        return self.last_time < time
