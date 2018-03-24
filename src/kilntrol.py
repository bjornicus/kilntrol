#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Kilt Troll """
import time


class KilnTrol(object):
    """ KilnTrol Kiln Controller """

    def __init__(self, temperature, heater, clock, target_profile, logger, tick_interval=5):
        self.temperature = temperature
        self.heater = heater
        self.clock = clock
        self.target_profile = target_profile
        self.logger = logger
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
                    self.log_until(self.clock.now() * 1.5)
            except KeyboardInterrupt:
                self.running = False

    def stop(self):
        """ Stop the run loop """
        self.running = False

    def tick(self):
        """ Check the current and desired temperature and turn the heater on or off as needed """
        now = self.clock.now()
        target_temperature = self.target_profile.temperature_at(now)
        t = self.temperature.get()
        if target_temperature > t:
            self.heater.on()
        else:
            self.heater.off()
        self.logger.log(now, t, target_temperature)

    def log_until(self, t_stop):
        while self.clock.now() < t_stop:
            self.logger.log(self.clock.now(), self.temperature.get(), 0)
            time.sleep(self.tick_interval)


def main():
    """ Run KilnTrol """
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "sim":
        from clocks import SpeedySimClock as Clock
        from heater_sim import HeaterRelay, MAX31855, TICKS_PER_SECOND
        tick_interval = 5/TICKS_PER_SECOND
    else:
        from clocks import BasicClock as Clock
        from max31855 import MAX31855
        from heater import HeaterRelay
        tick_interval - 5
    from target_profile import TargetProfile
    from loggers import FileLogger as Logger

    from profiles import glaze_profile as target_profile
    # from profiles import test_profile as target_profile
    # from profiles import sample_profile as target_profile

    temperature = MAX31855(cs_pin=27, clock_pin=22,
                           data_pin=17, units="f")
    heater = HeaterRelay(relay_pin=26)
    clock = Clock()
    logger = Logger('logs/temperature')
    target_profile = TargetProfile(target_profile)

    kilntrol = KilnTrol(temperature, heater, clock,
                        target_profile, logger, tick_interval)
    kilntrol.run()


if __name__ == '__main__':
    main()
