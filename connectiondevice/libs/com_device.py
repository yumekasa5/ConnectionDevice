import ipaddress
import socket
from time import sleep
from unicodedata import name
import numpy as np
from concurrent.futures import ThreadPoolExecutor

#通信機器情報クラス
class ComDeviceInfoBase:
    
    #コンストラクタ
    def __init__(self, devname, ipaddress, port, comstatus):
        self.device_name = devname
        self.ipaddress = ipaddress
        self.port_number = port
        self.is_alive = comstatus
        self.addres = (ipaddress, port)

#センサ制御機器クラス
class ComSensorControlDevice(ComDeviceInfoBase):
    
    #コンストラクタ
    def __init__(self, devname, ipaddress, port, comstatus, sensorlist):
        super().__init__(devname, ipaddress, port, comstatus)
        self.sensorlist = sensorlist

    #サーバとの通信
    def communicate_with_server(self, data, server_address):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.connect(server_address)
                    s.send(str(data).encode())
                except Exception as e:
                    print("Sensor control device communicates with server device : ", e, "\n")
                else:
                    break
                finally:
                    s.close()

#Android端末クラス
class ComAndroidDevice(ComDeviceInfoBase):

    #コンストラクタ
    def __init__(self, devname, ipaddress, port, comstatus, version):
        super().__init__(devname, ipaddress, port, comstatus)
        self.os_version = version

    #サーバとの通信
    def communicate_with_server(self, data, server_address):
        pass

#サーバ機器クラス
class ComServerDevice(ComDeviceInfoBase):
    """Server Device"""

    def __init__(self, devname, ipaddress, port, comstatus):
        super().__init__(devname, ipaddress, port, comstatus)





#インスタンス生成例
# android = ComDeviceInfoBase('xperia', '127.0.0.1', 55000, False)
# raspberrypi = ComDeviceInfoBase('rasperrypi4b', '162.198.127.123.3', 20000, False)

