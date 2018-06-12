# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
from compute import compute_Uin_from_Uquest
from helpers import writeAWG, writeDSO
import numpy as np
import matplotlib.pyplot as plt


def measure(Uin, verbosity):

    samplerateAWG = 999900000

    def sendUinToAWG(Uin):
        vpp = max(Uin)-min(Uin)
        UinNormalized = Uin/vpp
        send_to_AWG.send(UinNormalized, samplerateAWG, vpp)  # Rückbage wird nicht benötigt

    def receiveFromDSO(Uin):
        vpp = max(Uin) - min(Uin)
        fmax = 80e6
        samplerateOszi = 100 * samplerateAWG
        [time, dataUin, dataUout] = writeDSO.writeDSO(samplerateOszi, vpp, fmax, Uin)

    sendUinToAWG(Uin)
    [time, dataUin, dataUout] = receiveFromDSO(Uin)
    Uout_measured = np.zeros((len(time),2));
    Uout_measured[:,0] = time
    Uout_measured[:,1] = dataUout

    if verbosity:
        plt.figure()
        plt.plot(Uout_measured)
        plt.title('Uout_measured')
        plt.ylabel('u')
        plt.ylabel('t')
        plt.show()



    return(Uout_measured)


