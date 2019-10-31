import modulador
import demodulador

modular = int(input('Modular ou Demodular? '))

if modular == 0:
    a = modulador.Modulador()
    a.readSound()
    # a.playSound()
    a.modulateSignal()
    a.playSignal()
    a.plotSignal()
else: 
    b = demodulador.Demodulador()
    b.recordSignal()
    b.playSignal()
    b.demodulate()