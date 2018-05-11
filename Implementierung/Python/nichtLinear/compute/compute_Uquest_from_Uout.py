# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
def compute(Uout, H_, freqA, verbosity):
    """

    :type Uout: object
    """
    import math
    import copy
    import matplotlib.pyplot as plt
    #import time
    #import matplotlib.pyplot as plt
    import numpy as np
    #from scipy import interpolate
    from scipy.interpolate import interp1d

    f_rep=900e3

    # Ampl = [float(i) for i in Hampl]
    # Phase = [float(i) for i in Hphase]
    freq = [float(i) for i in freqA]


    f_max=math.floor(max(freq)/f_rep)*f_rep
    w=np.linspace(f_rep, f_max, f_max/f_rep)

    dt=1/f_rep/len(Uout)
    t=np.linspace(0, 1/f_rep, round(1/f_rep/dt))


#projizieren auf gleiche Achse
    # f = interp1d(freq, Phase)
    # arg = f(w)
    int_H = interp1d(freq, H_)
    H_neu = int_H(w)
    H = abs(H_neu)
    arg = np.angle(H_neu)

    u=copy.copy(Uout)
#fft
    L=len(u)
    NFFT = L
    ufft = np.fft.fft(u, NFFT)
    Y = 2 * ufft / L

    u_in = np.zeros(L)

    for k in range (int(math.floor(f_max/f_rep))):

        a_n = Y[k + 1] + Y[len(Y) - 1 - k]
        b_n = 1j * (Y[k + 1] - Y[len(Y) - 1 - k])

        omegat = 2 * math.pi * (k+1) * f_rep * t
        gamma =  arg[k] * np.ones(len(t))
        phi = omegat - gamma

        c = 1 / abs(H[k]) * ( a_n *np.cos(phi) + b_n * np.sin(phi) )

        u_in = u_in + c


    if verbosity:
        plt.figure()
        plt.plot(u_in)
        plt.grid(True)
        plt.ylabel('u_in')
        plt.xlabel('punkte')
        plt.show()

    return (u_in)