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
from helpers.find_nearest import find_nearest



def apply_transfer_function(Uout, H):
    from helpers.plot_helper import plot_2_transfer_functions
    from helpers.plot_helper import plot_vector, plot_transfer_function, plot_2_signals


    Uout_vector = Uout.in_V
    Fns = 1 / (Uout.time[1] - Uout.time[0])

    # -------- get FFT
    n = Uout_vector.size
    Uout_fft = np.fft.fft(Uout_vector)


    fn = Fns/2
    df = max(Fns/n, min(H.f))


    f_H_max = max(H.f)
    f_max = min(f_H_max, fn)
    ind_max = int(np.floor(f_max / df))
    f_U_max = ind_max * df

    frq = np.arange(0, f_U_max, df)

    Hw = frq[1:]

    int_Hc = interp1d(H.f, H.c)
    Hc = int_Hc(Hw)

    faktor = n / ( ind_max * 2 + 1 )


    Uout_fft_first_half = Uout_fft[1:ind_max]
    Uout_fft_0 = Uout_fft[0]

    Uquest_fft_0 = Uout_fft_0
    Uquest_fft_first_half = Uout_fft_first_half * Hc
    Uquest_fft_second_half = np.fliplr([np.conj(Uquest_fft_first_half)])[0]


    Uquest_fft = np.concatenate(([Uquest_fft_0], Uquest_fft_first_half, Uquest_fft_second_half), axis = 0)

    Uquest_vector = np.fft.ifft(Uquest_fft) / faktor


    Uquest_obj = signal_class.gen_signal_from_f_rep(Uquest_vector, Uout.f_rep)


    return Uquest_obj