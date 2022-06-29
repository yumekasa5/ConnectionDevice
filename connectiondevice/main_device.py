import logging
from .mydevice import *

#ロガーの設定
logger = logging.getLogger('mydevicelog')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./logs/logfile.log')
fmt = logging.Formatter('%(asctime)s%(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)

#executerの生成
executer = ThreadPoolExecutor(max_workers=4)
executer2 = ThreadPoolExecutor(max_workers=1)

def main():
    logger.debug('[START] MyDevice System')

    #各通信デバイスのインスタンス生成
    # rasp = ComSensorControlDevice()
    # android = ComAndroidDevice()
    # server = ComServerDevice()

    #センサ・ライトのインスタンス生成
    # gridtemp = AMG8833_8x8()
    # tof = VL53L0X()
    # light = SimpleLedLight()

    mydev = MyDevice()
    mydev.get_test_grid_data()

    logger.debug('[END] MyDevice System')

