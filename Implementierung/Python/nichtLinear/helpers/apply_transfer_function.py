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
from classes.transfer_function_class import transfer_function_class
from helpers import FFT


def apply_transfer_function(Uout, H):
    from helpers.plot_helper import plot_2_transfer_functions
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


    f_max=math.floor(max(freq)/f_rep)*f_rep
    w=np.linspace(f_rep, f_max, int(np.floor(f_max/f_rep)))

    dt=1/f_rep/len(Uout.time) # Uout_old.shape[0]
    t=np.linspace(0, 1/f_rep, round(1/f_rep/dt))


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

    for k in range(int(math.floor(f_max / f_rep))):

        rnd = 11 # round by , since fft is only this precise and would otherwise leave a negligable imaginary part which would throw a warning

        a_n = round(Y[k + 1], rnd) + round(Y[len(Y) - 1 - k], rnd)
        b_n = 1j * (round(Y[k + 1], rnd) - round(Y[len(Y) - 1 - k], rnd))

        omegat = 2 * math.pi * (k+1) * f_rep * t
        gamma =  Hph[k] * np.ones(len(t))
        phi = omegat + gamma

        c_ = 1 * abs(Ha[k]) * ( a_n *np.cos(phi) + b_n * np.sin(phi) )

        if any(c_.imag!= 0.0):
            warnings.warn("c is not purely real")

        c = c_.real

        Uquest[:,1] = Uquest[:,1] + c

    Uquest_obj = signal_class( Uout.time, Uquest[:,1] )

    #######################################################

    [frq, UoutAmpl, Phase, _] = FFT.get(Uout.in_V, 1 / (Uout.time[-1] - Uout.time[-2]))

    PhaseH = np.asarray([float(i) for i in Phase])
    PhaseVGL = [float(i) for i in Phase]


    for ind in range(0, (len(Phase) - 1)):
        if PhaseVGL[ind] * PhaseVGL[ind + 1] < 0:
            if PhaseVGL[ind] > np.pi / 2 and PhaseVGL[ind + 1] < -np.pi / 2:
                PhaseH[ind + 1:] = PhaseH[ind + 1:] + 2 * np.pi
            elif PhaseVGL[ind] < -np.pi / 2 and PhaseVGL[ind + 1] > np.pi / 2:
                PhaseH[ind + 1:] = PhaseH[ind + 1:] - 2 * np.pi

    

    UoutAmpl = UoutAmpl[1:w+1]
    frq = frq[1:w+1]
    UquestAmpl = UoutAmpl/H.a


    [frq, UoutAmpl, PhaseUout, _] = FFT.get(Uout.in_V, 1 / (Uout.time[-1] - Uout.time[-2]))

    # Uquest_freq = transfer_function_class(frq)
    # Uquest_freq.a = UquestAmpl

    Ha_computed = UoutAmpl / UquestAmpl
    H_computed = transfer_function_class(frq[1:88])
    H_computed.a = Ha_computed[1:88]

    plot_2_transfer_functions(H1=H, H2=H_computed, legend1='H',legend2='H_computed')



    return Uquest_obj