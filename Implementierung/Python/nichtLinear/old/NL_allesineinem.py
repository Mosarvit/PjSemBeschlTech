# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 13:11:53 2017
reviewed 13.2.18
@author: denys
"""
import computea as param
from old import NL_vorverzerrung
import computeU_quest_fromBBsignal
import getH
import numpy as np
from Helpers import writeAWG, writeDSO
import computeU_quest_fromAnySignal
#import matplotlib.pyplot as plt
#import copy

#Übertragungsfunktion messen
#fmax, Vpp, bits=10, writeAWG=True, showPlots=True, createCSV=True, formatOutput=1, modus=False)

[frq, H, PhaseH] = getH.compute(80e6,40e-3,10,True,True,True,1,False)                          #ÜBERPRÜFEN OB PHASE BEREINIGT




#Eingangssignal berechnen
#signal=computeUin.computeUin(f_rep, f_bb, f_g, Samplingrate)
signal= computeU_quest_fromBBsignal.compute(900e3, 5e6, 80e6, 1e9, frq, H, PhaseH)                               #SPEICHERT JETZT SIGNAL ALS CSV

#linear Vorverzerrtes Signal auf AWG geben
samplerateAWG=999900000 #Samplerate des AWG Signals 
vpp=200e-3 #Vpp die das awg ausgeben soll
[x, y, z]= writeAWG.writeAWG(signal[1], samplerateAWG, vpp) #Rückbage wird nicht benötigt


"""
bis hier geht safe alles, hat mehrfach mit diesen einstellungen funktioniert
Teil weiter unten noch nicht getestet
"""

#Signal am Gap messen das durch linear vorverzerrtes Signal entseht
fmax=80e6
samplerateOszi = 100*samplerateAWG
[time, dataUin, dataUout] = writeDSO.writeDSO(samplerateOszi, vpp, fmax, signal[1])

# Reduce time vector and signal to one period
periodTime = 1/900e3
tmpTime = periodTime - time[0]
ind = np.argmin(abs(time - tmpTime)) #find next index
time = time[0:ind]
dataUin = dataUin[0:ind]
dataUout = dataUout[0:ind]

##Nichtlinearer Teil
#gemessenes Ausgangssignal mit linearer Übertragungsfunktion zurückrechnen
u_mid =  computeU_quest_fromAnySignal.compute(dataUout, H, PhaseH, frq)    #kann nur 900kHz             #INDIZES IN DER FOR SCHLEIFE?

#Parameter Nl Vorverzerrung
N=3
in_pp=vpp

#Kennlinie berechnen
[ a, K ] = param.compute(dataUin, in_pp, u_mid, N)                                       #NORMIERUNG PRÜFEN


U=np.column_stack((time,dataUin))
U_nl = NL_vorverzerrung.NL_vorverzerrung(U, in_pp, K)                                     #speichert kennlinie und signal als csv

##write awg NL
writeAWG.writeAWG(U_nl[:, 1], samplerateAWG, in_pp)
