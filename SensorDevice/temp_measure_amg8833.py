from SensorDevice.i2c_device_base import I2CDeviceInfoBase
import i2c_device_base
import smbus
import adafruit_amg88xx
import numpy as np

#AMG8833(温度センサ)
class AMG8833_8x8(I2CDeviceInfoBase):

    #コンストラクタ
    def __init__(self, hex_i2c_address = 0x68):
        super().__init__(hex_i2c_address = 0x68)
        self.i2c = smbus.SMBus(1)                                                   #ラズパイのi2cバスの番号
        self.sensor = adafruit_amg88xx.AMG88XX(self.i2c_bus, self.i2c_address)      #初期化
    
    #8x8のグリッド温度データ取得
    def get_grid_tempdata():
        grid_8x8 = self.sensor.pixels
        return grid_8x8 

    
