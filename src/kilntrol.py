#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Kilt Troll """
import time

from target_profile import TargetProfile
from clocks import BasicClock as Clock
from loggers import FileLogger as Logger
# from max31855 import MAX31855
# from heater import HeaterRelay
from heater_sim import HeaterRelay, MAX31855
from profiles import sample_profile


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

    temperature = MAX31855(cs_pin=27, clock_pin=22,
                           data_pin=17, units="f")
    heater = HeaterRelay(relay_pin=26)
    clock = Clock()
    logger = Logger('logs/temperature')
    target_profile = TargetProfile(sample_profile)

    kilntrol = KilnTrol(temperature, heater, clock, target_profile, logger)
    kilntrol.run()


if __name__ == '__main__':
    main()