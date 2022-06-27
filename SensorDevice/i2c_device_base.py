import busio
import board

#i2cデバイス基底クラス
class I2CDeviceInfoBase:
    def __init__(self, address):
        self.device_address = address
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)