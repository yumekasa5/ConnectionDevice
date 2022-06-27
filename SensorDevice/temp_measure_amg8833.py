from asyncio.log import logger
from cgitb import handler
from i2c_device_base import I2CDeviceInfoBase
import smbus
import adafruit_amg88xx
import numpy as np
import logging

#ロガーの生成
logger = logging.getLogger('amg8833_log')

#出力レベルの設定
logger.setLevel(logging.DEBUG)

#ハンドラの設定
handler = logging.FileHandler('logfile.log')

#フォーマッタの生成
fmt = logging.Formatter('%(asctime)s%(message)s')

#AMG8833(温度センサ)
class AMG8833_8x8(I2CDeviceInfoBase):

    #コンストラクタ
    def __init__(self, address = 0x68):
        super().__init__()
        logger.debug('[Initialize]AMG8833 Settings...')
        self.i2c = smbus.SMBus(1)                                                   #ラズパイのi2cバスの番号
        self.sensor = adafruit_amg88xx.AMG88XX(self.i2c_bus, self.i2c_address)      #初期化
        self.thermister_i2c_address = 0xE                                           #サーミスタのアドレス
    
    #8x8のグリッド温度データ取得
    def get_grid_temp_degC(self):
        logger.debug('Get grid temperature')
        grid_8x8 = self.sensor.pixels
        return grid_8x8 

    #サーミスタ温度の取得(生データx0.0625)
    def get_thermister_temp_degC(self):
        logger.debug('Get thermister temparature')
        coificient = 0.0625
        rawtemp = self.i2c.read_word_data(self.i2c_address, self.thermister_i2c_address)
        temp = rawtemp * coificient
        return temp
    
