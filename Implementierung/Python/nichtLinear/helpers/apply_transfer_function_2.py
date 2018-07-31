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
    # freq = H.f

    # f_max=math.floor(max(freq)/f_rep)*f_rep
    #
    # wn = int(np.floor(f_max/f_rep))
    # w=np.linspace(f_rep, f_max, wn)



    # dt=1/f_rep/len(Uout.time) # Uout_old.shape[0]
    # t=np.linspace(0, 1/f_rep, round(1/f_rep/dt))


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
    #
    # int_Ha = interp1d(H.f, H.a)
    # Ha = int_Ha(w)
    # #
    # # # Hph = np.angle(H_neu)
    # #
    # int_Hph = interp1d(H.f, H.p)
    # Hph = int_Hph(w)






#     u=copy.copy(Uout.in_V)
# #fft
#     L=len(u)
#     NFFT = L
#
#
#
#
#     ufft = np.fft.fft(u, NFFT)
#     Y =  ufft / L
#
#
#     Uquest = np.zeros([L, 2])
#     Uquest[:,0] =  Uout.time

    # for k in range(int(math.floor(f_max / f_rep))):
    #
    #     rnd = 11 # round by , since fft is only this precise and would otherwise leave a negligable imaginary part which would throw a warning
    #
    #     a_n = round(Y[k + 1], rnd) + round(Y[len(Y) - 1 - k], rnd)
    #     b_n = 1j * (round(Y[k + 1], rnd) - round(Y[len(Y) - 1 - k], rnd))
    #
    #     omegat = 2 * math.pi * (k+1) * f_rep * t
    #     gamma =  Hph[k] * np.ones(len(t))
    #     phi = omegat + gamma
    #
    #     c_ = 1 * abs(Ha[k]) * ( a_n *np.cos(phi) + b_n * np.sin(phi) )
    #
    #     if any(c_.imag!= 0.0):
    #         warnings.warn("c is not purely real")
    #
    #     c = c_.real
    #
    #     Uquest[:,1] = Uquest[:,1] + c

    # Uquest_obj1 = signal_class( Uout.time, Uquest[:,1] )

    #######################################################

    # [frq, UoutAmpl, Phase, _] = FFT.get(Uout.in_V, 1 / (Uout.time[-1] - Uout.time[-2]))

    # [frq, UoutAmpl, Phase, Uout_fft2] = FFT.get(Uout.in_V, 1 / (Uout.time[-1] - Uout.time[-2]))

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



    # ind_half = int(np.floor(n/2))

    # Uout_fft_0 = Uout_fft[0]
    # Uout_fft_first_half = Uout_fft[1:ind_half+1]
    # Uout_fft_second_half = np.fliplr([np.conj(Uout_fft_first_half)])[0]    #
    # Uout_fft_back = np.concatenate(([Uout_fft_0], Uout_fft_first_half, Uout_fft_second_half), axis=0)    #
    # Uout_fftifft = np.fft.ifft(Uout_fft_back) / faktor
    # plot_vector(Uout_fftifft)
    # plot_vector(Uout_vector)

    Uout_fft_first_half = Uout_fft[1:ind_max]
    Uout_fft_0 = Uout_fft[0]

    Uquest_fft_0 = Uout_fft_0
    Uquest_fft_first_half = Uout_fft_first_half * Hc
    Uquest_fft_second_half = np.fliplr([np.conj(Uquest_fft_first_half)])[0]



    Uquest_fft = np.concatenate(([Uquest_fft_0], Uquest_fft_first_half, Uquest_fft_second_half), axis = 0)

    Uout_fftifft = np.fft.ifft(Uout_fft) * faktor
    Uquest_vector = np.fft.ifft(Uquest_fft) / faktor

    # plot_vector(Uout_vector)
    # plot_vector(Uout_fftifft)

    # plot_vector(Uout_vector)
    # plot_vector(Uout_fftifft, integ=1)
    # plot_vector(Uquest_vector, integ=1)
    # plot_vector(Uquest_obj.in_V, integ=2)

    Uquest_obj = signal_class.gen_signal_from_f_rep(Uquest_vector, Uout.f_rep)

    # plot_2_signals(Uout, Uquest_obj)

    # plot_2_signals(Uquest_obj, Uquest_obj1, legend1='Uquest_obj', legend2='Uquest_obj1')


    # PhaseH = np.asarray([float(i) for i in Phase])
    # PhaseVGL = [float(i) for i in Phase]
    #
    #
    # for ind in range(0, (len(Phase) - 1)):
    #     if PhaseVGL[ind] * PhaseVGL[ind + 1] < 0:
    #         if PhaseVGL[ind] > np.pi / 2 and PhaseVGL[ind + 1] < -np.pi / 2:
    #             PhaseH[ind + 1:] = PhaseH[ind + 1:] + 2 * np.pi
    #         elif PhaseVGL[ind] < -np.pi / 2 and PhaseVGL[ind + 1] > np.pi / 2:
    #             PhaseH[ind + 1:] = PhaseH[ind + 1:] - 2 * np.pi
    #
    #
    #
    # UoutAmpl = UoutAmpl[1:w+1]
    # frq = frq[1:w+1]
    # UquestAmpl = UoutAmpl/H.a
    #
    #
    # [frq, UoutAmpl, PhaseUout, _] = FFT.get(Uout.in_V, 1 / (Uout.time[-1] - Uout.time[-2]))
    #
    # # Uquest_freq = transfer_function_class(frq)
    # # Uquest_freq.a = UquestAmpl
    #
    # Ha_computed = UoutAmpl / UquestAmpl
    # H_computed = transfer_function_class(frq[1:88])
    # H_computed.a = Ha_computed[1:88]
    #
    # plot_2_transfer_functions(H1=H, H2=H_computed, legend1='H',legend2='H_computed')

    # [frq, UoutAmpl, Phase, Uquest_fft] = FFT.get(Uout.in_V, 1 / (Uout.time[-1] - Uout.time[-2]))
    # [frq, UquestAmpl, Phase, Uquest_fft] = FFT.get(Uquest_obj.in_V, 1 / (Uquest_obj.time[-1] - Uquest_obj.time[-2]))
    #
    # Ha = UoutAmpl[:88] / UquestAmpl
    # H2 = transfer_function_class(frq[1:])
    # H2.a = Ha
    #
    # plot_2_transfer_functions(H1=H, H2=H2, legend1='H', legend2='H2')


    return Uquest_obj