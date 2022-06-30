"""温度補正における数値計算のテスト"""
from ..connectiondevice.libs.correct_temp import *

def test_gaussian_filter():
    result = gaussian_filter([])
    assert result

def test_calc_offset_by_distance():
    result = calc_offset_by_distance(30, 5, 5)
    assert result == 155

def test_get_facegrids_degC():
    result = get_facegrids_degC([])
    assert result == None

def test_estimate_body_temp_degC():
    result = estimate_body_temp_degC(30, [], 10)
    assert result == 36.5