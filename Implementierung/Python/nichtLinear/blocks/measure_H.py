from blocks import get_H
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from helpers import csvHelper
from adts.transfer_function import transfer_function

def measure_H(loadCSV, saveCSV, verbosity):

    """
    measure_H misst die Übertragungsfunktion

    INPUT:

        saveCSV - boolean; ob H gespreichert werden soll
        loadCSV - boolean; ob H aus vorhandenen CSV-Datei ausgelesen werden soll
        verbosity - boolean; ob H gelplottet werden soll

    OUTPUT:

        H - nx3 array; Übertragungsfunktion (old Version) :
            H[:,0] - Frequenz f
            H[:,1] - Amplitudenverstärkung
            H[:,2] - Phasenverschiebung

        Instance of transfer_funtion:
            Halt.f - Frequences f
            Halt.a - Amplitude a
            Halt.p - Phaseshift p
            Halt.c - Complex Value c = a*exp(jp)

    """

    if loadCSV :
        Ha = genfromtxt('data/current_data/H_a.csv', delimiter=',')
        Hph = genfromtxt('data/current_data/H_p.csv', delimiter=',')[:,1]
        f = Ha[:,0]
        Ha = Ha[:,1]
    else :
        fmax = 80e6
        vpp = 40e-3
        f, Ha, Hph = get_H.compute(fmax, vpp, bits=9)

        if saveCSV:
            csvHelper.save_2cols('data/current_data/H_a.csv', f, Ha)
            csvHelper.save_2cols('data/current_data/H_p.csv', f, Hph)

    # assemble H

    # H = np.zeros((len(f), 3));
    # H[:,0] = f
    # H[:,1] = Ha
    # H[:,2] = Hph

    H = transfer_function(f)
    H.a = Ha
    H.p = Hph

    if verbosity:
        # fig = plt.figure()
        # plt.subplot(1, 2, 1)
        # plt.plot(f, Ha)
        # plt.title('Amplitude')
        # plt.xlabel('f')
        #
        # plt.subplot(1, 2, 2)
        # plt.plot(f, Hph)
        # plt.title('Phase in rad')
        # plt.xlabel('f')
        #
        # if globalVars.showPlots :
        #     plt.show()
        # fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/H.pdf')

        fig = plt.figure()
        plt.plot(f, Ha)
        plt.title('Amplitude')
        plt.xlabel('f')

        if globalVars.showPlots :
            plt.show()
        #fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/H_a.pdf')

        fig = plt.figure()
        plt.plot(f, Hph)
        plt.title('Phase in rad')
        plt.xlabel('f')

        if globalVars.showPlots:
            plt.show()
       # fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/H_p.pdf')


    return H