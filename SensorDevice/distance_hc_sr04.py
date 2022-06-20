import RPi.GPIO

class HC_SR04_Ultrasound:
    
    def __init__(self):
        self.trigger = 27
        self.echo = 22
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def get_distance_mm(self):
        pass
