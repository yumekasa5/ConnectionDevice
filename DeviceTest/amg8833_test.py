from SensorDevice.temp_measure_amg8833 import AMG8833_8x8

#8x8のグリッド温度データをコンソールに表示
mydev = AMG8833_8x8()
gridtemp = mydev.get_grid_temp_degC
print(gridtemp)