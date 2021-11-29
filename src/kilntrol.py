#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Kilt Troll """
import time
import asyncio

from options import create_arg_parser
from target_profile import TargetProfile, hhmmss_to_sec, loadProfile, sec_to_hhmmss

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

    async def run(self):
        """ Start the run loop """
        self.running = True
        while self.running:
            try:
                self.tick()
                await self.wait(self.tick_interval)
                if self.target_profile.is_finished(self.clock.now()):
                    self.heater.off()
                    self.running = False
                    log_stop_time = self.clock.now() * 1.5
                    print(f'profile complete after {sec_to_hhmmss(self.clock.now())} , logging until {sec_to_hhmmss(log_stop_time)} ')
                    await self.log_until(log_stop_time)
            except KeyboardInterrupt:
                self.running = False

    def stop(self):
        """ Stop the run loop """
        self.running = False

    async def wait(self, seconds):
        await asyncio.sleep(self.clock.world_seconds(seconds))

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

    async def log_until(self, t_stop):
        while self.clock.now() < t_stop:
            self.logger.log(self.clock.now(), self.temperature.get(), 0)
            await self.wait(self.tick_interval)

def create_clock(options):
    from clock import Clock
    startTime = hhmmss_to_sec(options.time)
    if options.simulate: 
        clock_speed = 100
    else:
        clock_speed = 1
    return Clock(startTime, clock_speed)

def create_temperature_reader(options):
    if options.simulate:
        from simulator import SimulatedThermocoupleReader
        return SimulatedThermocoupleReader(options.kiln)
    else:
        from max31855 import MAX31855
        return MAX31855(cs_pin=27, clock_pin=22,
                           data_pin=17, units="f")

def create_heater(options):
    if options.simulate:
        from simulator import SimulatedHeaterRelay
        return SimulatedHeaterRelay(options.kiln)
    else:
        from heater import HeaterRelay
        return HeaterRelay(relay_pin=26)

def create_logger(options):
    from loggers import FileLogger as Logger
    return Logger('logs/temperature')

def create_kiln_simulator(options):
    from simulator import KilnSimulator
    options.kiln = KilnSimulator()

async def run_kiln_simulator(clock, kiln):
    while True:
        await asyncio.sleep(clock.world_seconds(1))
        kiln.run(1)

async def main():
    """ Run KilnTrol """
    options = create_arg_parser().parse_args()
    print(options)


    target_profile = loadProfile(options.profile)
    target_profile.dump_csv('logs/target_profile.csv')

    clock = create_clock(options)

    if options.simulate:
        create_kiln_simulator(options)
        asyncio.create_task(run_kiln_simulator(clock, options.kiln))
    temperature = create_temperature_reader(options)
    heater = create_heater(options)
    logger = create_logger(options)

    kilntrol = KilnTrol(temperature, heater, clock, target_profile, logger)

    await kilntrol.run()

if __name__ == '__main__':
    asyncio.run(main())
