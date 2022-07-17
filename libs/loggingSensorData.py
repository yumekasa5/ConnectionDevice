"""センサからのデータを保存するクラスや関数"""
from datetime import datetime, date
import numpy as np
import pandas as pd

#日付、時刻、顔グリッド温度、測定距離、推定体温
date_now = date.today()
time_now = datetime.now().time()
data_array = np.array([[date_now, time_now,  35.9, 30.5, 36.4],
                       [date_now, time_now, 36.3, 25.5, 36.6]])
df = pd.DataFrame(data_array, 
                  columns=['date', 'time',  'facegrid temp[degC]', 'distance[cm]', 'body temp[degC]'])
print(df)
