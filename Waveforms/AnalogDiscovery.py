from ctypes import *
import time
import sys
import threading as th
from Waveforms.dwfconstants import *
from enum import Enum


if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")


class Echannel(Enum):
    ch_1 = 0
    ch_2 = 1
    ch_all = 2


class AnalogDiscovery2:

    def __init__(self):
        self.hdwf = c_int()
        self.samples = int()
        self.is_open_device = c_bool()
        self.check_ai = False
        self.check_ao = False
        self.sample_rate = None
        self.sample_num = None
        self.device_index = c_int(0)
        self.ai_th = None
        self.check_ai_th = True
        self.ai_data = None

    def viewVersion(self):
        version = create_string_buffer(16)
        dwf.FDwfGetVersion(version)
        print("DWF Version: " + str(version.value))

    def openDevice(self, device_index=-1):
        self.device_index = c_int(device_index)
        dwf.FDwfEnumDeviceIsOpened(self.device_index, byref(self.is_open_device))
        if not self.is_open_device:
            dwf.FDwfDeviceOpen(self.device_index, byref(self.hdwf))
            self.is_open_device = c_bool(True)

    def closeDevice(self):
        if self.is_open_device:
            self.stopAI()
            dwf.FDwfDeviceClose(self.hdwf)
            self.check_ao = False
            self.check_ai = False
            self.is_open_device = c_bool(False)

    def is_open(self):
        dwf.FDwfEnumDeviceIsOpened(self.device_index, byref(self.is_open_device))
        return self.is_open_device

    def is_start_ai(self):
        return self.check_ai

    def is_start_ao(self):
        return self.check_ao

    def get_serial(self):
        serial_num = create_string_buffer(16)
        dwf.FDwfEnumSN(self.device_index, serial_num)
        serial_num = str(serial_num.value)
        serial_num = serial_num.replace("b'", "")
        serial_num = serial_num.replace("'", "")
        return serial_num

    def get_sample_rate(self):
        return self.sample_rate

    def get_sample_num(self):
        return self.sample_num

    def startAI(self, channel=Echannel.ch_1, thread_mode=False):
        self.check_ai = True
        if thread_mode:
            channel = Echannel.ch_all
            self.check_ai_th = True
            dwf.FDwfAnalogInConfigure(self.hdwf, c_int(channel.value), c_int(1))
            self.ai_th = th.Thread(target=self.ai_loop_process)
            self.ai_th.setDaemon(True)
            self.ai_th.start()
        else:
            dwf.FDwfAnalogInConfigure(self.hdwf, c_int(channel.value), c_int(1))

    def stopAI(self):
        if self.check_ai:
            self.check_ai_th = False
            time.sleep(0.5)
            self.check_ai = False

    def setConfigAI(self, hzAcq, nSamples, mode=acqmodeSingle):
        self.sample_rate = hzAcq
        self.sample_num = nSamples
        self.samples = nSamples
        dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(0), c_bool(True))
        dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(0), c_double(10))
        dwf.FDwfAnalogInAcquisitionModeSet(self.hdwf, mode)  # (1)acqmodeScanShift (2)ScanScreen (3)Record
        dwf.FDwfAnalogInFrequencySet(self.hdwf, c_double(hzAcq))
        dwf.FDwfAnalogInBufferSizeSet(self.hdwf, c_int(self.samples))
        time.sleep(2)

    def getAI(self, channel=Echannel.ch_1):
        sts = c_byte()
        cValid = c_int(0)
        index = c_int(0)
        rgdSamples = (c_double * self.samples)()
        rgdSamples2 = (c_double * self.samples)()

        rgpy = [0.0] * len(rgdSamples)
        rgpy2 = [0.0] * len(rgdSamples)
        error_cnt = 0
        while True:
            dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(sts))
            dwf.FDwfAnalogInStatusSamplesValid(self.hdwf, byref(cValid))
            # get samples
            if channel != Echannel.ch_all:
                dwf.FDwfAnalogInStatusData(self.hdwf, c_int(channel.value), byref(rgdSamples), cValid)
                dwf.FDwfAnalogInStatusIndexWrite(self.hdwf, byref(index))
                for i in range(0, cValid.value):
                    rgpy[i] = rgdSamples[i]
                if cValid.value > 0:
                    return rgpy
                if error_cnt > 100:
                    return rgpy
            else:
                dwf.FDwfAnalogInStatusData(self.hdwf, c_int(0), byref(rgdSamples), cValid)
                dwf.FDwfAnalogInStatusIndexWrite(self.hdwf, byref(index))
                dwf.FDwfAnalogInStatusData(self.hdwf, c_int(1), byref(rgdSamples2), cValid)
                dwf.FDwfAnalogInStatusIndexWrite(self.hdwf, byref(index))
                for i in range(0, cValid.value):
                   rgpy[i] = rgdSamples[i]
                   rgpy2[i] = rgdSamples2[i]
                if cValid.value > 0:
                    return rgpy, rgpy2
                if error_cnt > 100:
                    return rgpy, rgpy2
            error_cnt += 0

    def ai_loop_process(self):
        while self.check_ai_th:
            self.ai_data = self.getAI(Echannel.ch_all)

    def startAO(self, channel=0):
        dwf.FDwfAnalogOutConfigure(self.hdwf, c_int(channel), c_int(1))
        self.check_ao = True

    def createSweep(self, startHz, stopHz, sweepSec, outVoltage=1.0, channel=0):
        channel = c_int(channel)
        startHz = float(startHz)
        stopHz = float(stopHz)
        sweepSec = float(sweepSec)
        dwf.FDwfAnalogOutNodeEnableSet(self.hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
        dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf, channel, AnalogOutNodeCarrier, funcSine)
        dwf.FDwfAnalogOutNodeSymmetrySet(self.hdwf, channel, AnalogOutNodeCarrier, c_double(0))
        dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, channel, AnalogOutNodeCarrier, c_double((stopHz+startHz)/2))
        dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, channel, AnalogOutNodeCarrier, c_double(outVoltage))
        dwf.FDwfAnalogOutNodeOffsetSet(self.hdwf, channel, AnalogOutNodeCarrier, c_double(0))
        dwf.FDwfAnalogOutNodeEnableSet(self.hdwf, channel, AnalogOutNodeFM, c_bool(True))
        dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf, channel, AnalogOutNodeFM, funcRampUp)
        dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, channel, AnalogOutNodeFM, c_double(1.0/sweepSec))
        dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, channel, AnalogOutNodeFM, c_double(100.0*(stopHz-startHz)/(startHz+stopHz)))
        dwf.FDwfAnalogOutNodeSymmetrySet(self.hdwf, channel, AnalogOutNodeFM, c_double(100))
        dwf.FDwfAnalogOutNodeOffsetSet(self.hdwf, channel, AnalogOutNodeFM, c_double(0))

    def __del__(self):
        self.closeDevice()
        self.check_ai = False
        self.check_ao = False


