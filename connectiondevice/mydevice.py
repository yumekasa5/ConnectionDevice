import os
import sys
import socket
import smbus
import busio
import board
import logging
import RPi.GPIO as GPIO
import adafruit_amg88xx
# from concurrent.futures import ThreadPoolExecutor
# from .libs.VL53L0X import VL53L0X
# from .libs.temp_amg8833 import AMG8833_8x8

MYDEVICE_VERSION = '10.00'

I2C_ADDR_AMG8833 = 0x68
I2C_ADDR_VL53L0X = 0x29
I2C_ADDR_THERMISTER = 0xE

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

                 self.version = MYDEVICE_VERSION
                 self.rasp_ip = IP_RASP
                 self.android_ip = IP_ANDROID
                 self.server_ip = IP_SERVER

                 self.temp = adafruit_amg88xx.AMG88xx(i2c_bus, addr = I2C_ADDR_AMG8833)

    #8x8のグリッド温度データ取得
    def get_grid_degC(self):
        logger.debug('Get grid temperature')
        grid_8x8 = self.temp.pixels
        return grid_8x8 

    #サーミスタ温度の取得(生データx0.0625)
    def get_thermister_degC(self):
        logger.debug('Get thermister temparature')
        coificient = 0.0625
        rawtemp = i2c.read_word_data(I2C_ADDR_AMG8833, I2C_ADDR_THERMISTER)
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
      

    