from ctypes import *
import math
import time
import matplotlib.pyplot as plt
import sys
from .dwfconstants import *


if __name__ == "__main__" :

    if sys.platform.startswith("win"):
        dwf = cdll.dwf
    elif sys.platform.startswith("darwin"):
        dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    else:
        dwf = cdll.LoadLibrary("libdwf.so")

    #declare ctype variables
    hdwf = c_int()
    sts = c_byte()
    secRange = 0.00001
    hzAcq = 32000
    nSamples = 8192
    rgdSamples = (c_double*nSamples)(0.0)
    cValid = c_int(0)
    channel = c_int(0)

    #print DWF version
    version = create_string_buffer(16)
    dwf.FDwfGetVersion(version)
    print("DWF Version: "+str(version.value))

    #open device
    print("Opening first device")
    dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

    if hdwf.value == 0:
        szerr = create_string_buffer(512)
        dwf.FDwfGetLastErrorMsg(szerr)
        print(szerr.value)
        print("failed to open device")
        quit()

    print("Preparing to read sample...")

    hzStart = 1000
    hzStop = 4000
    secSweep = 0.05

    print("Generating sine wave...")
    dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcSine)
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double((hzStop+hzStart)/2))
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1))
    dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(0))

    dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeFM, c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeFM, funcRampUp)
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeFM, c_double(1.0/secSweep))
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeFM, c_double(100.0*(hzStop-hzStart)/(hzStart+hzStop)))
    dwf.FDwfAnalogOutSymmetrySet(hdwf, channel, AnalogOutNodeFM, c_double(50.0))
    dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeFM, c_double(0))
    dwf.FDwfAnalogOutConfigure(hdwf, channel, c_bool(True))

    #set up acquisition
    dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))
    dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeScanScreen) #(1)acqmodeScanShift (2)ScanScreen (3)Record
    dwf.FDwfAnalogInFrequencySet(hdwf, c_double(hzAcq))
    dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(nSamples))

    #wait at least 2 seconds for the offset to stabilize
    time.sleep(2)

    #begin acquisition
    dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))

    plt.axis([0, len(rgdSamples), -2, 2])
    plt.ion()
    hl, = plt.plot([], [])
    hl.set_xdata(list(range(0, len(rgdSamples))))

    while True:
        dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))

        dwf.FDwfAnalogInStatusSamplesValid(hdwf, byref(cValid))

        # get samples
        dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(rgdSamples), cValid)
        print(cValid.value)
        rgpy = [0.0]*len(rgdSamples)
        for i in range(0, cValid.value):
            rgpy[i] = rgdSamples[i]
        hl.set_ydata(rgpy)
        plt.draw()
        plt.pause(0.03)
