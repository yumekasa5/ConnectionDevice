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