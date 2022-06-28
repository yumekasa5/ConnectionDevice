from asyncio.log import logger
from ensurepip import version
import os
import sys
import socket
import logging
import libs
import RPi.GPIO as GPIO
from concurrent.futures import ThreadPoolExecutor
from .libs.VL53L0X import VL53L0X
from .libs.temp_amg8833 import AMG8833_8x8

IP_SERVER = '192.168.12.55'
IP_RASP = '192.168.12.52'
IP_ANDROID = '192.168.12.43'

PORT_SCREEN_CHANGE1 = 55000
PORT_SCREEN_CHANGE2 = 25000
PORT_SERVER = 40000
PORT_SENSOR = 30000
PORT_LED = 20000
PORT_TEMP = 24000

MAX_DISTANCE_CM = 60
MIN_DISTANCE_CM = 10

ALART_BODY_TEMP_DEGC = 37.5
MIN_BODY_TEMP_DEGC = 35.0

#mydeviceクラス
class MyDevice(object):
    """MyDevice"""

    version = '1.1.0'

    def __init__(self, id,
                 control_device_object, android_device_object, 
                 temp_sensor, distance_sensor, light_unit):
                 """Initialize MyDevice"""
                 logger.debug('[INITIALIZE]Create MyDevice')    
                 self.device_id = id
                 self.control_device = control_device_object
                 self.android_device = android_device_object
                 self.temp_sensor = temp_sensor
                 self.distance_sensor = distance_sensor
                 self.light = light_unit

    