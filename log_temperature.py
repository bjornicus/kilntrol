""" logs the current temperature of the thermocouple to a file """
from __future__ import print_function
import time
from datetime import datetime
from max31855 import MAX31855, MAX31855Error

CS_PIN = 27
CLOCK_PIN = 22
DATA_PIN = 17
UNITS = "f"

LOG_INTERVAL = 12


def log_readings(thermocouple, logfile):
    """
    Reads the thermocouple and reference junction temperatures and writes them to the console.
    Every LOG_INTERVAL readings it also logs the readings to the logfile.
    """
    rj = thermocouple.get_rj()
    try:
        thermocouple.reading_count += 1
        tc = thermocouple.get()
    except MAX31855Error as e:
        tc = "Error: " + e.value
        thermocouple.error_count += 1
    print("tc: {} and rj: {} error ratio: {}/{}"
          .format(tc, rj, thermocouple.error_count, thermocouple.reading_count))
    if thermocouple.reading_count % LOG_INTERVAL == 0:
        print("logging...")
        logfile.write(datetime.now().strftime(
            "%I:%M %p, " + str(tc) + ", " + str(rj) + "\n"))
        logfile.flush()


def main():
    thermocouple = MAX31855(CS_PIN, CLOCK_PIN, DATA_PIN, UNITS)
    thermocouple.error_count = 0
    thermocouple.reading_count = 0

    logfile = open("temperature_log.csv", "a")

    running = True
    while running:
        try:
            log_readings(thermocouple, logfile)
            time.sleep(5)
        except KeyboardInterrupt:
            running = False

    thermocouple.cleanup()
    logfile.close()


if __name__ == '__main__':
    main()
