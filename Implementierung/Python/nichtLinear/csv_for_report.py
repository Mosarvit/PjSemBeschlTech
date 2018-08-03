import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from evaluate_adjust_H import evaluate_adjust_H
from helpers.plot_helper import plot_2_signals, plot_2_transfer_functions
from helpers import csv_helper, plot_helper
from helpers.csv_helper import read_in_transfer_function
from classes.transfer_function_class import transfer_function_class
from classes.signal_class import signal_class
from settings import project_path, mock_data_path
from blocks.generate_BBsignal import generate_BBsignal
from helpers.signal_evaluation import signal_evaluate
from scipy import linalg
import numpy as np


def printCSV(saveCSV=False):
    quality_development = []
    data_path = project_path + 'data/optimizer/adjust_H_19_07_2018-10_58_39/'

    # initial:
    H=csv_helper.read_in_transfer_function(data_path + 'H_0.csv')
    K = csv_helper.read_in_K(data_path + 'K_initial.csv')
    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.6

    sample_rate_AWG_max = 2e8
    sample_rate_DSO = 9999e5

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max)

    num_iters=3
    for i in range(1, num_iters + 1):
        id = str(i)
        # compute new Uin

        Uout_measured = csv_helper.read_in_signal(data_path + 'Uout_measured_' + id + '.csv')

        sigma_H = 0.5

        H_calc, f_abs_calc, Id_spectrum, Meas_spectrum, rms, rms_orig = adjust_H(H, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=1)
        H_old = transfer_function_class(H.f)
        H_old.c = H.c

        H = csv_helper.read_in_transfer_function(data_path + 'H_' + id + '.csv')

        f_abs_load = (1 - H.a / H_old.a) / sigma_H

        f_load_sig = signal_class(H.f, f_abs_load)
        f_calc_sig = signal_class(H.f, f_abs_calc)

        plt.subplot(3,1,1)
        plt.scatter(Id_spectrum.time, np.abs(Id_spectrum.in_V), s=3, c='r')
        plt.scatter(Meas_spectrum.time, np.abs(Meas_spectrum.in_V), s=3, c='b')
        plt.xlabel('f')
        plt.ylabel('abs FFT')
        plt.title('r Ideal, b Meas')

        plt.subplot(3, 1, 2)
        plt.plot(H.f, f_abs_load, 'b', H_calc.f, f_abs_calc, 'r')
        # plt.xlim((0, np.max(Halt.f)))
        # plt.ylim((-rms * 3, 3 * rms))
        plt.title('Absratio b load, r calc')
        plt.xlabel('f')
        plt.ylabel('ratio')
        # plt.show()

        plt.subplot(3,1,3)
        plt.plot(H.f, H.a, 'b', H_calc.f, H_calc.a, 'r', H_old.f, H_old.a, 'g')
        plt.title('Abs(H): b load, r calc, g old')
        plt.xlabel('f')
        plt.ylabel('Magnitude')
        # plt.xlim((0, np.max(Halt.f)))
        plt.show()
        if saveCSV:
            csv_helper.save_2cols(data_path+'Spectrum_Ideal_'+id+'.csv', Id_spectrum.time, np.abs(Id_spectrum.in_V))
            csv_helper.save_2cols(data_path+'Spectrum_Meas_'+id+'.csv', Meas_spectrum.time, np.abs(Meas_spectrum.in_V))
            csv_helper.save_2cols(data_path + 'Spectrum_Ideal_angle' + id + '.csv', Id_spectrum.time,
                                  np.angle(Id_spectrum.in_V))
            csv_helper.save_2cols(data_path + 'Spectrum_Meas_angle' + id + '.csv', Meas_spectrum.time,
                                  np.angle(Meas_spectrum.in_V))
            csv_helper.save_signal(f_calc_sig, data_path + 'f_abs_calc_' + id + '.csv')
            csv_helper.save_signal(f_load_sig, data_path + 'f_abs_load_' + id + '.csv')

        err = linalg.norm(H_calc.a - H.a) / linalg.norm(H.a)
        print(err)
        print('RMS: '+ str(rms) + ' von reinem: ' + str(rms_orig))
        #csv_helper.save_signale(f_calc_sig, data_path + 'f_abs_orig_' + id + '.csv')

    return

printCSV(saveCSV=False)