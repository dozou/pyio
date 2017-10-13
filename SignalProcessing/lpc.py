#coding:utf-8
import scipy.fftpack
from PyQt5.QtCore import *
from Experiments.lpc import *
from Window.ShowGraph import *
from Waveforms.AnalogDiscovery import *
from pylab import *


class LPCAnalyzer(Graph):
    def __init__(self, graphname, xsize, ysize, number):
        super(LPCAnalyzer, self).__init__(graphname, xsize, ysize, number)
        self.device = None
        self.lpc_order = 256

    def loop(self):
        # FFTを行いながらリアルタイム表示
        sample = self.device.ai_data[0]
        sample_rate = self.device.get_sample_rate()
        sample_num = self.device.get_sample_num()
        r = auto_correlate(sample)
        a, e = levinson_durbin(r, self.lpc_order)
        w, h = scipy.signal.freqz(np.sqrt(e), a, sample_num, "whole")
        amplitudeSpectrum = [np.sqrt(i.real**2 + i.imag**2) for i in h]
        freqList = scipy.fftpack.fftfreq(sample_num, d=1.0/sample_rate)

        self.set_xrange(0, 8000)
        self.set_yrange(0, 1500)
        self.show(amplitudeSpectrum, freqList, 0, len(freqList))

    def set_device(self, device):
        self.device = device
