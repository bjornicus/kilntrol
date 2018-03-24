
#!/usr/bin/python
from __future__ import print_function
import time

HEATERSTATEFILE = 'logs/_heater.sim'
TEMPERATUREFILE = 'logs/_temperature.sim'
TICKS_PER_SECOND = 500


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
    room_temperature = 65
    while running:
        try:
            with open(HEATERSTATEFILE, "r") as heaterStateFile:
                # there's always cooling
                temperature -=  0.0001 * (temperature - room_temperature) # per second
                # but sometimes heating as well
                if heaterStateFile.read() == "on":
                    temperature += 0.33

            with open(TEMPERATUREFILE, "w") as temperatureFile:
                temperatureFile.write(str(temperature))
            # print(temperature)
            time.sleep(1/TICKS_PER_SECOND)
        except KeyboardInterrupt:
            running = False


if __name__ == '__main__':
    main()
