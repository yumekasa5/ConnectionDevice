"""センサからのデータを保存するクラスや関数"""
import os
from datetime import datetime, date
import numpy as np
import pandas as pd

class SensorDataLog:
    """センサからの出力データのロギング"""
     
    OUTPUT_PATH = '../result/sensordatalog.csv'
    """データログ出力先のパス"""

    def __init__(self, facetemp_degC, distance_cm, environment_temp_degC, estimate_bofy_temp_degC) -> None:
        self.ft = facetemp_degC
        self.dis = distance_cm
        self.envt = environment_temp_degC
        self.estbt = estimate_bofy_temp_degC
        
    def create_df(self) -> None:
        """ロギングデータ整形(DataFrame作成)"""
        date_now = date.today()
        time_now = datetime.now().time()
        logging_array = np.array([[date_now, time_now.strftime('%H:%M'),         #日付、時刻
                                   self.ft, self.dis, self.envt, self.estbt]])   #顔グリッド温度、推定環境温度, 測定距離、推定体温
        self.df = pd.DataFrame(logging_array, 
                        columns=['日付', '時刻',  '顔グリッド温度[degC]', 
                                 '推定環境温度[degC]','測定距離[cm]', '推定体温[degC]'])

    def to_csv(self) -> None:
        """CSVファイルに出力"""
        is_file = os.path.isfile(self.OUTPUT_PATH)
        if is_file:
            self.df.to_csv(self.OUTPUT_PATH, mode='a', header=False, index=False)
        else:
            self.df.to_csv(self.OUTPUT_PATH, mode='w', index=False)
