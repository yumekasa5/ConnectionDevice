"""センサからのデータを保存するクラスや関数"""
from datetime import datetime, date
import numpy as np
import pandas as pd

#日付、時刻、顔グリッド温度、推定環境温度, 測定距離、推定体温
date_now = date.today()
time_now = datetime.now().time()
test_array = np.array([[date_now, time_now.strftime('%H:%M'),  35.9, 25.0, 30.5, 36.4],
                       [date_now, time_now.strftime('%H:%M'), 36.3, 25.0, 25.5, 36.6]])
test_df = pd.DataFrame(test_array, 
                  columns=['日付', '時刻',  '顔グリッド温度[degC]', 
                           '推定環境温度[degC]','測定距離[cm]', '推定体温[degC]'])
# print(test_df)
output_path = '../result/output.csv'
test_df.to_csv(output_path, index = False)
