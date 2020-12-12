
def main():
    """ Run KilnTrol """
    import sys
    from clocks import BasicClock as Clock
    from max31855 import MAX31855
    from target_profile import TargetProfile
    from loggers import FileLogger as Logger
    tick_interval = 5
    clock = Clock()
    temperature = MAX31855(cs_pin=27, clock_pin=22, data_pin=17, units="f")
    while clock.now() < t_stop:
        logger.log(clock.now(), temperature.get(), 0)
        time.sleep(tick_interval)


if __name__ == '__main__':
    main()
