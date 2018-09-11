from heater import HeaterRelay
import time

heater = HeaterRelay(relay_pin=26)

while True:
    print('on')
    heater.on()
    time.sleep(1)
    print('off')
    heater.off()
    time.sleep(1)
