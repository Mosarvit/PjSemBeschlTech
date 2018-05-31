import numpy as np
import math
import copy


def overlay(Uin, Uquest):
    l_out = len(Uquest)
    print("Kreuzkorrelation")
    xc = np.correlate(Uin, Uquest, 'full')
    print("Kreuzkorrelation fertig")
    shift = np.where(xc == max(xc))
    shift = int(math.floor(shift[0]))
    if shift >= np.size(Uquest):
        shift = np.size(Uquest) - shift
    if shift >= 0:

        Uout = copy.copy(Uquest)
        In = copy.copy(Uout)
        In[0:l_out - shift] = Uin[shift:]
        In[l_out - shift:] = Uin[0:shift]
    else:
        Uout = copy.copy(Uquest)
        In = copy.copy(Uout)
        In[l_out + shift:] = Uin[:-shift]
        In[:l_out + shift] = Uin[-shift:]

    return In, Uout