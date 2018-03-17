""" Kilt Troll """
import time

class KilnTrol(object):
    """ KilnTrol Kiln Controller """
    def __init__(self, temperature, heater, clock, target_profile, tick_interval=5):
        self.temperature = temperature
        self.heater = heater
        self.clock = clock
        self.target_profile = target_profile
        self.tick_interval = tick_interval
        self.running = False

    def run(self):
        """ Start the run loop """
        self.running = True
        while self.running:
            try:
                self.tick()
                time.sleep(self.tick_interval)
                if self.target_profile.is_finished(self.clock.now()):
                    self.heater.off()
                    self.running = False
            except KeyboardInterrupt:
                self.running = False

    def stop(self):
        """ Stop the run loop """
        self.running = False

    def tick(self):
        """ Check the current and desired temperature and turn the heater on or off as needed """
        target_temperature = self.target_profile.temperature_at(self.clock.now())
        if target_temperature > self.temperature.get():
            self.heater.on()
        else:
            self.heater.off()
        print('current: '+ str(self.temperature.get()) + ' target: ' + str(target_temperature))

class TargetProfile(object):
    def __init__(self, points):
        self.points = points
        self.last_time = points[-1][0]

    def temperature_at(self, time):
        if self.is_finished(time):
            return 0

        next_point_index = 0
        while self.points[next_point_index][0] < time:
            next_point_index +=1
        if next_point_index == 0:
            return self.points[0][1]
        last_point = self.points[next_point_index -1]
        next_point = self.points[next_point_index]
        duration = next_point[0] - last_point[0]
        temperature_delta = next_point[1] - last_point[1]
        slope = temperature_delta/duration
        time_since_last_point = time - last_point[0]
        return last_point[1] + slope*time_since_last_point

    def is_finished(self, time):
        return self.last_time < time

class BasicClock(object):
    def __init__(self, start_time = time.time()):
        self.start = start_time
    def now(self):
        return time.time() - self.start

def main():
    """ Run KilnTrol """
    # from max31855 import MAX31855
    # from heater import HeaterRelay
    from heater_sim import HeaterRelay, MAX31855
    from profiles import sample_profile

    temperature = MAX31855(cs_pin = 27, clock_pin = 22, data_pin = 17, units = "f")
    heater = HeaterRelay(relay_pin = 26)
    clock = BasicClock()
    target_profile = TargetProfile(sample_profile)

    kilntrol = KilnTrol(temperature, heater, clock, target_profile )
    kilntrol.run()

if __name__  == '__main__':
    main()