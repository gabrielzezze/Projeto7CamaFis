#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import *
import sys
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import time
import peakutils

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    signal = mySignal()
    fs = signal.fs
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs #taxa de amostragem
    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa
    duration = signal.duration #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print('INICIANDO EM 3')
    time.sleep(1)
   #faca um print informando que a gravacao foi inicializada
    print('INICIANDO CAPTURA')
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)

    audio = sd.rec(int(duration*fs), fs, channels=1)
    sd.wait()

    audio = [a[0] for a in audio]

    # audioF = []
    # for a in audio: 
    #     if a[0] < 2000 and a[0] > 600:
    #         audioF.append(a[0])
    #     else:
    #         audioF.append(0)
    print("FIM")
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t = np.linspace(0.0, duration, fs/duration)

    # plot do gravico  áudio vs tempo!


    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias

    xf, yf = signal.calcFFT(audio, fs)

    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
    index = peakutils.indexes(yf, 0.05, min_dist=50)
    picos = [xf[i] for i in index]
    for pico in picos:
        print('PICO: {}'.format(pico))
    delta = 10
    for index in signal.table:
        numero = signal.table[index]
        if numero[1] - delta <= picos[0] <= numero[1] + delta and numero[0] - delta <= picos[1] <= numero[0] + delta:
            print('\nTecla: {}\n'.format(index))
            break
    
    #printe os picos encontrados! 
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
