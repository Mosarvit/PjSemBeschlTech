# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017
@author: denys
"""

import matplotlib.pyplot as plt
#import time
#from scipy import interpolate
from settings import show_plots
from helpers.apply_transfer_function import apply_transfer_function
from classes.signal_class import signal_class
from helpers.plot_helper import plot_2_signals

def compute_Uquest_from_Uout(Uout, H, verbosity=0):

    """
    compute_Uquest_from_Uout berechten Uquest aus Uout mithilfe der Invertierung der Übetragungsfunktion H
    INPUT:
        Uout - nx2 array; Ausgangssignal (n - Länge des Signals)
            Uout[:,0] - Zeitvektor
            Uout[:,1] - Signalvektor
        H - nx3 array; Übertragungsfunktion (n - Anzahl der Frequenzen)
            H[:,0] - Frequenz f
            H[:,1] - Amplitudenverstärkung
            H[:,2] - Phasenverschiebung
        verbosity - boolean; ob Uin gelplottet werden soll
    OUTPUT:
        Uquest - nx2 array; U_? (n - Länge des Signals)
            Uquest[:,0] - Zeitvektor
            Uquest[:,1] - Signalvektor
    """

    Uquest = apply_transfer_function(Uout = Uout, H = H.get_inverse())

    # plot_2_signals(Uout, Uquest)
    Uquest_doubled = signal_class(Uquest.time, Uquest.in_V)

    if verbosity:
        fig = plt.figure()
        plt.plot(Uquest_doubled.time,Uquest_doubled.in_V)
        plt.title('Uquest')
        # plt.grid(True)
        plt.ylabel('u')
        plt.xlabel('t')
        if show_plots :
            plt.show()
        #fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/U_quest_measured.pdf')

    return Uquest_doubled