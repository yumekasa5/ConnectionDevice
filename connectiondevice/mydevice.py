import os
import sys
import socket
import smbus
import busio
import board
import logging
import RPi.GPIO as GPIO
import adafruit_amg88xx
from .libs.led_light import *
from .libs.distance_hc_sr04 import *
# from concurrent.futures import ThreadPoolExecutor
# from .libs.VL53L0X import VL53L0X
# from .libs.temp_amg8833 import AMG8833_8x8
import param

#i2cの設定
i2c_bus = busio.I2C(board.SCL, board.SDA)
i2c = smbus.SMBus(1)

#ロガーの設定
logger = logging.getLogger('mydevicelog')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./logs/logfile.log')
fmt = logging.Formatter('%(asctime)s%(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)


#MyDeviceクラス
class MyDevice(object):
    """MyDevice"""

    def __init__(self):
                 """Initialize MyDevice"""
                 logger.debug('[INIT]MyDevice System')

                 self.version = param.MYDEVICE_VERSION
                 self.rasp_ip = param.IP_RASP
                 self.android_ip = param.IP_ANDROID
                 self.server_ip = param.IP_SERVER

                 self.temp = adafruit_amg88xx.AMG88xx(i2c_bus, addr = param.I2C_ADDR_AMG8833)
                 self.dis = HC_SR04_Ultrasound()
                 self.light = SimpleLedLight()

    #8x8のグリッド温度データ取得
    def get_grid_degC(self):
        logger.debug('Get grid temperature')
        grid_8x8 = self.temp.pixels
        return grid_8x8 

    #サーミスタ温度の取得(生データx0.0625)
    def get_thermister_degC(self):
        logger.debug('Get thermister temparature')
        coificient = 0.0625
        rawtemp = i2c.read_word_data(param.I2C_ADDR_AMG8833, param.I2C_ADDR_THERMISTER)
        temp = rawtemp * coificient
        return temp

    #テスト用温度データ取得
    def get_test_grid_data(self):
        try:
            logger.debug('[START]temp data')
            while True:
                    for row in self.temp.pixels:
                        print(['{0:.1f}'.format(temp) for temp in row])
                        print('')
                        print('\n')
        except KeyboardInterrupt:
            logger.debug('[STOP]temp data')

    #照明をつける
    def light_on(self):
        logger.debug('[ON]Light')
        self.light.start_lit()

    #照明を消す
    def light_off(self):
        logger.debug('[OFF]Light')
        self.light.end_lit()

    #距離を取得
    def get_distance_cm(self):
        pass
      

    