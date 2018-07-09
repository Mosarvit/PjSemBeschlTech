# -*- coding: utf-8 -*-
import numpy as np
from helpers import read_from_DSO

def read_from_DSO_resolution(samplerateOszi, vpp_ch1, fmax, signal):

    """

    read_from_DSO liest das Eingagns- und Ausgangssignal aus DSO ein

    INPUT:

        vpp_ch1 : skalar; Output peak-peak voltage of the signal
        samplerateOszi: positiver integer; Abtastrate des DSO
        fmax : positiver skalar; max frequency of interest
        signal : nx1 vector; Signalvektor

    OUTPUT:

        time : nx1 vector; Zeitvektor
        dataUin : nx1 vector; Signalvektor des Eingangssignals (Vorausgesetzt richtig angeschlossen ans DSO)
        dataUout : nx1 vector; Signalvektor des Eingangssignals (Vorausgesetzt richtig angeschlossen ans DSO)

    """
    # mit vpp_out = 0.3 erreichen wir den Wert wie in Denys Version
    vpp_out = 0.3
    # erste Messung
    time, dataUin, dataUout = read_from_DSO.read(samplerateOszi, vpp_ch1, vpp_out, fmax, signal)
    vpp_out = 2*np.amax(np.abs(dataUout))
    # Jetzt noch einmal mit angepasster Amplitude
    time, dataUin, dataUout = read_from_DSO.read(samplerateOszi, vpp_ch1, vpp_out, fmax, signal)

    
    return (time, dataUin, dataUout)