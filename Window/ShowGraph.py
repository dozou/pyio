#coding:utf-8
from abc import ABCMeta, abstractmethod
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

class Graph:
    timer = None
    def __init__(self, graphname, xsize, ysize, number):
        self.win=pg.GraphicsWindow(title=graphname)
        self.win.resize(xsize,ysize)
        self.p1=self.win.addPlot(title=graphname)
        self.gnum=number
        self.curve=[]
        self.color=['y','g']
        for num in range(0,self.gnum):
            self.curve.append(self.curve)
            self.curve[num] = self.p1.plot(pen=self.color[num])

    def set_realtime(self, timeout=10):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.loop)
        self.timer.start(timeout)

    def set_label(self,left,lunits,bottom,bunits):
        self.p1.setLabel('left',left,units=lunits)
        self.p1.setLabel('bottom',bottom,units=bunits)

    def set_xrange(self,xmin,xmax):
        self.p1.setXRange(xmin,xmax,padding=0)

    def set_yrange(self,ymin,ymax):
        self.p1.setYRange(ymin,ymax,padding=0)

    @abstractmethod
    def loop(self):
        print("LoopProcess")

    def show(self,ydata,xdata,start,size):
        for num in range(0,self.gnum):
            self.curve[num].setData(x=xdata[start:size],y=ydata[num*size+start:(num+1)*size])

if __name__ == '__main__':
    import sys
    import math

    #グラフ表示の設定
    gph1=Graph("Example of showing graph", 1000, 600, 1)
    gph1.set_label("Voltage", 'V', "Time", 'Sec')

    #サンプルデータ生成
    bufferSize=1000
    sampleRate=2000
    step = 1. / sampleRate
    xtime = np.arange(bufferSize) * step
    data = np.zeros((bufferSize,), dtype=np.float64)
    for num in range(0,bufferSize):
        data[num]=math.sin(math.pi/180 * num* 360/bufferSize)

    #グラフの表示
    gph1.show(data,xtime,0,bufferSize)
    gph1.set_realtime()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
