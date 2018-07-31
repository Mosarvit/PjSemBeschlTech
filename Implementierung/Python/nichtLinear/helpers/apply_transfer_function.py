# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017
@author: denys
"""

import math
import copy
#import time
import numpy as np
#from scipy import interpolate
from scipy.interpolate import interp1d
import warnings
from classes.signal_class import signal_class

def apply_transfer_function(Uout, H):

    """
    compute_Uquest_from_Uout berechten Uquest aus Uout mithilfe der Invertierung der Übetragungsfunktion H
    INPUT:
        Uout - nx2 array; Ausgangssignal (n - Länge des Signals)
            Uout[:,0] - Zeitvektor
            Uout[:,1] - Signalvektor
        H - nx3 array; Übertragungsfunktion (n - Anzahl der Frequenzen)
            H[:,0] - Frequenz f
            H[:,1] - Amplitudenverstärkung
            H[:,2] - Phasenverschiebung
        verbosity - boolean; ob Uin gelplottet werden soll
    OUTPUT:
        Uquest - nx2 array; U_? (n - Länge des Signals)
            Uquest[:,0] - Zeitvektor
            Uquest[:,1] - Signalvektor
    """



    f_rep=900e3

    # Ampl = [float(i) for i in Hampl]
    # Phase = [float(i) for i in Hphase]
    # freq = H[:, 0]
    freq = H.f

    fn = Uout.sample_rate / 2

    df = Uout.f_rep

    f_max = min( max(H.f), fn)
    f_min = max( min(H.f), df)

    ind_Y_min = int(np.ceil( ( f_min )  / df ) )
    f_min = ind_Y_min * df

    ind_w_max = int(np.floor((f_max - f_min) / df)) + 1
    f_max = ind_w_max * df
    # x = int(np.floor(f_max / f_rep))

    w=np.linspace(f_min, f_max, ind_w_max)

    t = Uout.time


#projizieren auf gleiche Achse
    # f = interp1d(freq, Phase)
    # arg = f(w)
    # int_H = interp1d(freq, H_)
    # H_neu = int_H(w)
    # Ha = abs(H_neu)

    ####################################################################################################################

    # int_Ha = interp1d(H[:, 0], H[:, 1])
    # Ha = int_Ha(w)

    # Hph = np.angle(H_neu)

    # int_Hph = interp1d(H[:, 0], H[:, 2])
    # Hph1 = int_Hph(w)

    int_Ha = interp1d(H.f, H.a)
    Ha = int_Ha(w)
    #
    # # Hph = np.angle(H_neu)
    #
    int_Hph = interp1d(H.f, H.p)
    Hph = int_Hph(w)


    u=copy.copy(Uout.in_V)
#fft
    L=len(u)
    NFFT = L




    ufft = np.fft.fft(u, NFFT)
    Y =  ufft / L


    Uquest = np.zeros([L, 2])
    Uquest[:,0] =  Uout.time

    for k in range(len(w) - 1):

        rnd = 11  # round by , since fft is only this precise and would otherwise leave a negligable imaginary part which would throw a warning

        k_shifted = ind_Y_min + k - 1

        a_n = round(Y[k_shifted + 1], rnd) + round(Y[len(Y) - 1 - k_shifted], rnd)
        b_n = 1j * (round(Y[k_shifted + 1], rnd) - round(Y[len(Y) - 1 - k_shifted], rnd))

        omegat = 2 * math.pi * ((k_shifted + 1) * df) * t
        gamma = Hph[k] * np.ones(len(t))
        phi = omegat + gamma

        c_ = 1 * abs(Ha[k]) * (a_n * np.cos(phi) + b_n * np.sin(phi))

        if any(c_.imag != 0.0):
            warnings.warn("c is not purely real")

        c = c_.real

        Uquest[:, 1] = Uquest[:, 1] + c

    Uquest_obj = signal_class( Uout.time, Uquest[:,1] )

    return Uquest_obj