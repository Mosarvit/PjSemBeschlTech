import numpy as np
from scipy.interpolate import interp1d

def setVpp(signal, Vpp):
    signal[:, 1] = Vpp / (max(signal[:, 1]) - min(signal[:, 1])) * signal[:, 1]
    return signal

def convert_V_to_mV(signal):
    signal[:, 1] = signal[:, 1]*1000;
    return signal

def setSampleRate(Uin, sampleRate):
    T = max(Uin[:, 0]) - min(Uin[:, 0])
    lenght_new = int(np.floor(T * sampleRate))
    indices_old = np.arange(0, Uin.shape[0])
    indices_new = np.linspace(0, Uin.shape[0] - 1, num=lenght_new)
    interpolator1 = interp1d(indices_old, np.transpose(Uin))
    Uin = np.transpose(interpolator1(indices_new))
    return Uin