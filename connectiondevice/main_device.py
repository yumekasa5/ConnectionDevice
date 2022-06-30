import logging
from concurrent.futures import ThreadPoolExecutor
from .mydevice import *

#ロガーの設定
logger = logging.getLogger('mydevicelog')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('./logs/logfile.log')
fmt = logging.Formatter('%(asctime)s%(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)

#executerの生成
light_executer = ThreadPoolExecutor(max_workers=4)
screen_executer = ThreadPoolExecutor(max_workers=1)

def main():
    logger.debug('[START] MyDevice System')

    mydev = MyDevice()
    # mydev.get_test_grid_data()

    logger.debug('[END] MyDevice System')

