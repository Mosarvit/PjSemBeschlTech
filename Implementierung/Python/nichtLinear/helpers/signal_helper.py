import numpy as np
from scipy.interpolate import interp1d
from  copy import copy
from scipy import linalg
from helpers.custom_value_error import custom_value_error
from classes.transfer_function_class import transfer_function_class


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

    signal_Vpp = copy(signal)
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
    signal_mV = copy(signal)
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
    signal = copy(signal_mV)
    signal[:, 1] = signal_mV[:, 1] / 1000;
    return signal


def set_sample_rate(signal, sampleRate):

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



def assemble_signal(time_vector, signal_vector):
    """
    cun_one_period schneidet eine Periode des Signals raus

    INPUT:
        signal_vector - n1x1 vector; das Signalvektor (n1 - Länge des Signals)
        time_vector - n1x1 vector; der Zeitvektor (n1 - Länge des Signals)
    OUTPUT:
        signal - n1x2 array; das Signal (n1 - Länge des Signals)
             signal[:,0] - Zeitvektor
             signal[:,1] - Signalvektor
    """
    signal = np.zeros((len(time_vector), 2));
    signal[:, 0] = time_vector
    signal[:, 1] = signal_vector
    return signal

def generateSinSum(fqAmp, t):

    from classes.signal_class import signal_class

    rg = range(fqAmp.shape[0])
    signal = np.zeros([len(t),2])
    signal[:,0] = t
    for ind in rg:
        signal[:,1] += fqAmp[ind, 1] * np.sin(fqAmp[ind, 0] * t)

    signal_obj = signal_class(signal[:, 0], signal[:, 1])

    return signal_obj

def calculate_error(values_computed, values_ideal):

    from classes.signal_class import signal_class

    if type(values_computed) is np.ndarray and type(values_ideal) is np.ndarray:

        if len(values_computed.shape) == 1 and len(values_ideal.shape) == 1 :
            datatype = 'a'
        elif len(values_computed.shape) == 2 and len(values_ideal.shape) == 2:
            datatype = 'K'
        else:
            raise custom_value_error("The computed value is of an appropriate shape")

    elif isinstance(values_computed, signal_class) and isinstance(values_ideal, signal_class) :
        datatype = 'signal'
    elif isinstance(values_computed, transfer_function_class) and isinstance(values_ideal, transfer_function_class):
        datatype = 'transfer_function'
    else:
        raise custom_value_error("The computed value is of an appropriate type")

    if datatype == 'signal':
        values_tested_vector = values_computed.in_V
        values_ideal_vector = values_ideal.in_V
    elif datatype == 'transfer_function':
        values_tested_vector = values_computed.c
        values_ideal_vector = values_ideal.c
    elif datatype == 'K':

        if len(values_computed) < len(values_ideal):
            fun = interp1d(values_ideal[:, 0], values_ideal[:, 1])
            values_ideal = copy(values_computed)
            values_ideal[:, 1] = fun(values_ideal[:, 0])
        elif len(values_computed) > len(values_ideal):
            fun = interp1d(values_computed[:, 0], values_computed[:, 1])
            values_computed = copy(values_ideal)
            values_computed[:, 1] = fun(values_computed[:, 0])


        values_tested_vector = values_computed[:, 1]
        values_ideal_vector = values_ideal[:, 1]
    elif datatype == 'a':
        values_tested_vector = values_computed
        values_ideal_vector = values_ideal
    else:
        raise custom_value_error("the datatype is unknown")


    err = abs(np.mean(values_tested_vector - values_ideal_vector)) / linalg.norm(values_ideal_vector)

    err = linalg.norm(values_tested_vector - values_ideal_vector) / linalg.norm(values_ideal_vector)

    return err

def signals_are_equal(U1, U2):
    err =  calculate_error(U1, U2)
    return err < 1e-10

def transfer_functions_are_equal(H1, H2):
    err = calculate_error(H1, H2)
    return err < 1e-10

def arrays_are_equal(array1, array2):
    err = calculate_error(array1, array2)
    return err < 1e-10

def find_nearest(array, value):

    """
    find_nearest findet den Index des Werts im vektor, der dem gesuchten Wert am nähsten liegt

    INPUT:
        array - der Vektor
        value - skalar; die gesuchte Zahl

    OUTPUT:
        idx - unsigned integer; der gesuchte Index
    """

    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
