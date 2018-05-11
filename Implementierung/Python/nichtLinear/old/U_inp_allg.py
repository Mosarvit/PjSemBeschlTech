# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""

def U_inp_allg( u_out, Hampl, Hphase, freqA ):

    import math
    import copy
    import matplotlib.pyplot as plt
    #import time
    #import matplotlib.pyplot as plt
    import numpy as np
    import FFT
    #from scipy import interpolate
    from scipy.interpolate import interp1d

    f_rep=900e3
     
    Ampl = [float(i) for i in Hampl]
    Phase = [float(i) for i in Hphase]
    freq = [float(i) for i in freqA]


    f_max=math.floor(max(freq)/f_rep)*f_rep
    w=np.linspace(f_rep, f_max, f_max/f_rep)
                           
    dt=1/f_rep/len(u_out)
    t=np.linspace(0, 1/f_rep, round(1/f_rep/dt))


#projizieren auf gleiche Achse
    f = interp1d(freq, Phase)
    arg = f(w)
    g = interp1d(freq, Ampl)
    H = g(w)
    
    u=copy.copy(u_out)
#fft
    L=len(u)
    [frqfft, amplfft, phasefft, Hfft] = FFT.get(np.asarray(u), 900000)
    NFFT=L
    asdf=np.fft.fft(u,NFFT)
    Y=2*asdf/L
    u_in = np.zeros(len(t))
    u_inY= np.zeros(len(t))
    P=math.floor(f_max/f_rep)
    u_init=np.zeros(np.size(u_out))
    print("lineares zurückrechnen")
    for i in range (0,P):
        betrag=abs(Y[i+1])/H[i]
        fest=2*np.pi*f_rep*t*(i+1)
        variabel=np.ones(len(t))*(-arg[i]+np.angle(Y[i+1]))
        
        cosinus=np.cos(fest+variabel)
        u_init=u_init+betrag*cosinus


    for i in range (0,P):
        u_in=u_in+abs(Hfft[i+1])/H[i]*np.cos(2*np.pi*(i+1)*f_rep*t+np.ones(len(t))*(-arg[i]+np.angle(Hfft[i+1])))
        u_inY=u_inY+abs(Y[i+1])/H[i]*np.cos(2*np.pi*(i+1)*f_rep*t+np.ones(len(t))*(-arg[i]+np.angle(Y[i+1])))

             
    plt.figure()
    plt.plot(u_inY)
    plt.plot(u_in)
    plt.grid(True)
    plt.ylabel('u_in')
    plt.xlabel('punkte')
    plt.show()

    return (u_in)