# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 17:11:40 2017

@author: denys
"""
import csv
import computea as param
import numpy as np
import NL_vorverzerrung
import computeU_quest_fromAnySignal
import computeU_quest_fromBBsignal

blub1 = open("UinL.csv", "r")
reader1 = csv.reader(blub1, delimiter = ';')
#for row in reader1:
Lneu1 = []
Lneu1.extend(reader1)
    
Hampl = []
freqA =[]
for i in range (0,len(Lneu1)):
    Hampl.append(Lneu1[i][1])
        
        
blub2 = open("320.csv", "r")
reader2 = csv.reader(blub2, delimiter = ';')
#for row in reader2:
Lneu2 = []
Lneu2.extend(reader2)
            
Hphase = []
freqP =[]
for i in range (0,len(Lneu2)):
    Hphase.append(Lneu2[i][0])

#eingelesene Signale mit der gerechnet werden kann
u_in = [float(i) for i in Hampl]
u_out1 = [float(i) for i in Hphase]
u_out=np.zeros(12500)
u_out = [float(i) for i in u_out]

ind5=0
for i in range (12500,25000):
    u_out[ind5]=u_out1[i]
    ind5=ind5+1

blub3 = open("Uefkt_exp155b.csv", "r")
reader3 = csv.reader(blub3, delimiter = ',')
for row in reader3:
    Lneu3 = []
    Lneu3.extend(reader3)
        
Hampl = []
freqA =[]
Hphase=[]
for i in range (0,len(Lneu3)):
    Hphase.append(Lneu3[i][2])
    Hampl.append(Lneu3[i][1])
    freqA.append(Lneu3[i][0])
            
Ampl = [float(i) for i in Hampl]
PhaseH = [float(i) for i in Hphase]
freq = [float(i) for i in freqA]

Phase=np.asarray(PhaseH)#/180*2*np.pi



#Phase bereinigen, Phasensprung korrigieren
PhaseVGL = np.asarray(PhaseH)#/180*2*np.pi
for ind in range (0,(len(Phase)-1)):
    if PhaseVGL[ind]*PhaseVGL[ind+1]<0:
        if PhaseVGL[ind]>np.pi/2 and PhaseVGL[ind+1]<-np.pi/2:
            Phase[ind+1:]=Phase[ind+1:]+2*np.pi
        elif PhaseVGL[ind]<-np.pi/2 and PhaseVGL[ind+1]>np.pi/2:
            Phase[ind+1:]=Phase[ind+1:]-2*np.pi
        

signal= computeU_quest_fromBBsignal.compute(900e3, 5e6, 80e6, 1e9, freq, Ampl, Phase)
u_in=signal[1]
    
u_mid = computeU_quest_fromAnySignal.compute(u_out, Ampl, Phase, freq)

[ a, K ] = param.compute(u_in, 320, u_mid, 3)

t=np.linspace(1,0.1/900000*1000000,len(u_in))
u=np.array(u_in)
U=np.column_stack((t,u))
U_nl = NL_vorverzerrung.NL_vorverzerrung(U, 40e-3, K)



