from get import get_H
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt

def measure(loadCSV, verbosity):

    if loadCSV :
        Ha = genfromtxt('data/current_data/H_a.csv', delimiter=',')
        Hph = genfromtxt('data/current_data/H_p.csv', delimiter=',')[:,1]
        f = Ha[:,0]
        Ha = Ha[:,1]
    else :
        fmax = 80e6
        vpp = 40e-3
        f, Ha, Hph = get_H.get(fmax, vpp)

    # assemble H

    H = np.zeros((len(f), 3));
    H[:,0] = f
    H[:,1] = Ha
    H[:,2] = Hph

    if verbosity:
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.plot(f, Ha)
        plt.title('Uebetragungsfunktion H - Amplitude')
        plt.ylabel('a')

        plt.subplot(2, 2, 2)
        plt.plot(f, Hph)
        plt.title('Uebetragungsfunktion H - phase')
        plt.ylabel('phi')

        plt.show()

    return H