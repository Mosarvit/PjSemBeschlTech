import numpy as np
from scipy.interpolate import interp1d
import copy
from helpers.find_nearest import find_nearest

def setVpp(signal, Vpp):
    """
    setVpp setzt die Spitze-zu-Spitze Amplitude eines Signals

    INPUT:
        Vpp - positive scalar; Spitze-zu-Spitze Spannung
        signal - nx2 array; das Signal (n - Länge des Signals)
             signal[:,0] - Zeitvektor
             signal[:,1] - Signalvektor
    OUTPUT:
        signal_Vpp - nx2 array; das Signal mit gesetzter Spitze-zu-Spitze Spannung (n - Länge des Signals)
             signal_Vpp[:,0] - Zeitvektor
             signal_Vpp[:,1] - Signalvektor
    """

    signal_Vpp = copy.copy(signal)
    signal_Vpp[:, 1] = Vpp / (max(signal[:, 1]) - min(signal[:, 1])) * signal[:, 1]
    return signal_Vpp

def convert_V_to_mV(signal):
    """
    convert_mV_to_V rechnet ein Signal von Volt nach milliVolt um

    INPUT:
        signal_in - nx2 array; Signal in Volt (n - Länge des Signals)
             signal_in[:,0] - Zeitvektor
             signal_in[:,1] - Signalvektor
    OUTPUT:
        signal_out - nx2 array; Signal in milliVolt (n - Länge des Signals)
             signal_out[:,0] - Zeitvektor
             signal_out[:,1] - Signalvektor
    """
    signal_mV = copy.copy(signal)
    signal_mV[:, 1] = signal_mV[:, 1] * 1000;
    return signal_mV

def convert_mV_to_V(signal_mV):
    """
    convert_mV_to_V rechnet ein Signal von milliVolt nach Volt um

    INPUT:
        signal_mV - nx2 array; Signal in milliVolt (n - Länge des Signals)
             signal_mV[:,0] - Zeitvektor
             signal_mV[:,1] - Signalvektor
    OUTPUT:
        signal - nx2 array; Signal in Volt (n - Länge des Signals)
             signal[:,0] - Zeitvektor
             signal[:,1] - Signalvektor
    """
    signal = copy.copy(signal_mV)
    signal[:, 1] = signal_mV[:, 1] / 1000;
    return signal


def setSampleRate(signal, sampleRate):

    """
    setSampleRate setzt die Abtastrate eines Signals

    INPUT:
        sampleRate - positive integer; Abtastrate
        signal - nx2 array; das Signal (n - Länge des Signals)
             signal[:,0] - Zeitvektor
             signal[:,1] - Signalvektor
    OUTPUT:
        signal_Vpp - nx2 array; das Signal mit gesetzter Abtastrate (n - Länge des Signals)
             signal_Vpp[:,0] - Zeitvektor
             signal_Vpp[:,1] - Signalvektor
    """

    T = max(signal[:, 0]) - min(signal[:, 0])
    lenght_new = int(np.floor(T * sampleRate))
    indices_old = np.arange(0, signal.shape[0])
    indices_new = np.linspace(0, signal.shape[0] - 1, num=lenght_new)
    interpolator1 = interp1d(indices_old, np.transpose(signal))
    signal_SR = np.transpose(interpolator1(indices_new))
    return signal_SR

def cun_one_period(signal, f):
    """
    cun_one_period schneidet eine Periode des Signals raus

    INPUT:
        f - positive integer; Frequenz
        signal - n1x2 array; das Signal (n1 - Länge des Signals)
             signal[:,0] - Zeitvektor
             signal[:,1] - Signalvektor
    OUTPUT:
        signal_cut - n2x2 array; eine Periode des Signals (n2 - Länge des Signals)
             signal_cut[:,0] - Zeitvektor
             signal_cut[:,1] - Signalvektor
    """
    T = 1 / f
    indT = find_nearest(signal[:, 0], T + signal[0, 0])
    signal_cut = signal[0:indT, :]

    return signal_cut