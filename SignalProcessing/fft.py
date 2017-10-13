#coding:utf-8
import scipy.fftpack
from PyQt5.QtCore import *
from Window.ShowGraph import *
from Waveforms.AnalogDiscovery import *
from pylab import *


class FFT:
    sampleRate = 0
    sampleNum = 0
    freq_list = None
    device = None

    def __init__(self):
        super(FFT, self).__init__()

    def config_ai(self, sampleRate, sampleNum):
        self.sampleRate = sampleRate
        self.sampleNum = sampleNum
        self.device.setConfigAI(hzAcq=self.sampleRate,
                                nSamples=self.sampleNum,
                                mode=acqmodeSingle)
        self.device.startAI(thread_mode=True)
        self.freq_list = scipy.fftpack.fftfreq(self.sampleNum, d=1.0/self.sampleRate)
        time.sleep(1)

    def set_device(self, device):
        self.device = device

    def get(self, channel=0):
        if not self.device.check_open:
            return
        fft_data = scipy.fftpack.fft(self.device.ai_data[channel])
        fft_data = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in fft_data]
        return fft_data


class RawSignalViewer(Graph):
    device = None

    def loop(self):
        # FFTを行いながらリアルタイム表示
        sample = self.device.ai_data[0]
        window = np.hamming(len(sample))
        #sample = window * sample
        sampleList = [0] * len(sample)
        for i in range(0, len(sample)):
            sampleList[i] = i
        self.set_xrange(0, 3200)
        self.show(sample, sampleList, 0, len(sample))

    def set_device(self, device):
        self.device = device[0]


class FFTAnalyzer(Graph):
    device = None

    def loop(self):
        # FFTを行いながらリアルタイム表示
        sample = self.device.ai_data[0]
        sample_rate = self.device.get_sample_rate()
        sample_num = self.device.get_sample_num()
        window = np.hamming(len(sample))
        X = scipy.fftpack.fft(sample)
        freqList = scipy.fftpack.fftfreq(sample_num, d=1.0/sample_rate)

        amplitudeSpectrum = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
        self.set_xrange(0, 8000)
        self.show(amplitudeSpectrum, freqList, 0, len(freqList))

    def set_device(self, device):
        self.device = device


def to_fft(wave_data):
    nfft = len(wave_data)
    out_data = np.fft.fft(wave_data, nfft)
    return out_data


def to_psd(spectrum_data):
    out_data = [i.imag**2 + i.real**2 for i in spectrum_data]
    out_data = np.array(out_data)
    return out_data


def to_fft2d(wave_data):
    nfft = len(wave_data[0])
    out_data = np.empty([len(wave_data),nfft], np.complex)
    for i, data in enumerate(wave_data):
        out_data[i] = np.fft.fft(wave_data[i], nfft)
    return out_data


def to_psd2d(spectrum_data):
    nfft = len(spectrum_data[0])
    out_data = np.empty([len(spectrum_data),nfft], np.float)
    for i,data in enumerate(spectrum_data):
       out_data[i] = [i.imag**2 + i.real**2 for i in data ]
    return out_data