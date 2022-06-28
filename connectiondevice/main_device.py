import logging
from connectiondevice.libs.VL53L0X import VL53L0X
import mydevice
from .libs.com_device import *
from .libs.temp_amg8833 import *
from .libs.led_light import *

#ロガーの生成
logger = logging.getLogger('amg8833_log')

#出力レベルの設定
logger.setLevel(logging.DEBUG)

#ハンドラの設定
handler = logging.FileHandler('./logs/logfile.log')

#フォーマッタの生成
fmt = logging.Formatter('%(asctime)s%(message)s')
handler.setFormatter(fmt)

#ハンドラをloggerに追加
logger.addHandler(handler)

debug_msg = 'debug message'
error_msg = 'error_message'

executer = ThreadPoolExecutor(max_workers=4)
executer2 = ThreadPoolExecutor(max_workers=1)

def main():
    logger.debug(debug_msg)
    logger.debug('[START] MyDevice System Start')

    #各通信デバイスのインスタンス生成
    rasp = ComSensorControlDevice()
    android = ComAndroidDevice()
    server = ComServerDevice()

    #センサ・ライトのインスタンス生成
    gridtemp = AMG8833_8x8()
    tof = VL53L0X()
