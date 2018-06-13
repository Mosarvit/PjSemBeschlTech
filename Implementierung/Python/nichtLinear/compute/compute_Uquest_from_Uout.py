# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
def compute(Uout, H, verbosity):
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
    freq = H[:, 0]


    f_max=math.floor(max(freq)/f_rep)*f_rep
    w=np.linspace(f_rep, f_max, int(np.floor(f_max/f_rep)))

    dt=1/f_rep/Uout.shape[0]
    t=np.linspace(0, 1/f_rep, round(1/f_rep/dt))


#projizieren auf gleiche Achse
    # f = interp1d(freq, Phase)
    # arg = f(w)
    # int_H = interp1d(freq, H_)
    # H_neu = int_H(w)
    # Ha = abs(H_neu)

    int_Ha = interp1d(H[:, 0], H[:, 1])
    Ha = int_Ha(w)

    # Hph = np.angle(H_neu)

    int_Hph = interp1d(H[:, 0], H[:, 2])
    Hph = int_Hph(w)

    u=copy.copy(Uout[:,1])
#fft
    L=len(u)
    NFFT = L
    ufft = np.fft.fft(u, NFFT)
    Y = 2 * ufft / L

    Uin = np.zeros([L, 2])
    Uin[:,0] = Uout[:,0]

    for k in range(int(math.floor(f_max / f_rep))):

        a_n = Y[k + 1] + Y[len(Y) - 1 - k]
        b_n = 1j * (Y[k + 1] - Y[len(Y) - 1 - k])

        omegat = 2 * math.pi * (k+1) * f_rep * t
        gamma =  Hph[k] * np.ones(len(t))
        phi = omegat - gamma

        c = 1 / abs(Ha[k]) * ( a_n *np.cos(phi) + b_n * np.sin(phi) )

        Uin[:,1] = Uin[:,1] + c


    if verbosity:
        plt.figure()
        plt.plot(Uin[:,0],Uin[:,1])
        plt.title('Uquest')
        # plt.grid(True)
        plt.ylabel('u')
        plt.xlabel('t')
        plt.show()

    return (Uin)