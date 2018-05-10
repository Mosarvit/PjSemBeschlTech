# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 09:46:20 2017

@author: denys
"""
def computeParam( u_in, in_pp, u_out, N ):
    import numpy as np
    import math
    import copy
    #import FFT
    import matplotlib.pyplot as plt
    from scipy.interpolate import interp1d
    import computeK
    #import csv
    #import os
    #import time
    #import FFT
    #from scipy import interpolate
    #import csv
 
    l_in=len(u_in)
    l_out=len(u_out)
    #Signallängen anpassen und interpolieren
    x_in=np.linspace(1,l_out,l_in)
    x_out=np.linspace(1,l_out, l_out)
    f=interp1d(x_in, u_in)
    g=interp1d(x_out,u_out)
    u_in=f(x_out)
    u_out=g(x_out)
    #Signale übereinanderschieben -> über Kreuzkorrelation
    print("Kreuzkorrelation")
    xc=np.correlate(u_in, u_out,'full')
    print("Kreuzkorrelation fertig")
    shift=np.where(xc==max(xc))
    shift=math.floor(shift[0])
    if shift >= 0:
        if shift >= np.size(u_out):
            shift = shift - np.size(u_out)
        uout=copy.copy(u_out)
        uin=copy.copy(uout)
        uin[0:l_out-shift]=u_in[shift:]
        uin[l_out-shift:]=u_in[0:shift]
        
    #Normierung: u_out wird in V gemessen--> mV
    #u_in Normierung händisch anhand in_pp
    uout=1000*uout                                          #STIMMT DAS IMMER?
    uin=(in_pp*uin)/(max(uin)-min(uin))

    #%Spannungsmatrix erzeugen
    print("Spannungsmatrix")
    U=np.zeros((l_out,N))
    for ind in range(0,N):
        U[:,ind] = uin**(ind+1)
    print("LGS lösen")
    a=np.linalg.lstsq(U,np.transpose(uout))
    lsg=a[0]
    #Kennlinie erstellen
    K=computeK.compute(lsg, 1)
    
    plt.figure
    plt.plot(uin)
    plt.plot(uout)
    plt.title('Spannungssignale')
    plt.ylabel('u in mV')
    plt.legend('U_in', 'H^-1*U_out')
    plt.show()
    
    plt.figure
    plt.plot(K[:,0],K[:,1])
    plt.title('Kennlinie')
    plt.xlabel('U_in in mV')
    plt.ylabel('U_out in mV')
    plt.show()
    
    return (lsg, K)