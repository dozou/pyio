import os
import sys
import signal
import time
import libPyCFS as cfs

ENUM = cfs.axis
cfs.open_device("/dev/tty.usbmodem16060261")
cfs.resetOffset()


a = 0
test = 2.0
while a < 50:
    test = cfs.getForce(ENUM.Z_FORCE) / 1.00
    print(test)
    a += 1
    time.sleep(0.1)


cfs.clearDevice()