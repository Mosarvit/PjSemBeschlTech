from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.measure_H import measure_H
from blocks.measure_Uout import measure_Uout
from helpers.signal_helper import convert_V_to_mV
from helpers.signal_helper import convert_mV_to_V
from helpers.signal_helper import setVpp
from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention
from settings import project_path
from classes.signal_class import signal_class
from copy import copy
from helpers.csv_helper import save_2cols
from settings import use_mock_system
from classes.signal_class import signal_class
from helpers.csv_helper import save_signal, save_transfer_function
from blocks.adjust_H import adjust_H
from numpy import genfromtxt
import matplotlib.pyplot as plt
from settings import project_path
from blocks.determine_a import determine_a
from helpers.plot_helper import plot_2_transfer_functions, plot_2_signals

from helpers.signal_evaluation import signal_evaluate

def loop_adjust_H(H, K, Uout_ideal, data_directory, num_iters, sample_rate_DSO):
    quality_development = []

    for i in range(1, num_iters + 1):
        id = str(i)
        # compute new Uin
        Uquest = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H)

        Uin = compute_Uin_from_Uquest(Uquest=Uquest, K=K)

        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO)

        save_signal(Uin_measured, data_directory + 'Uin_measured_uncut_' + id + '.csv')
        save_signal(Uout_measured, data_directory + 'Uout_measured_uncut_' + id + '.csv')

        # plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured_uncut', 'Uout_measured_uncut')

        f_rep_fix = 9e5
        Uout_measured = Uout_measured.cut_one_period(f_rep_fix)
        Uin_measured = Uin_measured.cut_one_period(f_rep_fix)

        # save Uin and Uout
        save_signal(Uin, data_directory + 'Uin_awg_' + id + '.csv')
        save_signal(Uquest, data_directory + 'Uquest_' + id + '.csv')
        save_signal(Uin_measured, data_directory + 'Uin_measured_' + id + '.csv')
        save_signal(Uout_measured, data_directory + 'Uout_measured_' + id + '.csv')

        # plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured', 'Uout_measured')

        quality = signal_evaluate(data_directory + 'Uout_measured_' + id + '.csv', data_directory + 'quality_' + id + '.csv')
        sigma_H = 0.5
        quality_development.append(quality)

        H = adjust_H(H, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=0)

        save_transfer_function(H, directory=data_directory, id=id)

        plot_H_0_H_current(H, id, data_directory)

    print('quality_development' + str(quality_development))
    return H, Uout_measured, quality_development

def plot_H_0_H_current(H, id, data_directory):
    verbosity = 0
    if verbosity:
        H_0 = read_in_transfer_function_old_convention(data_directory + 'Ha_0.csv', data_directory + 'Hp_0.csv')
        plot_2_transfer_functions(H1=H_0, H2=H, legend1='H_0', legend2='H_' + id)