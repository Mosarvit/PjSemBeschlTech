import numpy as np
import math
import copy
from scipy.interpolate import interp1d
from classes.signal_class import signal_class
from scipy import linalg


def overlay(U1obj, U2obj):

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


######### this is obviously a crutch, but this iliminates the cases, when U1 and U2 dont have the same t_end, which normally should not , since frequency1 == frequency2
    # its a dangerous crutch, since it allowes to overlay any signal over another
    # fortunately, this method will throw an error, if the time vectors are way too different, which should be a clear warning, that something being implemented cannot be right.
    # todo: decide on what to do in these cases
    time = np.linspace(0, U2obj.time[-1], num=len(U1obj.in_V), endpoint=True)
    U1obj = signal_class(time, U1obj.in_V)
######### end

    U1 = U1obj.get_signal_in_V_old_convention()
    U2 = U2obj.get_signal_in_V_old_convention()
    #
    # ###########
    #
    l_in = U1.shape[0]
    l_out = U2.shape[0]
    # Signallängen anpassen und interpolieren
    x_in = np.linspace(1, l_out, l_in)
    x_out = np.linspace(1, l_out, l_out)
    f = interp1d(x_in, U1[:, 1])

    # Signale übereinanderschieben -> über Kreuzkorrelation


    # print("Kreuzkorrelation")

    U1_vector1 = f(x_out)



    U1obj.sample_rate = U2obj.sample_rate

    U1_vector = U1obj.in_V

    d = U1_vector1 - U1_vector

    U2_signal = U2[:, 1]

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

    f2 = interp1d(x_out, U1_shifted_tmp)
    # g=interp1d(x_out, Uquest)
    U1_shifted_n1 = copy.copy(U1)
    U1_shifted_n1[:,1] = f2(x_in)

    U1_shifted_n2 = copy.copy(U2)
    U1_shifted_n2[:, 1] = U1_shifted_tmp

    #######

    # U1_shifted_n1 = signal_class.gen_signal_from_old_convention(U1_shifted_n1[:,0], U1_shifted_n1[:,1])
    # U1_shifted_n2 = signal_class.gen_signal_from_sample_rate(U1_shifted_n2[:, 0], U1_shifted_n2[:, 1])

    U1_shifted_n2 = signal_class(U2obj.time, U1_shifted_tmp)

    return U1_shifted_n2