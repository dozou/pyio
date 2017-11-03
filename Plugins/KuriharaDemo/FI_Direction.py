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


if __name__ == "__main__":
    devices = get_connection_count_analog_discovery2()
    print("接続されたデバイス数:" + str(devices))

    for i in range(devices):
        print(str(i) + " SN: " + get_serial_analog_discovery2(i))

    device = AnalogDiscovery2()
    device.view_version()
    device.open_device()

    ### カスタム出力 ###
    # wave = [(1.0 * (i / (4095 - 1))) - 0.5 for i in range(4095)]  # リスト内包表記
    # wave = [1 if i < 2000 else 0 for i in range(4000)]
    wave = [4 if i < 4000 else -1 for i in range(8000)]
    device.create_custom_wave(wave, 100, 4)
    ### 単振動出力 ###
    # device.create_sine_wave(outputWave=1000, offSet=2, outVoltage=1, channel=0)
    ### スイープ出力 ###
    # device.create_sweep(startHz=100, stopHz=300, sweepSec=0.05)

    # for n in range(40):
    #     wave[n] = [1 if i < 4000 else 0.5 for i in range(8000)]

    device.start_ao(channel=0)
    device.set_config_ai(nSamples=8192, hzAcq=163840, mode=dwfc.acqmodeScanScreen)
    device.start_ai(thread_mode=True)

    plt.axis([0, 8192, -5.0, 5.0])
    plt.ion()
    hl, = plt.plot([], [])
    hl.set_xdata(list(range(0, device.samples)))

    i = int(0)
    while True:
        i += 1
        if i == 100:
            # device.create_sine_wave(outputWave=1000, outVoltage=1, channel=0)
            device.create_square_wave(outputWave=200, outVoltage=1, channel=0)
            device.start_ao(channel=0)
        if i == 200:
            break
        hl.set_ydata(device.ai_data[0])
        plt.draw()
        plt.pause(0.025)

    device.stop_ai()
    device.close_device()






