import get_H
import numpy as np
import matplotlib.pyplot as plt

def measure(loadCSV, verbosity):

    if loadCSV :
        Ha = genfromtxt('data/currentdata/H_a.csv', delimiter=',')
        Hph = genfromtxt('data/currentdata/H_p.csv', delimiter=',')[:,1]
        f = Ha[:,0]
        Ha = Ha[:,1]
    else :
        fmax = 1000
        vpp = 100
        f, Ha, Hph = get_H.get(fmax, vpp)
        H = np.zeros((len(f), 3));

    # assemble H
    
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