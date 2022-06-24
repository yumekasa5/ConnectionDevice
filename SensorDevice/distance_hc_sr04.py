from i2c_device_base import I2CDeviceInfoBase
import time
import RPi.GPIO

#超音波センサ(HC-SR04)クラス
class HC_SR04_Ultrasound(I2CDeviceInfoBase):
    
    def __init__(self, hex_i2c_address):
        super().__init__(hex_i2c_address)
        self.trigger = 27
        self.echo = 22
        self.timer1_s = 0.3
        self.timer2_s = 0.00001
        self.convert_mm_to_cm = 1000000
        self.val = 58
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def get_distance_mm(self):
        
        distance = 0
        try:
            GPIO.setup(self.trigger, GPIO.OUT)
            GPIO.setup(self.echo, GPIO.IN)
            GPIO.output(self.trigger, GPIO.LOW)
            time.sleep(self.timer1_s)
            GPIO.output(self.trigger, GPIO.HIGH)
            time.sleep(self.timer2_s)
            GPIO.output(self.trigger, GPIO.LOW)

            while GPIO.input(self.echo) == 0:
                echo_on = time.time()
            while GPIO.input(self.echo) == 1:
                echo_off = time.time()
            echo_pulse_width = (echo_off - echo_on) * self.convert_mm_to_cm
            distance = echo_pulse_width / self.val

        except Exception as e:
               distance = 100.0
        return distance
