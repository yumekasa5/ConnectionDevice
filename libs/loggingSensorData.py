"""センサからのデータを保存するクラスや関数"""
import numpy as np
import pandas as pd

#source test
df = pd.DataFrame(np.array([[1, 2, 3], [5, 6, 7]]), 
                  columns=['facegrid temp[degC]', 'distance[cm]', 'body temp[degC]'])
print(df)
