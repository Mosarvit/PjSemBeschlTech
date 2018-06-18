from blocks import get_H
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from helpers import csvHelper, globalVars

def measure(loadCSV, saveCSV, verbosity):

    if loadCSV :
        Ha = genfromtxt('data/current_data/H_a.csv', delimiter=',')
        Hph = genfromtxt('data/current_data/H_p.csv', delimiter=',')[:,1]
        f = Ha[:,0]
        Ha = Ha[:,1]
    else :
        fmax = 80e6
        vpp = 40e-3
        f, Ha, Hph = get_H.get(fmax, vpp)

        if saveCSV:
            csvHelper.save_2cols('data/current_data/H_a.csv', f, Ha)
            csvHelper.save_2cols('data/current_data/H_p.csv', f, Hph)

    # assemble H

    H = np.zeros((len(f), 3));
    H[:,0] = f
    H[:,1] = Ha
    H[:,2] = Hph

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
        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/H_a.pdf')

        fig = plt.figure()
        plt.plot(f, Hph)
        plt.title('Phase in rad')
        plt.xlabel('f')

        if globalVars.showPlots:
            plt.show()
        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/H_p.pdf')


    return H