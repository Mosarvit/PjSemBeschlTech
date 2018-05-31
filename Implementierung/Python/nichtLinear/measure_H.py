import get_H
import numpy as np

def measure():
    fmax = 1000
    vpp = 100
    f, Ha, Hph = get_H.get(fmax, vpp)
    H = np.zeros((len(f), 3));
    H[:,0] = f
    H[:,1] = Ha
    H[:,2] = Hph

    return H