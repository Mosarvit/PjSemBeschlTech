import numpy as np
import math
import copy
from scipy.interpolate import interp1d


def overlay(Uin, Uout):

    l_in = Uin.shape[0]
    l_out = Uout.shape[0]
    # Signallängen anpassen und interpolieren
    x_in = np.linspace(1, l_out, l_in)
    x_out = np.linspace(1, l_out, l_out)
    f = interp1d(x_in, Uin[:,1])
    # g=interp1d(x_out, Uquest)
    Uin = f(x_out)
    # Uquest=g(x_out)
    # Signale übereinanderschieben -> über Kreuzkorrelation

    l_out = len(Uout)
    # print("Kreuzkorrelation")
    Uout = Uout[:,1]
    xc = np.correlate(Uin, Uout, 'full')




    # print("Kreuzkorrelation fertig")
    shift = np.asarray(np.where(xc == max(xc)))
    shift = int(math.floor(shift[0,0]))

    if shift >= np.size(Uout):
        shift = np.size(Uout) - shift



    In = copy.copy(Uout)

    if shift > 0:

        In[0:l_out - shift - 1] = Uin[shift+1:]
        In[l_out - shift - 1:] = Uin[0:shift+1]
    else:

        In[l_out + shift - 1:] = Uin[:-shift+1]
        In[:l_out + shift-1] = Uin[-shift+1:]

    return In