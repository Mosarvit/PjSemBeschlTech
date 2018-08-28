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
import settings

def apply_transfer_function(Uout, H):

    f_rep = settings.f_rep
    freq = H.f

    fn = Uout.sample_rate / 2

    df = Uout.f_rep

    f_max = min(max(H.f), fn)
    f_min = max(min(H.f), df)

    ind_Y_min = int(np.ceil((f_min) / df))
    f_min = ind_Y_min * df

    ind_w_max = int(np.floor((f_max - f_min) / df)) + 1
    f_max = ind_w_max * df
    # x = int(np.floor(f_max / f_rep))

    w = np.linspace(f_min, f_max, ind_w_max)


    version = 1

    if version == 1 :

        t = Uout.time


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

    elif version == 2 :

        from helpers.plot_helper import plot_2_transfer_functions
        from helpers.plot_helper import plot_vector, plot_transfer_function, plot_2_signals

        Uout_vector = Uout.in_V
        # Fns = 1 / (Uout.time[1] - Uout.time[0])
        #
        # # -------- get FFT
        n = Uout_vector.size
        Uout_fft = np.fft.fft(Uout_vector)
        #

        int_Hc = interp1d(H.f, H.c)
        Hc = int_Hc(w)

        faktor = n / (ind_w_max * 2 + 1)

        Uout_fft_first_half = Uout_fft[1:ind_w_max+1]
        Uout_fft_0 = Uout_fft[0]

        Uquest_fft_0 = Uout_fft_0
        Uquest_fft_first_half = Uout_fft_first_half * Hc
        Uquest_fft_second_half = np.fliplr([np.conj(Uquest_fft_first_half)])[0]

        Uquest_fft = np.concatenate(([Uquest_fft_0], Uquest_fft_first_half, Uquest_fft_second_half), axis=0)

        Uquest_vector = np.fft.ifft(Uquest_fft) / faktor

        Uquest_obj = signal_class.gen_signal_from_f_rep(Uquest_vector, Uout.f_rep)

        return Uquest_obj