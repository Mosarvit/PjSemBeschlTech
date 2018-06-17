# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
from helpers import read_from_DSO, write_to_AWG
import numpy as np
import matplotlib.pyplot as plt
from helpers import csvHelper, signalHelper
from numpy import genfromtxt
from helpers import globalVars


def measure(Uin, sampleRateAWG, id, loadCSV, saveCSV, verbosity):

    def sendUinToAWG(Uin):
        Vpp = max(Uin[:, 1]) - min(Uin[:, 1])
        UinNormalized = Uin[:,1]/Vpp # todo : is it necessary to normalize Uin ?
        write_to_AWG.send(UinNormalized, sampleRateAWG, Vpp)  # Rückbage wird nicht benötigt

    def receiveFromDSO(Uin):
        fmax = 80e6
        samplerateOszi = 1 * sampleRateAWG
        Vpp = max(Uin[:, 1]) - min(Uin[:, 1])

        [time, dataUin, dataUout] = read_from_DSO.read(samplerateOszi, Vpp/10, fmax, Uin[:, 1])

        if saveCSV:
            csvHelper.save_2cols('data/current_data/Uout_'+id+'.csv', time, dataUout)

        return(time, dataUin, dataUout)

    if loadCSV :
        Uout_measured = genfromtxt('data/current_data/Uout_'+id+'.csv', delimiter=',')

    else:

        Uin = signalHelper.setSampleRate(Uin, sampleRateAWG)

        sendUinToAWG(Uin)
        [time, dataUin, dataUout] = receiveFromDSO(Uin)
        Uout_measured = np.zeros((len(time),2));
        Uout_measured[:,0] = time
        Uout_measured[:,1] = dataUout

    if verbosity:
        fig = plt.figure()
        plt.plot(Uout_measured[:,0], Uout_measured[:,1])
        plt.title('Uout_measured')
        plt.xlabel('t')
        plt.ylabel('U')
        if globalVars.showPlots :
            plt.show()
        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/Uout_measured.pdf')



    return(Uout_measured)


