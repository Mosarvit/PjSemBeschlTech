# -*- coding: utf-8 -*-
import numpy as np
#import FFT
from helpers import overlay
#import csv
#import os
#import time
#import FFT
#from scipy import interpolate
#import csv

def compute(Uin,  Uquest, N, verbosity):

    """
    compute_a_from_Uin_Uquest berechten die Vorfaktoren a aus gegebenen Uin und Uquest

    INPUT:

        Uquest - n1x2 array; U_? (n1 - Länge des Signals)
            Uquest[:,0] - Zeitvektor
            Uquest[:,1] - Signalvektor

        Uin - n2x2 array; Eingangsspannung (n2 - Länge des Signals)
            Uin[:,0] - Zeitvektor
            Uin[:,1] - Signalvektor

        N - positiver integer; Polynomgrad der Approximierugnsmatrix

        verbosity - boolean, ob Uin gelplottet werden soll

    OUTPUT:

        a - Nx1 vektor; die Vorfaktoren

    """

    l_out = len(Uquest)

    np.sin(Uin)
    _, Uin = overlay.overlay(Uin, Uquest)
    Uin = Uin[:,1]

    #Normierung: u_out wird in V gemessen--> mV
    #u_in Normierung händisch anhand in_pp
    Uquest=Uquest[:,1]                                         #STIMMT DAS IMMER?
    # Uin = (Uin_pp) / (max(Uin) - min(Uin)) * Uin * 1000                    #Wo kommt der Faktor 1000 her??



    #%Spannungsmatrix erzeugen
    print("Spannungsmatrix")
    U=np.zeros((l_out,N))
    for ind in range(1,N+1):#[1,2,3]:
        U[:,(ind-1)] = [np.power(x,ind) for x in Uin]

    # print("LGS lösen")
    a=np.linalg.lstsq(U,np.transpose(Uquest),rcond=-1)
    lsg=a[0]
    # print(lsg)

    return (lsg)
