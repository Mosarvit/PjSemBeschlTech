
from adts.transfer_function import transfer_function
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import csv
from numpy import genfromtxt
from blocks.generate_BBsignal import generate_BBsignal
from helpers.csvHelper import read_in_transfer_function, read_in_transfer_function_old


def plot_this():
    # Initialization
    sampleRateDSO = 999900000
    f_rep = 900e3
    sampleRateAWG = 223 * f_rep
    f_BB = 5e6
    Vpp = 0.3

    Uout_ideal = np.transpose(generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sampleRateAWG=sampleRateAWG, saveCSV=False,verbosity=0))


    meas_Nr = 1

    if meas_Nr == 1:
        H_0 = read_in_transfer_function_old('Messung1/Ha_0.csv',
                                             'Messung1/Hp_0.csv')
        H_1 = read_in_transfer_function_old('Messung1/H_a_1.csv',
                                             'Messung1/H_p_1.csv')
        Uout_measured_0 = genfromtxt('Messung1/Uout_0.csv', delimiter=',')
        Uout_measured_1 = genfromtxt('Messung1/Uout_1.csv', delimiter=',')

        delta_t_meas = (Uout_measured_0[1, 0] - Uout_measured_0[0, 0])
        delta_t_id = (Uout_ideal[1, 0] - Uout_ideal[0, 0])
        print('Zeitstep Meas: ' + str(delta_t_meas) + ' Zeitstep Ideal: ' + str(delta_t_id))
        fig = plt.figure(1)
        # Plot Spannungen
        plt.plot(Uout_ideal[:, 0], Uout_ideal[:, 1], 'r', Uout_measured_0[:, 0], Uout_measured_0[:, 1],
                 'b', Uout_measured_1[:, 0], Uout_measured_1[:, 1], 'g')
        plt.title('Uout_ideal - rot, Uout_meas_0 - blau, Uout_meas_1 - gruen')
        plt.xlabel('t')
        plt.ylabel('U')
        plt.show()
        # Plot H
        plt.plot(H_0.f, H_0.a, 'r', H_1.f, H_1.a, 'b')
        plt.title('H_0 - rot, H_1 - blau')
        plt.xlabel('f')
        plt.ylabel('Amp')
        plt.show()


plot_this()