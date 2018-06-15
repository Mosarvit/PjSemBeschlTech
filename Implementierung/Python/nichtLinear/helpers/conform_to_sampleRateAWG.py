import numpy as np
from scipy.interpolate import interp1d

def conform(Uin, sampleRateAWG):
    T = max(Uin[:, 0]) - min(Uin[:, 0])
    lenght_new = int(np.floor(T * sampleRateAWG))
    indices_old = np.arange(0, Uin.shape[0])
    indices_new = np.linspace(0, Uin.shape[0] - 1, num=lenght_new, endpoint=True)
    interpolator1 = interp1d(indices_old, np.transpose(Uin))
    Uin = np.transpose(interpolator1(indices_new))
    return Uin