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

"""温度データの補正"""
from curses import raw
import numpy as np
from typing import List

def gaussian_filter(src: np.ndarray) -> np.ndarray:
    """ガウシアンフィルタ"""
    kernel = np.array([[1/16, 2/16, 1/16],         #カーネル(size:3x3)
                       [2/16, 4/16, 2/16],
                       [1/16, 2/16, 1/16]])
    m, n = kernel.shape

    #畳み込みしない領域の幅
    d = int((m-1)/2)
    h, w = src.shape[0], src.shape[1]
    dst = src.copy()

    #空間フィルタリング
    for y in range(d, h - d):
        for x in range(d, w -d):
            dst[y][x] = np.sum(src[y-d:y+d+1, x-d:x+d+1] * kernel)
    
    return dst

def calc_offset_by_distance(distance: float, slope: float, intercept: float) -> float:
    """距離によるオフセットの算出"""
    offset = slope * distance + intercept
    return offset

def get_facegrids_degC(facegrid_array: List[float]) -> float:
    """顔と推定されるグリッドの平均値を算出"""
    ave_grid_degC = (facegrid_array[4, 5] + facegrid_array[4, 6] 
                   + facegrid_array[5, 5] + facegrid_array[5, 6]) / 4
    return ave_grid_degC

def estimate_body_temp_degC(raw_grids: List[float], temp_offset: float) -> float:
    """体温推定"""
    grids = gaussian_filter(raw_grids)
    facegrids = get_facegrids_degC(grids)
    ret = facegrids + temp_offset
    return ret

def estimate_env_temp_degC(raw_grids: List[List[float]], pos_exclude: List[List[int]]) -> float:
    """環境温度の推定"""
    env_temp_degC = 0.0
    h, w = np.shape(raw_grids)[0], np.shape(raw_grids)[1]

    #環境温度の推定に利用するグリッド数の算出
    if (pos_exclude == [[]]):
        cnt = h * w
    else:
        cnt = h * w - len(pos_exclude)

    #人体以外のグリッドの平均値算出
    for y in range(0, h):
        for x in range(0, w):
            if ([y, x] in pos_exclude):
                env_temp_degC += 0
            else:
                env_temp_degC += raw_grids[y][x]
    env_temp_degC /= cnt
    return env_temp_degC
        