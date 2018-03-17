#!/usr/bin/python
from __future__ import print_function
import RPi.GPIO as GPIO

class HeaterRelay(object):
    def __init__(self, relay_pin, board = GPIO.BCM):
        self.relay_pin = relay_pin
        GPIO.setmode(board)
        GPIO.setup(self.relay_pin, GPIO.OUT)
    def on(self):
        GPIO.output(self.relay_pin, GPIO.HIGH)
    def off(self):
        GPIO.output(self.relay_pin, GPIO.LOW)