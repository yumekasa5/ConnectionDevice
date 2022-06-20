import busio
import board

#i2cデバイス基底クラス
class I2CDeviceInfoBase:
    def __init__(self, hex_i2c_address):
        self.i2c_address = hex_i2c_address
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)