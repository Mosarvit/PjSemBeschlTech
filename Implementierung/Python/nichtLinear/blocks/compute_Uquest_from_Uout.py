# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017
@author: denys
"""

import matplotlib.pyplot as plt
#import time
#from scipy import interpolate
import global_data
from helpers.apply_transfer_function import apply_transfer_function

def compute_Uquest_from_Uout(Uout, H, verbosity):

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

    Uquest = apply_transfer_function(Uout, H.get_inverse())
    Uquest[:,1] = Uquest[:,1] * 2

    if verbosity:
        fig = plt.figure()
        plt.plot(Uquest[:,0],Uquest[:,1])
        plt.title('Uquest')
        # plt.grid(True)
        plt.ylabel('u')
        plt.xlabel('t')
        if global_data.showPlots :
            plt.show()
        #fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/U_quest_measured.pdf')

    return Uquest