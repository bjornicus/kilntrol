   
#!/usr/bin/python
from __future__ import print_function
import time

HEATERSTATEFILE = 'heater_state.sim'
TEMPERATUREFILE = 'temperature.sim'

class HeaterRelay(object):
    def __init__(self):
        pass
    def on(self):
        with open(HEATERSTATEFILE, "w") as heaterStateFile:
            heaterStateFile.write("on")
    def off(self):        
        with open(HEATERSTATEFILE, "w") as heaterStateFile:
            heaterStateFile.write("off")


def main():
    """ Run the simulated heater """
    running = True
    temperature = 70
    with open(TEMPERATUREFILE, "r") as temperatureFile:
        startTemp = temperatureFile.read()
        print('starting at '+ startTemp)
        temperature = float(startTemp)
    while running:
        try:
            with open(HEATERSTATEFILE, "r") as heaterStateFile:
                if heaterStateFile.read() == "on":
                    temperature = temperature + 0.75
                else:
                    temperature = temperature - 1
            with open(TEMPERATUREFILE, "w") as temperatureFile:
                temperatureFile.write(str(temperature))
            print(temperature)
            time.sleep(1)
        except KeyboardInterrupt:
            running = False

if __name__  == '__main__':
    main()