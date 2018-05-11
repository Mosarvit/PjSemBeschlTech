import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np

from helpers import writeAWG, writeDSO

samplerateAWG = 999900000  # Samplerate des AWG Signals
vpp = 300e-3  # Vpp die das awg ausgeben soll

def plot_Results():

    plt.figure()
    plt.switch_backend('TkAgg')  # TkAgg (instead Qt4Agg)
    # fig, ax = plt.subplots(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')

    plt.subplot(2, 2, 1)
    plt.plot(t_in, U_in)
    plt.title('Das berechnete U_in')
    plt.ylabel('u in mV')

    plt.subplot(2, 2, 2)
    plt.plot(t_out_ideal, U_out_ideal)
    plt.title('Das ideale U_out')
    plt.ylabel('u in mV')

    # plt.subplot(2, 2, 3)
    # plt.plot(t_real, U_in_real)
    # plt.title('Das reale U_in')
    # plt.ylabel('u in mV')
    #
    # plt.subplot(2, 2, 4)
    # plt.plot(t_real, U_out_real)
    # plt.title('Das reale U_out')
    # plt.ylabel('u in mV')

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

def readIn_U_in():
    U_in = genfromtxt('../data/testdata/U_in.csv', delimiter=',')
    t_in = U_in[:, 0]
    U_in = U_in[:, 1]
    return U_in, t_in

def readIn_U_out_ideal():
    U_and_t_out_ideal = genfromtxt('../data/testdata/out_300.csv', delimiter=',')
    t_out_ideal = U_and_t_out_ideal[:, 0]
    U_out_ideal = U_and_t_out_ideal[:, 1]
    return t_out_ideal, U_out_ideal

def sendU_inToAWG():
    writeAWG.writeAWG(U_in, samplerateAWG, vpp)  # Rückbage wird nicht benötigt

def receiveFromDSO():
    fmax = 80e6
    samplerateOszi = 100 * samplerateAWG
    [time, dataUin, dataUout] = writeDSO.writeDSO(samplerateOszi, vpp, fmax, U_in)
    return time, dataUin, dataUout


t_out_ideal, U_out_ideal = readIn_U_out_ideal()
U_in, t_in = readIn_U_in()
# sendU_inToAWG()
# t_real, U_in_real, U_out_real = receiveFromDSO()

plot_Results()