def get_devices():
    devices = c_int()
    dwf.FDwfEnum(c_int(0), byref(devices))
    return devices.value


def get_serial(device_index: int):
    device_index = c_int(device_index)
    serial_num = create_string_buffer(16)
    dwf.FDwfEnumSN(device_index, serial_num)
    serial_num = str(serial_num.value)
    serial_num = serial_num.replace("b'", "")
    serial_num = serial_num.replace("'", "")
    return serial_num


def get_device_index(serial_num: str):
    for i in range(get_devices()):
        if get_serial(i) == serial_num:
            return i

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    devices = get_devices()
    print("接続されたデバイス数:"+str(devices))

    for i in range(devices):
        print(str(i)+" SN: "+get_serial(i))

    Discovery = AnalogDiscovery2()

    Discovery.viewVersion()

    Discovery.openDevice()

    Discovery.createSweep(startHz=1000, stopHz=3000, sweepSec=0.05)
    Discovery.startAO(channel=0)
    Discovery.setConfigAI(nSamples=8192, hzAcq=163840, mode=acqmodeScanScreen)
    Discovery.startAI(thread_mode=True)

    plt.axis([0, 8192, -2, 2])
    plt.ion()
    hl, = plt.plot([], [])
    hl.set_xdata(list(range(0, Discovery.samples)))

    i = int(0)
    while True:
        i += 1
        if i == 100:
            break
        hl.set_ydata(Discovery.ai_data[0])
        plt.draw()
        plt.pause(0.03)

    Discovery.stopAI()
    Discovery.closeDevice()

