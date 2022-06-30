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
import numpy as np

def gaussian_filter(array):
    """ガウシアンフィルタ"""
    return array

def calc_offset_by_distance(distance, slope, intercept):
    """距離によるオフセットの算出"""
    offset = slope * distance + intercept
    return offset

def get_facegrids_degC(facegrid_array):
    """顔と推定されるグリッドの平均値を算出"""
    ave_grid_degC = (facegrid_array[4, 5] + facegrid_array[4, 6] 
                   + facegrid_array[5, 5] + facegrid_array[5, 6]) / 4
    return ave_grid_degC

def estimate_body_temp_degC(distance_cm, raw_grids, temp_offset):
    """体温推定"""
    grids = gaussian_filter(raw_grids)
    facegrids = get_facegrids_degC(grids)
    ret = facegrids + temp_offset
    return ret