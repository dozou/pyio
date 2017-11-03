"""
肘関節角度推定をAnalogDiscovery2で実現

２点キャリブレーション

コメント：2017年度の建学祭に向けて取り急ぎ作成ー＞終わったら，直します．

作成者：栗原
制作日：2017/10/29
"""

from Devices.Waveforms.AnalogDiscovery import *
import threading
import time
from pandas import *
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import scipy as sp
import scipy.stats as stats
import sys


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


### デモ用，終わったら即消し
_gChange = True
_gBreak = True

class SwitchCase(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.bool = _gChange

    def run(self):
        global _gChange, _gBreak
        while True:
            com = input('> ')
            if com in {'p', 'q'}:
                break
            elif com == 'b':
                _gChange = False
            elif _gBreak == False:
                break
            else:
                print("なし")

def PutBar(per, barlen):
    perb = int(per/(100.0/barlen))
    s = '\r'
    s += '|'
    s += '='* (perb - 1)
    s += '>'
    s += '~'* (barlen - perb)
    s += '|'
    s += ' ' + (str(per) + '%').rjust(4) + '  '
    sys.stdout.write(s)

if __name__ == "__main__":
    ### AnalogDiscoveryのセッティング
    devices = get_connection_count_analog_discovery2()
    print("接続されたデバイス数:" + str(devices))

    for i in range(devices):
        print(str(i) + " SN: " + get_serial_analog_discovery2(i))

    device = AnalogDiscovery2()
    device.view_version()
    device.open_device()
    # wave = [1 if i < 2000 else 0 for i in range(4000)]
    # device.create_custom_wave(wave, 100, 2)
    device.create_sine_wave(outputWave=1000, outVoltage=5, channel=0)
    device.start_ao(channel=0)
    device.set_config_ai(nSamples=8000, hzAcq=160000, mode=dwfc.acqmodeScanScreen)
    device.start_ai(thread_mode=True)

    ### スイッチケースセット
    switch = SwitchCase()
    switch.start()

    ### dataFrameセット
    df_one = pandas.DataFrame()
    df_two = pandas.DataFrame()

    bar = 100

    print("２点キャリブレーション開始")
    print("0度取得")
    print("press the b key")
    _gChange = True
    while True:
        if _gChange == False:
            break
    _gChange = True
    # print("２点キャリブレーション開始")
    numOne = 0
    numTwo = 0
    barNum = 0
    print("0度取得開始")
    while _gChange:
        df_one[numOne] = pandas.Series([0, max(device.ai_data[0])])
        # print("test")
        numOne += 1
        # if numOne % 100 == 0:
        #     print(numOne)
        if numOne % int(5000/100) == 0:
            PutBar(barNum, bar)
            barNum += 1
        if numOne == 5000:
            PutBar(100, bar)
            break
    print("0度取得完了")
    print(" ")
    print("90度取得")
    print("press the b key")
    _gChange = True
    while True:
        if _gChange == False:
            break

    barNum = 0
    _gChange = True
    print("90度取得開始")
    while _gChange:
        df_one[numOne] = pandas.Series([90, max(device.ai_data[0])])
        numOne += 1
        numTwo += 1
        # if numOne % 100 == 0:
        #     print(numOne)
        if numTwo % int(5000/100) == 0:
            PutBar(barNum, bar)
            barNum += 1
        if numTwo == 5000:
            PutBar(100, bar)
            break
    print("90度取得完了")
    df_one = df_one.T
    a, b, r, p, stdError  = stats.linregress(df_one[1], df_one[0])
    print("y = ", a, "x + ", b)

    _gChange = True
    while True:
        if _gChange == False:
            break

    setX = [-1, 0, 1, 0]
    setY = [0, 0, 0, 1]

    plt.axis([-1.1, 1.1, -0.2, 1.2])
    # plt.axis('equal')
    plt.ion()
    hl, = plt.plot([], [], 'o', )
    hl.set_xdata(setX)
    hl.set_ydata(setY)
    nl, = plt.plot([], [], marker="o", lw=5, markersize=12, )

    y = 0
    print("推定開始")
    print("press the b key")
    print("終わらせる時は，")
    _gChange = True
    while _gChange:
        x = max(device.ai_data[0])
        y = a * x + b
        # y += 1
        # if y == 90:
        #     y = 0
        if y > 90:
            y = 90
            cirX = [-1, 0, 1 - (y / 90)]
            cirY = [0, 0, np.sqrt((y / 90) ** 2)]
        elif y < 0:
            y = 0
            cirX = [-1, 0, 1 - (y / 90)]
            cirY = [0, 0, np.sqrt((y / 90) ** 2)]
        else:
            cirX = [-1, 0, 1 - (y / 90)]
            cirY = [0, 0, np.sqrt((y / 90) ** 2)]
        nl.set_xdata(cirX)
        nl.set_ydata(cirY)
        plt.draw()
        plt.pause(0.001)
    _gBreak = False
    device.stop_ai()
    device.close_device()