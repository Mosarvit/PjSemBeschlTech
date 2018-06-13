# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
from compute import compute_Uin_from_Uquest
from helpers import read_from_DSO, write_to_AWG
import numpy as np
import matplotlib.pyplot as plt


def measure(Uin, verbosity):

    T = max(Uin[:, 0]) - min(Uin[:, 0])
    sampleRateAWG = Uin.shape[0] / T

    def sendUinToAWG(Uin):
        vpp = max(Uin[1,:])-min(Uin[1,:])
        UinNormalized = Uin[1,:]/vpp
        write_to_AWG.send(UinNormalized, sampleRateAWG, vpp)  # Rückbage wird nicht benötigt

    def receiveFromDSO(Uin):
        vpp = max(Uin[:,1]) - min(Uin[:,1])
        fmax = 80e6
        samplerateOszi = 100 * sampleRateAWG
        [time, dataUin, dataUout] = read_from_DSO.read(samplerateOszi, vpp, fmax, Uin[:,1])

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


