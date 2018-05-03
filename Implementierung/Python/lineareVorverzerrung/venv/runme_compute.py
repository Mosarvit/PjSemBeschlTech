# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 10:00:41 2017

%   Wiederholfrequenz f_rep
%   Barrier_Bucket Frequenz f_bb
%   Grenzfrequenz f_g

@author: denys
"""

import visa
import time
import matplotlib.pyplot as plt
import numpy as np
import computeUin
import getH
#import csv

"""
# Übertragungsfunktion einlesen für Tests

blub3 = open("Uefkt_exp155b.csv", "r")
reader3 = csv.reader(blub3, delimiter = ',')
for row in reader3:
    Lneu3 = []
    Lneu3.extend(reader3)
Hampl = []
Hphase = []
freqP =[]
for i in range (0,len(Lneu3)):
    Hphase.append(Lneu3[i][2])
    freqP.append(Lneu3[i][0])
    Hampl.append(Lneu3[i][1])


H = [float(i) for i in Hampl]
PhaseH = [float(i) for i in Hphase]
frq = [float(i) for i in freqP]
"""
#return(frq, H, PhaseH)  
#fmax, Vpp, bits=10, writeAWG=True, showPlots=True, createCSV=True, formatOutput=1, modus=False)
[frq, H, PhaseH] = getH.compute(80e6,40e-3,9,True,True,True,2,False) #Übertragungsfunktion berechnen

#Eingangssignal berechnen
#signal=computeUin.computeUin(f_rep, f_bb, f_g, Samplingrate) PHASE IN BOGENMASS???
signal=computeUin.computeUin(900e3,5e6,80e6,1e9, frq, H, PhaseH) 

fig = plt.figure()
plt.plot(signal[0]*1e6,signal[1])
plt.grid(True)
plt.ylabel(r'$Uin$')
plt.xlabel(r'$t$ in $us$')
plt.show()

#AWG Parameter
samplerateAWG=999900000 #Samplerate des AWG Signals
awg_volt=40e-3 #Vpp des AWG Signals

# Connect to Instruments
rm = visa.ResourceManager()
rs = rm.list_resources()
for i in range (0,len(rs)):
    pruf=rs[i]
    test=pruf.find("USB")
    if test != -1:
        index=i
awg_id = rs[index]
AWG = rm.open_resource(awg_id)

    ##################################################
    ################## Write to AWG ##################
    ##################################################

AWG.write("*RST") 
#time.sleep(5)
AWG.write("DATA:VOLatile:CLEar")
#time.sleep(5)
myrange=max(abs(max(signal[1])),abs(min(signal[1])))
 #Data Conversion from V to DAC levels
data_conv = np.round(signal[1]*32766/myrange);  
data_conv = ",".join(str(e) for e in data_conv)
AWG.write("SOURce1:DATA:ARBitrary:DAC myarb ," + data_conv)
time.sleep(10)
AWG.write("SOURce1:FUNCtion:ARBitrary 'myarb'")
time.sleep(10)
AWG.write("SOURce1:FUNCtion ARB") #USER
AWG.write("DISPlay:FOCus CH1")
AWG.write("DISPlay:UNIT:ARBRate FREQuency")
AWG.write("SOURce1:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
AWG.write("SOURce2:DATA:ARBitrary:DAC myarb ," + data_conv)
AWG.write("SOURce2:FUNCtion:ARBitrary 'myarb'")
time.sleep(10)
AWG.write("SOURce2:FUNCtion ARB") #USER
AWG.write("DISPlay:FOCus CH2")
AWG.write("DISPlay:UNIT:ARBRate FREQuency")
AWG.write("SOURce2:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
AWG.write("FUNC:ARB:SYNC")
AWG.write("SOURce1:VOLTage " + str(awg_volt)) 
AWG.write("SOURce2:VOLTage " + str(awg_volt))
time.sleep(5)
AWG.write("OUTPut1 ON")
AWG.write("OUTPut2 ON")
AWG.write("DISPlay:FOCus CH1")
