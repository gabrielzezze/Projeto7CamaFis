import soundfile as sf
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from suaBibSignal import *
from scipy import signal as signal

class Demodulador:
    def __init__(self):
        self.fs = 44100
        self.portadora = 14000
        self.time = 5
        self.mySignal = mySignal()
        self.modulatedSignal = None
        self.desmodulatedSignal = None


    
    def recordSignal(self):
        print('RECORDING')
        audio = sd.rec(int(self.time*self.fs), self.fs, channels=1)
        sd.wait()
        self.modulatedSignal = [a[0] for a in audio]

    def playSignal(self):
        sd.play(self.modulatedSignal, self.fs)
        sd.wait()

    def demodulate(self):
        print('DEMODULATING')
        portadora = self.mySignal.generateSin(self.portadora, 1, self.time, self.fs)
        self.desmodulatedSignal = self.modulatedSignal*portadora[1]

        nyq_rate = self.fs/2
        width = 5/nyq_rate
        ripple_db = 60
        N, beta = signal.kaiserord(ripple_db, width)
        cutoff_hz = 4000
        taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        signalFiltered = signal.lfilter(taps, 1, self.desmodulatedSignal)
        maxValue = max(abs(signalFiltered))
        signalFiltered /= maxValue

        print('PLAYING')
        sf.write('entrega.ogg', signalFiltered, self.fs)
        sf.write('entrega1.wav', signalFiltered, self.fs)
        sd.play(signalFiltered, self.fs)
        sd.wait()

