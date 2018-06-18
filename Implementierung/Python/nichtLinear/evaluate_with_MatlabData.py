import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np


from helpers import write_to_AWG, read_from_DSO

samplerateAWG = 999900000  # Samplerate des AWG Signals
vpp = 300e-3  # Vpp die das awg ausgeben soll

def plot_Results():

    plt.figure()
    plt.switch_backend('TkAgg')  # TkAgg (instead Qt4Agg)
    # fig, ax = plt.subplots(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')

    plt.subplot(2, 2, 1)
    plt.plot(t_in, Uin)
    plt.title('Das berechnete U_in')
    plt.ylabel('u in mV')

    plt.subplot(2, 2, 2)
    plt.plot(t_out_ideal, U_out_ideal)
    plt.title('Das ideale U_out')
    plt.ylabel('u in mV')

    plt.subplot(2, 2, 3)
    plt.plot(t_real, Uin_real)
    plt.title('Das reale Uin')
    plt.ylabel('u in mV')
    
    plt.subplot(2, 2, 4)
    plt.plot(t_real, U_out_real)
    plt.title('Das reale U_out')
    plt.ylabel('u in mV')

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

def readIn_Uin():
    Uin = genfromtxt('data/test_data/Uin.csv', delimiter=',')
    t_in = Uin[:, 0]
    Uin = Uin[:, 1]
    return Uin, t_in

def readIn_Uout_ideal():
    Uout_and_t_ideal = genfromtxt('data/test_data/Uout_300.csv', delimiter=',')
    tout_ideal = Uout_and_t_ideal[:, 0]
    Uout_ideal = Uout_and_t_ideal[:, 1]
    return tout_ideal, Uout_ideal

def sendUinToAWG():
    write_to_AWG.write(Uin, samplerateAWG, vpp)  # Rückbage wird nicht benötigt

def receiveFromDSO():
    fmax = 80e6
    samplerateOszi = 100 * samplerateAWG
    [time, dataUin, dataUout] = read_from_DSO.read(samplerateOszi, vpp, fmax, Uin)
    return time, dataUin, dataUout


t_out_ideal, U_out_ideal = readIn_Uout_ideal()
Uin, t_in = readIn_Uin()
sendUinToAWG()
t_real, Uin_real, U_out_real = receiveFromDSO()

plot_Results()

