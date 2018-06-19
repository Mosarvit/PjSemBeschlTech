# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
from helpers import read_from_DSO, write_to_AWG
import numpy as np
import matplotlib.pyplot as plt
from helpers.csvHelper import save_2cols
from numpy import genfromtxt
from helpers import globalVars
from helpers.signalHelper import assemble_signal
from helpers.signalHelper import setSampleRate
from helpers.overlay import overlay


def measure_Uout(Uin, sampleRateAWG, id, loadCSV, saveCSV, verbosity):

    """
    compute_Uin_from_Uquest berechten Uin aus Uquest mithilfe der Lookuptabelle K

    INPUT:

        Uin - n1x2 array; Eingangssignal in Volt :
            Uquest[:,0] - Zeitvektor
            Uquest[:,1] - Signalvektor

        sampleRateAWG - skalar; Abtastarte des AWG

        saveCSV - boolean; ob Uout gespreichert werden soll
        loadCSV - boolean; ob Uout aus vorhandenen CSV-Datei ausgelesen werden soll
        verbosity - boolean; ob Uout gelplottet werden soll

    OUTPUT:

        Uout_measured - n2x2 array; das gemessene Uout :
            Uout_measured[:,0] - Zeitvektor
            Uout_measured[:,1] - Signalvektor

        Uin_measured - n2x2 array; das gemessene Uin :
            Uin_measured[:,0] - Zeitvektor
            Uin_measured[:,1] - Signalvektor

    """

    ####################################################################################################################
    # Local functions
    ####################################################################################################################

    def sendUinToAWG(Uin):
        Vpp = max(Uin[:, 1]) - min(Uin[:, 1])
        UinNormalized = Uin[:,1]/Vpp # todo : is it necessary to normalize Uin ?
        write_to_AWG.write(UinNormalized, sampleRateAWG, Vpp)  # Rückbage wird nicht benötigt

    def receiveFromDSO(Uin):
        fmax = 80e6
        samplerateOszi = 1 * sampleRateAWG
        Vpp = max(Uin[:, 1]) - min(Uin[:, 1])

        [time, dataUin, dataUout] = read_from_DSO.read(samplerateOszi, Vpp/10, fmax, Uin[:, 1])

        if saveCSV:
            save_2cols('data/current_data/Uout_'+id+'.csv', time, dataUout)
            save_2cols('data/current_data/Uin_' + id + '.csv', time, dataUin)

        return(time, dataUin, dataUout)

    ####################################################################################################################
    # Here the actual function begins.
    ####################################################################################################################

    if loadCSV :
        Uout_measured = genfromtxt('data/current_data/Uout_'+id+'.csv', delimiter=',')
        Uin_measured = genfromtxt('data/current_data/Uin_' + id + '.csv', delimiter=',')
    else:

        Uin = setSampleRate(Uin, sampleRateAWG)

        sendUinToAWG(Uin)
        [time, dataUin, dataUout] = receiveFromDSO(Uin)

        Uout_measured = assemble_signal(time, dataUout)
        Uin_measured = assemble_signal(time, dataUin)

    if verbosity:
        fig = plt.figure()
        plt.plot(Uout_measured[:,0], Uout_measured[:,1])
        plt.title('Uout_measured')
        plt.xlabel('t')
        plt.ylabel('U')
        if globalVars.showPlots :
            plt.show()
        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/Uout_measured.pdf')

        _, Uin_measured_overlay = overlay(Uin_measured, Uin)

        fig = plt.figure()
        plt.plot(Uin[:, 0], Uin[:, 1])
        plt.plot(Uin_measured[:, 0], Uin_measured[:, 1])
        plt.title('Uin vs. Uin_measured')
        plt.xlabel('t')
        plt.ylabel('U')
        if globalVars.showPlots:
            plt.show()
        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/UinVsUin_measured.pdf')


    return(Uin_measured, Uout_measured)




