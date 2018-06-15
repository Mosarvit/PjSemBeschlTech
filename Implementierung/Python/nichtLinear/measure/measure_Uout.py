# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
from compute import compute_Uin_from_Uquest
from helpers import read_from_DSO, write_to_AWG
import numpy as np
import matplotlib.pyplot as plt
from helpers import csvHelper
from numpy import genfromtxt


def measure(Uin, Vpp, id, loadCSV, saveCSV, verbosity):

    if loadCSV :
        Uout_measured = genfromtxt('data/current_data/Uout_'+id+'.csv', delimiter=',')

    else:

        T = max(Uin[:, 0]) - min(Uin[:, 0])
        sampleRateAWG = int(np.floor(Uin.shape[0] / T))

        def sendUinToAWG(Uin):
            UinNormalized = Uin[:,1]/(max(Uin[:,1])-min(Uin[:,1])) # todo : is it necessary to normalize Uin ?
            write_to_AWG.send(UinNormalized, sampleRateAWG, Vpp)  # Rückbage wird nicht benötigt

        def receiveFromDSO(Uin):
            fmax = 80e6
            samplerateOszi = 1 * sampleRateAWG

            [time, dataUin, dataUout] = read_from_DSO.read(samplerateOszi, Vpp/10, fmax, Uin[:, 1])

            if saveCSV:
                csvHelper.save_2cols('data/current_data/Uout_'+id+'.csv', time, dataUout)

            return(time, dataUin, dataUout)



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


