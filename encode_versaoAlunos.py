from suaBibSignal import *
import sys
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import time

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    signal = mySignal()
    fs = signal.fs
    gotNumber = False
    while not gotNumber:
        try:
            numbero = str(input('Digite um número de 0 a 9:'))
            gotNumber = True
            # if number >=0 and number <=9:
            #     gotNumber = True
            # else: 
            #     print('Por favor digite um número de 0 a 9')
        except:
            print('POR FAVOR DIGITE UM NUMERO RS') 

    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    #declare uma variavel com a frequencia de amostragem, sendo 44100

    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    duration = signal.duration #tempo em segundos que ira emitir o sinal acustico 
      
#relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    for i in range(0, len(numbero)):
        if numbero[i] == '#':
            number = numbero[i]
        else:
            number = int(numbero[i])
        freqX, freqY = signal.numberToFreq(number)

        print("Gerando Tons base")
        
        #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y 
        #use para isso sua biblioteca (cedida)
        #obtenha o vetor tempo tb.
        #deixe tudo como array
        signalX = signal.generateSin(freqX, gainX, duration, fs)
        signalY = signal.generateSin(freqY, gainX, duration, fs)

        #printe a mensagem para o usuario teclar um numero de 0 a 9. 
        #nao aceite outro valor de entrada.
        print("Gerando Tom referente ao símbolo : {}".format(number))
        
        #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
        plt.plot(signalX[0], signalX[1] + signalY[1])
        plt.plot(signalX[0], signalX[1])
        plt.plot(signalX[0], signalY[1])
        
        #printe o grafico no tempo do sinal a ser reproduzido
        # reproduz o som
        sd.play(signalX[1] + signalY[1], fs)
        # aguarda fim do audio
        sd.wait()
        time.sleep(1.5)
    plt.show()

if __name__ == "__main__":
    main()
