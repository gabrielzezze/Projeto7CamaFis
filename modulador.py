import soundfile as sf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from suaBibSignal import *
from scipy import signal as signal

class Modulador:
    def __init__(self):
        self.fs = 44100
        self.portadora = 14000
        self.time = 5
        self.canalX = None
        self.canalXNormalized = None
        self.canalY = None
        self.canalYNormalized = None
        self.mySignal = mySignal()
        self.signalX = None
        self.signalY = None
        self.xAM = None
        self.yAM = None

    def readSound(self):
        print('READING SOUND')
        # audio = sf.read('./old-phone-ringing', -1, 1000000, 1220500)
        # sampleRate = audio[1]
        # audio = audio[0]
        # self.time = len(audio)/sampleRate
        # self.canalX = [a[0] for a in audio]
        # self.canalY = [a[1] for a in audio]
        audio = sd.rec(int(self.time*self.fs), self.fs, channels=1)
        sd.wait()
        self.canalX = [a[0] for a in audio]
        self.canalXNormalized = self.canalX/max([abs(a) for a in self.canalX])

        nyq_rate = self.fs/2 #sampleRate/2
        width = 5/nyq_rate
        ripple_db = 60
        N, beta = signal.kaiserord(ripple_db, width)
        cutoff_hz = 4000
        taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        self.signalX = signal.lfilter(taps, 1, self.canalXNormalized)

    def playSound(self):
        print('PLAYING SOUND')
        sd.play(self.signalX, self.fs)
        sd.wait()


    def modulateSignal(self):
        print('MODULATING SIGNAL')
        portadora = self.mySignal.generateSin(self.portadora, 1, self.time, self.fs)
        self.xAM = self.signalX*portadora[1]

    def playSignal(self):
        print('PLAYING SIGNAL')
        sd.play(self.xAM, self.fs)
        sd.wait()

    def plotSignal(self):
        print('PLOTING SIGNAL')
        plt.plot(np.linspace(0.0, self.time, self.time*self.fs), self.canalX)
        plt.title('SINAL ORIGINAL (tempo)')
        plt.show()
        signalXFourrier = self.mySignal.calcFFT(self.canalX, self.fs)
        plt.plot(signalXFourrier[0], signalXFourrier[1])
        plt.title('SINAL ORIGINAL (freq)')
        plt.show()

        plt.plot(np.linspace(0.0, self.time, self.time*self.fs), self.canalXNormalized)
        plt.title('SINAL NORMALIZADO (tempo)')
        plt.show()
        signalXFourrier = self.mySignal.calcFFT(self.canalXNormalized, self.fs)
        plt.plot(signalXFourrier[0], signalXFourrier[1])
        plt.title('SINAL NORMALIZADO (freq)')
        plt.show()

        plt.plot(np.linspace(0.0, self.time, self.time*self.fs), self.signalX)
        plt.title('SINAL FILTRADO (tempo)')
        plt.show()
        signalXFourrier = self.mySignal.calcFFT(self.signalX, self.fs)
        plt.plot(signalXFourrier[0], signalXFourrier[1])
        plt.title('SINAL FILTRADO (freq)')
        plt.show()

        plt.plot(np.linspace(0.0, self.time, self.time*self.fs), self.xAM)
        plt.title('SINAL MODULADO (tempo)')
        plt.show()
        signalXFourrier = self.mySignal.calcFFT(self.xAM, self.fs)
        plt.plot(signalXFourrier[0], signalXFourrier[1])
        plt.title('SINAL MODULADO (freq)')
        plt.show()
