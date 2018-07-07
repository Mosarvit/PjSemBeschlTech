import numpy as np
import math
import copy
from scipy.interpolate import interp1d
from classes.signal_class import signal_class


def overlay(U1, U2):

    """
     overlay verschiebt Uin so, dass es maximal auf U2 aufliegt

     INPUT:

         U1 - n1x2 array; U_? (n1 - Länge des Signals)
             U1[:,0] - Zeitvektor
             U1[:,1] - Signalvektor

         U2 - n2x2 array; (n2 - Länge des Signals)
             U2[:,0] - Zeitvektor
             U2[:,1] - Signalvektor

     OUTPUT:

         U1_shifted_n1 - n1x2 array; das verschoben U1 (n1 - Länge des Signals U1)
             U1_shifted_n1[:,0] - Zeitvektor
             U1_shifted_n1[:,1] - Signalvektor

         U1_shifted_n2 - n2x2 array; das verschoben U1 der Länge m (n2 - Länge des Signals U2)
             U1_shifted_n2[:,0] - Zeitvektor
             U1_shifted_n2[:,1] - Signalvektor

     """

    # U1 = U1.get_signal_in_V_old_convention()
    # U2 = U2.get_signal_in_V_old_convention()
    #
    # ###########
    #
    # l_in = U1.shape[0]
    # l_out = U2.shape[0]
    # # Signallängen anpassen und interpolieren
    # x_in = np.linspace(1, l_out, l_in)
    # x_out = np.linspace(1, l_out, l_out)
    # f = interp1d(x_in, U1[:, 1])
    # # g=interp1d(x_out, Uquest)
    #
    # # Uquest=g(x_out)
    # # Signale übereinanderschieben -> über Kreuzkorrelation


    # print("Kreuzkorrelation")

    U1.t_end = U2.t_end
    U1.sample_rate = U2.sample_rate

    # U1 = U1.get_signal_in_V_old_convention()
    # U2 = U2.get_signal_in_V_old_convention()

    U1_vector = U1.in_V
    U2_signal = U2.in_V


    # U2_signal = U2[:, 1]

    l_out = len(U2_signal)

    xc = np.correlate(U1_vector, U2_signal, 'full')




    # print("Kreuzkorrelation fertig")
    shift = np.asarray(np.where(xc == max(xc)))
    shift = int(math.floor(shift[0,0]))

    if shift >= np.size(U2_signal):
        shift = np.size(U2_signal) - shift



    U1_shifted_tmp = copy.copy(U2_signal)

    if shift > 0:

        U1_shifted_tmp[0:l_out - shift - 1] = U1_vector[shift + 1:]
        U1_shifted_tmp[l_out - shift - 1:] = U1_vector[0:shift + 1]
    else:

        U1_shifted_tmp[l_out + shift - 1:] = U1_vector[:-shift + 1]
        U1_shifted_tmp[:l_out + shift-1] = U1_vector[-shift + 1:]

    # f2 = interp1d(x_out, U1_shifted_tmp)
    # g=interp1d(x_out, Uquest)
    # U1_shifted_n1 = copy.copy(U1)
    # U1_shifted_n1[:,1] = f2(x_in)

    # U1_shifted_n2 = copy.copy(U2)
    # U1_shifted_n2[:, 1] = U1_shifted_tmp

    #######

    U1_shifted = signal_class(U1_shifted_tmp, U2.sample_rate)


    return U1_shifted