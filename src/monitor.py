import signal
import sys
import time


def main():
    """ Run KilnTrol """
    from clocks import BasicClock as Clock
    from max31855 import MAX31855
    from target_profile import TargetProfile
    from loggers import FileLogger as Logger

    temperature = MAX31855(cs_pin=27, clock_pin=22, data_pin=17, units="f")

    def signal_handler(sig, frame):
        print('cleaning up GPIO...')
        temperature.cleanup()
        exit()
    signal.signal(signal.SIGINT, signal_handler)

    tick_interval = 5
    clock = Clock()
    logger = Logger('logs/temperature')

    while True:
        t = temperature.get()
        print('logging {0}'.format(t))
        logger.log(clock.now(), temperature.get(), 0)
        time.sleep(tick_interval)


if __name__ == '__main__':
    main()
