""" Kilt Troll """
import time

class KilnTrol(object):
    """ KilnTrol Kiln Controller """
    def __init__(self, temperature, heater, clock, target_profile, tick_interval=5):
        self.temperature = temperature
        self.heater = heater
        self.clock = clock
        self.target_profile = target_profile
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
            except KeyboardInterrupt:
                self.running = False

    def stop(self):
        """ Stop the run loop """
        self.running = False

    def tick(self):
        """ Check the current and desired temperature and turn the heater on or off as needed """
        target_temperature = self.target_profile.temperature_at(self.clock.now())
        if target_temperature > self.temperature.get():
            self.heater.on()
        else:
            self.heater.off()

def main():
    """ Run KilnTrol """
    import max31855
    # import heater

if __name__  == '__main__':
    main()