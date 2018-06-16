import numpy as np
def find1(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx