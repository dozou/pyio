from ctypes import *
import sys
import time

if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

#declare ctype variables
szerr = create_string_buffer(512)
dwf.FDwfGetLastErrorMsg(szerr)
print(szerr.value)

#declare ctype variables
IsInUse = c_bool()
hdwf = c_int()
channel = c_int()
hzfreq = c_double()
cdevices = c_int()

#declare string variables
devicename = create_string_buffer(64)
serialnum = create_string_buffer(16)

#print DWF version
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: " + str(version.value))

#enumerate and print device information
dwf.FDwfEnum(c_int(0), byref(cdevices))
print("Number of Devices: " + str(cdevices.value))

for i in range(0, cdevices.value):
    dwf.FDwfEnumDeviceName(c_int(i), devicename)
    dwf.FDwfEnumSN(c_int(i), serialnum)
    print("------------------------------")
    print("Device " + str(i) + " : ")
    print("t" + str(devicename.value))
    print("t" + str(serialnum.value))
    dwf.FDwfEnumDeviceIsOpened(c_int(i), byref(IsInUse))

    if not IsInUse:
        dwf.FDwfDeviceOpen(c_int(i), byref(hdwf))
        dwf.FDwfAnalogInChannelCount(hdwf, byref(channel))
        dwf.FDwfAnalogInFrequencyInfo(hdwf, None, byref(hzfreq))
        print("tAnalog input channels: " + str(channel.value))
        print("tMax freq: " + str(hzfreq.value))
        dwf.FDwfDeviceClose(hdwf)
        hdwf = c_int(-1)

# ensure all devices are closed
time.sleep(10)
dwf.FDwfDeviceCloseAll()
