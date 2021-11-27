import unittest
from simulator import SimulatedHeaterRelay, SimulatedThermocoupleReader
from clock import Clock

class SimulatorTest(unittest.TestCase):
    def test_heat_up(self):
        clock = Clock()
        heater = SimulatedHeaterRelay(clock)
        thermocouple = SimulatedThermocoupleReader(clock)
