# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 09:07:31 2017
%   Berechnet das Eingangszeitsignal für ein System mit 
%   der Übertragungsfunktion H
%   der Wiederholfrequenz f_rep
%   der Barrier_Bucket Frequenz f_bb
%   der Grenzfrequenz f_g
%   auf Basis des Matlab Skripts von Jens Harzheim
@author: Denys Bast
"""
def compute(f_rep, f_bb, f_g, Samplingrate, frq, H, PhaseH):
    

    
    #import MLBS
    import math
    import csv
    import time
    #import time
    #import matplotlib.pyplot as plt
    import numpy as np
    import os
    #import FFT
   # from scipy import interpolate
    from scipy.interpolate import interp1d
   # import csv
    directory = time.strftime("%d.%m.%Y_%H_%M_%S")
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory + "/Plots"):
        os.makedirs(directory + "/Plots")
    if not os.path.exists(directory + "/csv"):
        os.makedirs(directory + "/csv")
    

#Frequenzvektor mit Vielfachen der Wiederholfrequenz bis f_grenz=80MHz
    w = np.linspace(f_rep, math.floor(f_g/f_rep)*f_rep, math.floor(f_g/f_rep))
    
#t für 1 Perioden, 10 Abtastpunkte/Periode
    dt=1/Samplingrate
    t=np.linspace(0, 1/f_rep, round(1/f_rep/dt))
    
 #eingelesene Übertragungsfunktion mit der gerechnet werden kann
    Hampl=H
    Hphase=PhaseH
    freqA=frq
    
    #überprüfen ob das benötigt wird bei gemessener Übertragungsfunktion
    Ampl = [float(i) for i in Hampl]
    Phase = np.asarray([float(i) for i in Hphase])
    freq = [float(i) for i in freqA]
    
    """
    freqPlot = np.asarray(freq) * 1e-6
    
    plt.figure()
    plt.plot(freqPlot,Ampl)
    plt.grid(True)
    plt.ylabel(r'$AmplH$')
    plt.xlabel(r'$f$ in $MHz$')
    plt.show()
    
    plt.figure()
    plt.plot(freqPlot,Phase)
    plt.grid(True)
    plt.ylabel(r'$PhaseH$')
    plt.xlabel(r'$f$ in $MHz$')
    plt.show()
    """
#projizieren auf gleiche Achse
    f = interp1d(freq, Phase)
    #tck = interpolate.splrep(freq, Ampl, s=0)
    #H = interpolate.splev(w, tck, der=0)
    arg = f(w)
    g=interp1d(freq,Ampl)
    H=g(w)
    """    
    plt.figure()
    plt.plot(w,H)
    plt.grid(True)
    plt.ylabel(r'$AmplHinterpolate$')
    plt.xlabel(r'$f$ in $Hz$')
    plt.show()
    
    plt.figure()
    plt.plot(w,arg)
    plt.grid(True)
    plt.ylabel(r'$PhaseHinterpolate$')
    plt.xlabel(r'$f$ in $Hz$')
    plt.show()
    """    
    u_in = np.zeros(len(t))
    F = np.ones(len(w))
    P=F
    B=F
    U=u_in
    
    for ind in range (0,len(w)):
# b=Fourierkoeffizient
        b=-f_rep/f_bb*(np.sinc(((ind+1)*2*f_rep-2*f_bb)/f_bb/2)-np.sinc(((ind+1)*2*f_rep+2*f_bb)/f_bb/2))
        u_in=u_in+b/H[ind]*np.sin((ind+1)*2*np.pi*f_rep*t-np.ones(len(t))*arg[ind])
  
        
        F[ind]=b/H[ind]
        P[ind]=arg[ind]
        B[ind]=np.angle(b)
        U=U+b*np.sin(ind*2*np.pi*f_rep*t)
    """
    plt.figure()
    plt.plot(t,u_in)
    plt.grid(True)
    plt.ylabel(r'$Uin$')
    plt.xlabel(r'$t$ in $us$')
    plt.show()
    """
    with open(directory + '/csv/UinL.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0,u_in.size):
                writer.writerow([str(t[i]), str(u_in[i])])
    
    return (t, u_in)
    
