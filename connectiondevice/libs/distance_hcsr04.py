import time
import RPi.GPIO as GPIO

#超音波センサ(HC-SR04)クラス
class HCSR04_Ultrasound(object):
    """HC-SR04 Ultrasound"""

    object_number = 0

    def __init__(self, trriger = 27, echo = 22, timer1 = 0.3, timer2 = 0.00001):
        self.trigger_pin = trriger
        self.echo_pin = echo
        self.timer1_s = timer1
        self.timer2_s = timer2
        self.convert_mm_to_cm = 1000000
        self.val = 58
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def get_distance_cm(self):
        """Get distance from HC-SR04 Ultrasound Sensor"""

        logger.debug('Get distance from hc-sr04')
        distance = 0
        try:
            GPIO.setup(self.trigger_pin, GPIO.OUT)
            GPIO.setup(self.echo_pin, GPIO.IN)
            GPIO.output(self.trigger_pin, GPIO.LOW)
            time.sleep(self.timer1_s)
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(self.timer2_s)
            GPIO.output(self.trigger_pin, GPIO.LOW)

            while GPIO.input(self.echo_pin) == 0:
                echo_on = time.time()
            while GPIO.input(self.echo_pin) == 1:
                echo_off = time.time()
            echo_pulse_width = (echo_off - echo_on) * self.convert_mm_to_cm
            distance = echo_pulse_width / self.val

        except Exception as e:
               logger.debug('[DEBUG]Out of Sensing Range')
               distance = 100.0
        
        return distance
