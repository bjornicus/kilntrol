
#!/usr/bin/python
from __future__ import print_function
import time

HEATERSTATEFILE = 'logs/_heater.sim'
TEMPERATUREFILE = 'logs/_temperature.sim'
TICKS_PER_SECOND = 100


class HeaterRelay(object):
    def __init__(self, relay_pin, board="sim"):
        pass

    def on(self):
        try:
            with open(HEATERSTATEFILE, "w") as heaterStateFile:
                heaterStateFile.write("on")
        except:
            time.sleep(0.2/TICKS_PER_SECOND)
            return self.on()

    def off(self):
        try:
            with open(HEATERSTATEFILE, "w") as heaterStateFile:
                heaterStateFile.write("off")
        except:
            time.sleep(0.2/TICKS_PER_SECOND)
            return self.on()


class MAX31855(object):
    def __init__(self, cs_pin, clock_pin, data_pin, units="c", board="sim"):
        pass

    def get(self):
        try:
            with open(TEMPERATUREFILE, "r") as temperatureFile:
                t = temperatureFile.read()
            return float(t)
        except:
            time.sleep(0.2/TICKS_PER_SECOND)
            return self.get()


def main():
    """ Run the simulated heater """
    running = True
    with open(TEMPERATUREFILE, "r") as temperatureFile:
        startTemp = temperatureFile.read()
    print('starting at ' + startTemp)
    temperature = float(startTemp)
    while running:
        try:
            with open(HEATERSTATEFILE, "r") as heaterStateFile:
                if heaterStateFile.read() == "on":
                    temperature = temperature + \
                        (1 - temperature/2500) * 0.33
                else:
                    # T(t) = Ts + (T0 - Ts ) e(-kt) but t == 1 always
                    temperature = 65 + (temperature - 65)*(0.995)
            with open(TEMPERATUREFILE, "w") as temperatureFile:
                temperatureFile.write(str(temperature))
            # print(temperature)
            time.sleep(1/TICKS_PER_SECOND)
        except KeyboardInterrupt:
            running = False


if __name__ == '__main__':
    main()
