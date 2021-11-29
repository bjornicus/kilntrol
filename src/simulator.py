
#!/usr/bin/python
import datetime
from time import sleep
from clock import Clock


class KilnSimulator(object):
    def __init__(self, start_temperature=60, room_temperature=60) -> None:
        super().__init__()
        self.temperature = start_temperature
        self.room_temperature = room_temperature
        self.heat_input_rate = 0
        self.heat_loss_rate = -0.000071
    def heat_on(self):
        self.heat_input_rate = 0.18
    def heat_off(self):
        self.heat_input_rate = 0
    def run(self, duration_seconds):
        for t in range(0, duration_seconds):
            # there's always cooling
            delta_t_cooling = self.heat_loss_rate * (self.temperature - self.room_temperature)
            # but sometimes heating as well
            delta_t_heating = self.heat_input_rate
            self.temperature += delta_t_heating + delta_t_cooling 

defaultKiln = KilnSimulator()
class SimulatedHeaterRelay(object):
    def __init__(self, kiln=defaultKiln):
        self.kiln = kiln

    def on(self):
        self.kiln.heat_on()

    def off(self):
        self.kiln.heat_off()


class SimulatedThermocoupleReader(object):
    def __init__(self, kiln=defaultKiln):
        self.kiln = kiln

    def get(self):
        return self.kiln.temperature


def main():
    """ Run the simulated heater """
    running = True
    clock = Clock()
    kiln = KilnSimulator(start_temperature=1713.2)
    heater = SimulatedHeaterRelay(kiln)
    temperarature = SimulatedThermocoupleReader(kiln)
    runtime_seconds = 0
    heater.on()
    while running and runtime_seconds < 60*5*26:
        try:
            if runtime_seconds % (60*5) == 0:
                # heater.on()
                print(f'{str(datetime.timedelta(seconds=runtime_seconds))}, {temperarature.get()}')
            # if step % 120 == 0:
            #     heater.off()

            # sleep(0.01)
            runtime_seconds +=5
            kiln.run(5)
        except KeyboardInterrupt:
            running = False


if __name__ == '__main__':
    main()
