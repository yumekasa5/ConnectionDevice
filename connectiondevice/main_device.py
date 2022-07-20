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
"""My device System"""
from concurrent.futures import ThreadPoolExecutor
from .mydevice import *

#executerの生成
light_executer = ThreadPoolExecutor(max_workers=4)
screen_executer = ThreadPoolExecutor(max_workers=1)

def main():
    logger.debug('[START] MyDevice System')

    mydev = MyDevice()
    # mydev.get_test_grid_data()
    screen_executer.submit(mydev.screen_change_loop)
    light_executer.submit(mydev.socket_lit)

    logger.debug('[END] MyDevice System')

