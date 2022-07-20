#Version
MYDEVICE_VERSION = '10.00'

#Mode
SYSTEM_MODE = False

#I2C address
I2C_ADDR_AMG8833 = 0x68
I2C_ADDR_VL53L0X = 0x29
I2C_ADDR_THERMISTER = 0xE

#IP address
IP_SERVER = '192.168.12.55'
IP_RASP = '192.168.12.52'
IP_ANDROID = '192.168.12.43'

#Port number
PORT_SCREEN_CHANGE1 = 55000
PORT_SCREEN_CHANGE2 = 25000
PORT_SERVER = 40000
PORT_SENSOR = 30000
PORT_LED = 20000
PORT_TEMP = 24000

#Range(distance[cm])
MAX_DISTANCE_CM = 80
MIN_DISTANCE_CM = 10

#Range(body temparature[℃])
ALART_BODY_TEMP_DEGC = 37.5
MIN_BODY_TEMP_DEGC = 35.0

#Correct temparature coeficient
DIS_SLOPE = 0.0671
DIS_INTERCEPT = 7.82
ENV_SLOPE = 0.0
ENV_INTERCEPT = 0.0

#Position of no used grids for estimating environment temperature
NO_USED_GRIDS_POS = [[2, 0], [2, 1],
                     [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5],
                     [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5],
                     [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5],
                     [6, 0], [6, 1], [6, 2], [6, 3], [6, 4], [6, 5],]