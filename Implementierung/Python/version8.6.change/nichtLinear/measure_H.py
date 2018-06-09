import get_H
import numpy as np
import matplotlib.pyplot as plt

def measure(verbosity):
    fmax = 1000
    vpp = 100
    f, Ha, Hph = get_H.get(fmax, vpp)
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