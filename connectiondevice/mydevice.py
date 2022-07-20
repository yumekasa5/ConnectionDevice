#!/usr/bin/python

# MIT License
#
# Copyright (c) 2022 Kaito Mori
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from ast import While
from concurrent.futures import ThreadPoolExecutor
from http import client
import os
from pickle import TRUE
import sys
import socket
import smbus
import busio
import board
import logging
import RPi.GPIO as GPIO
import adafruit_amg88xx
from libs.led_light import *
from libs.distance_hcsr04 import *
# from concurrent.futures import ThreadPoolExecutor
# from .libs.VL53L0X import VL53L0X
import param
from libs.correct_temp import gaussian_filter, get_facegrids_degC, calc_offset, estimate_env_temp_degC, estimate_body_temp_degC

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

                 logger.debug('[START]Initialize MyDevice System')

                 self.version = param.MYDEVICE_VERSION
                 self.mode = param.SYSTEM_MODE
                 self.rasp_ip = param.IP_RASP
                 self.android_ip = param.IP_ANDROID
                 self.server_ip = param.IP_SERVER
                 self.port_screen_change1 = param.PORT_SCREEN_CHANGE1
                 self.port_screen_change2 = param.PORT_SCREEN_CHANGE2
                 self.port_led = param.PORT_LED
                 self.port_sensor = param.PORT_SENSOR
                 self.port_server = param.PORT_SERVER
                 self.max_dis_cm = param.MAX_DISTANCE_CM
                 self.min_dis_cm = param.MIN_DISTANCE_CM
                 self.max_temp_degC = param.ALART_BODY_TEMP_DEGC
                 self.min_temp_degC = param.MIN_BODY_TEMP_DEGC
                 self.correct_slope = param.SLOPE
                 self.correct_intercept = param.INTERCEPT
                 self.temp = adafruit_amg88xx.AMG88xx(i2c_bus, addr = param.I2C_ADDR_AMG8833)
                 self.dis = HCSR04_Ultrasound()
                 self.light = SimpleLedLight()

                 logger.debug('[END]Initialize MyDevice System')

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
        distance_cm = self.dis.get_distance_cm()
        return distance_cm

    #
    def socket_lit(self):
        pass
    
    #画面遷移(待機 <-> 認証)ループ
    def screen_change_loop(self):
        """Change Android GUI """
        try:
            is_recog = False
            logger.debug('[START]Screen change loop')
            
            while True:
                if not is_recog:
                    try:
                        distance_cm = self.get_distance_cm()
                        logger.info('[DATA]distance:', distance_cm, '[cm]')
                    except Exception as e:
                        logger.error('[999]Get distance failed')

                    #距離の評価
                    if distance_cm <= self.max_dis_cm:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            try:
                                s.connect((self.android_ip, self.port_screen_change1))
                                s.send(b'startFRR')
                                is_recog = True
                                logger.debug('[MODE]Face recognition')

                            except Exception as e:
                                if str(e) != '[Error 111] Connection refused':
                                    logger.error('[111]Connection refused')
                            finally:
                                s.close()
                else:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        try:
                            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                            s.bind((self.rasp_ip, self.port_screen_change2))
                            s.listen(2)
                            clientsock, clienct_address = s.accept()
                            is_recog = False
                            logger.debug('[MODE]Wating')

                        except Exception as e:
                            if str(e) != '[Error 111] Connection refused':
                                logger.error('[111]Connection refused')
                        finally:
                            clientsock.close()
                            s.close()
        except Exception as e:
            if str(e) != '[Error 111] Connection refused':
                logger.error('[111]Connection refused')
        
        logger.debug('[END]Screen change loop')


    #体温測定ループ(RaspberryPi -> Android)
    def sensor_socket_android_loop(self):
        """Measure body temp and send results to android."""

        logger.debug('[START]Sensor socket android loop')
        send_data_executor = ThreadPoolExecutor(max_workers=1)
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    logger.debug('[START]Connect to android')
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(self.rasp_ip, self.port_sensor)
                    s.listen(2)
                    
                    #android端末との接続
                    logger.debug('[START]Wating for connection from android')
                    clientsock, client_address = s.accept()
                    logger.debug('[END]Wating for connection from android')
                    
                    #体温測定
                    logger.debug('[START]Measure body temp')
                    raw_grid_degC = self.get_grid_degC()
                    distance_cm = self.get_distance_cm()
                    logger.info('[DATA]distance:', distance_cm, '[cm]')

                    #距離によるオフセットの算出
                    if self.min_dis_cm <= distance_cm <=  self.max_dis_cm:
                        temp_offset_degC = calc_offset(distance_cm, self.correct_slope, self.correct_intercept)
                    else:
                        temp_offset_degC = calc_offset(25, self.correct_slope, self.correct_intercept)
                    logger.info('[DATA]Offset:', temp_offset_degC, '[℃]')

                    #取得値補正
                    body_temp_degC = estimate_body_temp_degC(distance_cm, raw_grid_degC, temp_offset_degC)
                    send_data_executor.submit(self.send_data_to_server_loop, body_temp_degC)
                    logger.info('[DATA]Body temp:', body_temp_degC, '[℃]')
                    logger.debug('[END]Measure body temp')

                except Exception as e:
                    logger.error('[E112]rasp -> android:', e)
                finally:
                    clientsock.close()
                    s.close()
                    logger.debug('[END]Connect to android')
        
        logger.debug('[END]Sensor socket android loop')
    
    #体温データ送信ループ(RaspberryPi -> Server)
    def send_data_to_server_loop(self, grid_degC):
        """Send body temp data to server."""

        logger.debug('[START]Send data to server loop')
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    logger.debug('[START]Connect to server')
                    s.connect(self.server_ip, self.port_server)
                    s.send(str(grid_degC).encode())
                    logger.debug('[SUCCESS]Send body temp data')

                except Exception as e:
                    logger.error('[E112]rasp -> server:', e)

                else:
                    break
                finally:
                    s.close()
                    logger.debug('[END]Connect to server')
        logger.debug('[END]Send data to server loop')

      

    