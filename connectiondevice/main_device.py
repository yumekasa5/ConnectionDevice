import logging
from concurrent.futures import ThreadPoolExecutor
from .mydevice import *

#executerの生成
light_executer = ThreadPoolExecutor(max_workers=4)
screen_executer = ThreadPoolExecutor(max_workers=1)

def main():
    logger.debug('[START] MyDevice System')

    mydev = MyDevice()
    # mydev.get_test_grid_data()
    screen_executer.submit(mydev.screen_change_loop)
    light_executer.submit(mydev.socket_lit)

    logger.debug('[END] MyDevice System')

