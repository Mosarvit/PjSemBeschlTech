# -*- coding: utf-8 -*-
import numpy as np
import math
import copy
#import FFT
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from compute import compute_K_from_a
from helpers import overlay
#import csv
#import os
#import time
#import FFT
#from scipy import interpolate
#import csv

def compute(Uin, in_pp, Uquest, N, verbosity):


    l_in=len(Uin)
    l_out = len(Uquest)
    #Signallängen anpassen und interpolieren
    x_in=np.linspace(1,l_out,l_in)
    x_out=np.linspace(1,l_out, l_out)
    f=interp1d(x_in, Uin)
    #g=interp1d(x_out, Uquest)
    Uin=f(x_out)
    #Uquest=g(x_out)
    #Signale übereinanderschieben -> über Kreuzkorrelation

    In, Uout = overlay.overlay(Uin, Uquest)

    #Normierung: u_out wird in V gemessen--> mV
    #u_in Normierung händisch anhand in_pp
    Uout=Uout*1000                                          #STIMMT DAS IMMER?
    In=(in_pp)/(max(In)-min(In))*In*1000                    #Wo kommt der Faktor 1000 her??



    #%Spannungsmatrix erzeugen
    print("Spannungsmatrix")
    U=np.zeros((l_out,N))
    for ind in [1,2,3]:
        U[:,(ind-1)] = [np.power(x,ind) for x in In]

    print("LGS lösen")
    a=np.linalg.lstsq(U,np.transpose(Uout),rcond=None)
    lsg=a[0]
    print(lsg)
    if verbosity:
        compute_K_from_a.compute(lsg, True)
        plt.figure
        plt.plot(In)
        plt.plot(Uout)
        #plt.title('Spannungssignale')
        #plt.ylabel('u in mV')
        #plt.legend('U_in', 'H^-1*U_out')
        plt.show()
    
    return (lsg)


# def overlay(Uin, Uquest):
#     l_out = len(Uquest)
#     print("Kreuzkorrelation")
#     xc = np.correlate(Uin, Uquest, 'full')
#     print("Kreuzkorrelation fertig")
#     shift = np.where(xc == max(xc))
#     shift = int(math.floor(shift[0]))
#     if shift >= np.size(Uquest):
#         shift = np.size(Uquest) - shift
#     if shift >= 0:
#
#         Uout = copy.copy(Uquest)
#         In = copy.copy(Uout)
#         In[0:l_out - shift] = Uin[shift:]
#         In[l_out - shift:] = Uin[0:shift]
#     else:
#         Uout = copy.copy(Uquest)
#         In = copy.copy(Uout)
#         In[l_out + shift:] = Uin[:-shift]
#         In[:l_out + shift] = Uin[-shift:]
#
#     return In, Uout