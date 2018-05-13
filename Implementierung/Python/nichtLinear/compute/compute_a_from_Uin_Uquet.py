# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 09:46:20 2017

@author: denys
"""
def compute(Uin, in_pp, Uquest, N, verbosity):
    import numpy as np
    import math
    import copy
    #import FFT
    import matplotlib.pyplot as plt
    from scipy.interpolate import interp1d
    #import csv
    #import os
    #import time
    #import FFT
    #from scipy import interpolate
    #import csv
 
    l_in=len(Uin)
    l_out=len(Uquest)
    #Signallängen anpassen und interpolieren
    x_in=np.linspace(1,l_out,l_in)
    x_out=np.linspace(1,l_out, l_out)
    f=interp1d(x_in, Uin)
    g=interp1d(x_out, Uquest)
    Uin=f(x_out)
    Uquest=g(x_out)
    #Signale übereinanderschieben -> über Kreuzkorrelation
    print("Kreuzkorrelation")
    xc=np.correlate(Uin, Uquest, 'full')
    print("Kreuzkorrelation fertig")
    shift=np.where(xc==max(xc))
    shift=int(math.floor(shift[0]))
    if shift >= 0:
        if shift >= np.size(Uquest):
            shift = shift - np.size(Uquest)
        Uout=copy.copy(Uquest)
        Uin=copy.copy(Uout)
        Uin[0:l_out-shift]= Uin[shift:]
        Uin[l_out-shift:]= Uin[0:shift]
        
    #Normierung: u_out wird in V gemessen--> mV
    #u_in Normierung händisch anhand in_pp
    Uout=1000*Uout                                          #STIMMT DAS IMMER?
    Uin=(in_pp*Uin)/(max(Uin)-min(Uin))

    #%Spannungsmatrix erzeugen
    print("Spannungsmatrix")
    U=np.zeros((l_out,N))
    for ind in range(0,N):
        U[:,ind] = Uin**(ind+1)
    print("LGS lösen")
    a=np.linalg.lstsq(U,np.transpose(Uout))
    lsg=a[0]

    if verbosity:
        plt.figure
        plt.plot(Uin)
        plt.plot(Uout)
        plt.title('Spannungssignale')
        plt.ylabel('u in mV')
        plt.legend('U_in', 'H^-1*U_out')
        plt.show()
    
    return (lsg)