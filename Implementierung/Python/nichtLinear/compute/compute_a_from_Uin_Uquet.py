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

def compute(Uin, Uin_pp, Uquest, N, verbosity):
    l_out = len(Uquest)


    Uin = overlay.overlay(Uin, Uquest)

    #Normierung: u_out wird in V gemessen--> mV
    #u_in Normierung händisch anhand in_pp
    Uquest=Uquest*1000                                          #STIMMT DAS IMMER?
    Uin= (Uin_pp) / (max(Uin) - min(Uin)) * Uin * 1000                    #Wo kommt der Faktor 1000 her??



    #%Spannungsmatrix erzeugen
    print("Spannungsmatrix")
    U=np.zeros((l_out,N))
    for ind in [1,2,3]:
        U[:,(ind-1)] = [np.power(x,ind) for x in Uin]

    print("LGS lösen")
    a=np.linalg.lstsq(U,np.transpose(Uquest),rcond=None)
    lsg=a[0]
    print(lsg)
    if verbosity:
        compute_K_from_a.compute(lsg, True)
        plt.figure
        plt.plot(Uin)
        plt.plot(Uquest)
        #plt.title('Spannungssignale')
        #plt.ylabel('u in mV')
        #plt.legend('U_in', 'H^-1*U_out')
        plt.show()
    
    return (lsg)
