import RPi.GPIO as GPIO
from time import sleep
 

class SimpleLedLight(object):
    """Simple LED Light"""

    def __init__(self, pin = 25):
        """Constructor"""
        self.gpio_pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

    def start_lit(self):
        """Start light"""
        try:
            GPIO.output(self.gpio_pin, GPIO.HIGH)
        except KeyboardInterrupt:
            pass

    def end_lit(self):
        """End light"""
        try:
            GPIO.output(self.gpio_pin, GPIO.LOW)
        except KeyboardInterrupt:
            pass


