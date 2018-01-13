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
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

"""
# class dataSet(object):
#     def __init__(self):
#         self.data = []
#         self._bool = True
#         self.path = 'test.csv'
# 
# 
# class write(threading.Thread):
#     def __init__(self, share_data):
#         threading.Thread.__init__(self)
#         self.df_amp = pd.DataFrame()
#         self.share_data = share_data
# 
#     def write_pandas(self, df):
#         self.df_amp = df
#         self.df_amp = self.df_amp.T
#         self.df_amp.to_pickle(self.share_data.path)
# 
#     def run(self):
#         print("test:")
#         self.num = 0
#         while self.share_data._bool:
#             self.df_amp[self.num] = pd.Series(self.share_data.data)
#             self.num += 1
#             time.sleep(0.001)
#         self.write_pandas(self.df_amp)
# 
#     def __del__(self):
#         print("del")
# 
# 
# class GetData(threading.Thread):
#     def __init__(self, share_data):
#         threading.Thread.__init__(self)
#         self.device = AnalogDiscovery2()
#         self.device.view_version()
#         self.device.open_device()
#         self.share_data = share_data
# 
#     def AnalogOut(self):
#         # self.device.create_sine_wave(1000, outVoltage=5.0)
#         self.device.create_sweep(startHz=100, stopHz=200, sweepSec=0.01)
#         self.device.start_ao(channel=0)
# 
#     def AnalogIn(self):
#         self.device.set_config_ai(nSamples=8192, hzAcq=163840, mode=dwfc.acqmodeScanScreen)
#         self.device.start_ai(thread_mode=True)
# 
#     def run(self):
#         self.AnalogOut()
#         self.AnalogIn()
#         plt.axis([0, 8192, -5.5, 5.5])
#         plt.ion()
#         hl, = plt.plot([], [])
#         hl.set_xdata(list(range(0, self.device.samples)))
#         i = int(0)
#         while self.share_data._bool:
#             i += 1
#             if i == 100:
#                 break
#             hl.set_ydata(self.device.ai_data[0])
#             self.share_data.data = self.device.ai_data
#             plt.draw()
#             plt.pause(0.001)
# 
# 
#     def __del__(self):
#         self.device.close_device()
#         self.device.check_ai = False
#         self.device.check_ao = False
# 
"""

class boolCase(object):
    def __init__(self):
        self._change = True
        self._next = False

class switchCase(threading.Thread):

    def __init__(self, bool):
        threading.Thread.__init__(self)
        self.bool = bool

    def run(self):
        while True:
            x = input('> ')
            if x in {'p', 'q'}:
                print("終了")
                self.bool._change = False
                break
            elif x == 'c':
                print("Next")
                self.bool._next = True
            else:
                print("キーが設定されていません")





if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    import termios

    devices = get_connection_count_analog_discovery2()
    print("接続されたデバイス数:"+str(devices))

    for i in range(devices):
        print(str(i) + " SN: " + get_serial_analog_discovery2(i))


    device = AnalogDiscovery2()
    device.view_version()

    device.open_device()

    device.create_sine_wave(1000, outVoltage=5.0)
    device.start_ao(channel=0)

    device.set_config_ai(nSamples=8192, hzAcq=163840, mode=dwfc.acqmodeScanScreen)
    device.start_ai(thread_mode=True)

    set_bool = boolCase()

    switch = switchCase(set_bool)
    switch.start()

    plt.axis([0, 8192, -5.5, 5.5])
    plt.ion()
    hl, = plt.plot([], [])
    hl.set_xdata(list(range(0, device.samples)))

    df_One = pd.DataFrame()
    df_Two = pd.DataFrame()
    numOne = 0
    numTwo = 0
    _test = False
    _calibrationOne = False
    _calibrationTwo = False

    i = int(0)
    while True:
        # time.sleep(0.05)

        if _calibrationOne == True:
            df_One[numOne] = pd.Series(device.ai_data[0])
            numOne += 1
        elif _calibrationTwo == True:
            df_Two[numTwo] = pd.Series(device.ai_data[0])
            numTwo += 1

        if set_bool._change == False:
            break
        elif set_bool._next == True:
            if _test == False:
                print("0度取得")
                _calibrationOne = True
                _test = True
                _calibrationTwo = False

            elif _test == True:
                print("90度取得")
                _calibrationOne = False
                _calibrationTwo = True
                _test = False

            set_bool._next = False

        hl.set_ydata(device.ai_data[0])
        plt.draw()
        plt.pause(0.025)


    device.stop_ai()
    device.close_device()


    # 0 deg get
    # 90 deg get
    # reg line cul
    # estimate

    switch.join()







"""
マルチスレッド化に向けてそのまま
    v = dataSet()
    print(v._bool)
    # path = 'test.csv'
    mt = GetData(v)
    write_th = write(v)
    time.sleep(0.5)
    mt.start()
    write_th.start()

    mt.join()
    write_th.join()
"""
