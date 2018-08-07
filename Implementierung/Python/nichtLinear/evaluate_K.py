from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.determine_H import determine_H
from blocks.measure_Uout import measure_Uout
from helpers.signal_helper import convert_V_to_mV
from helpers.signal_helper import convert_mV_to_V
from helpers.signal_helper import setVpp
from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention
from settings import project_path
from copy import copy
from helpers.csv_helper import save_2cols
from settings import use_mock_system
from classes.signal_class import signal_class
from helpers.csv_helper import save_signal, save_transfer_function, read_in_transfer_function
from blocks.adjust_H import adjust_H
from numpy import genfromtxt
import matplotlib.pyplot as plt
from settings import project_path
from blocks.loop_adjust_H import loop_adjust_H
from blocks.determine_a import determine_a
from helpers.plot_helper import plot_vector

from helpers.signal_evaluation import signal_evaluate

from save_results import save, save_text



import numpy as np


def evaluate_K() :

    if use_mock_system :

        data_directory = project_path + 'tests/mock_data/mock_results/evaluate_K/'

    else :

        data_directory = project_path + save(path='data', name='evaluate_K') + '/'


    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.6

    sample_rate_AWG_max = 2e8
    sample_rate_DSO = 9999e5

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max)

    H = determine_H(loadCSV=1, saveCSV=1)

#    save_transfer_function(H=H, directory=data_directory, id = '0' )

    a = determine_a(H, Uout_ideal, sample_rate_DSO, data_directory)

    K = compute_K_from_a(a=a, verbosity=0)
    save_2cols(data_directory + '/K_initial.csv', K[:, 0], K[:, 1])

    Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H)
    save_signal(Uquest_ideal, data_directory + 'Uquest_ideal.csv')
    Uin, Uquest_ideal = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K_Uin_to_Uquest=K)

    quality_development = []
    Vpp_development = []
    for i in range(5,10):
        id = str(i)
        Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H)
        save_signal(Uquest_ideal, data_directory + 'Uquest_ideal_' + id + '.csv')
        
        Uquest_ideal.Vpp = 0.3*i*0.1
        Uin, Uquest_adapted = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K_Uin_to_Uquest=K)
        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO)

        save_signal(Uin_measured, data_directory + 'Uin_measured_uncut_' + id + '.csv')
        save_signal(Uout_measured, data_directory + 'Uout_measured_uncut_' + id + '.csv')

        # plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured_uncut', 'Uout_measured_uncut')

        f_rep_fix = 9e5
        Uout_measured = Uout_measured.cut_one_period(f_rep_fix)
        Uin_measured = Uin_measured.cut_one_period(f_rep_fix)

        # save Uin and Uout
        save_signal(Uin, data_directory + 'Uin_awg_' + id + '.csv')
        # save_signal(Uquest_ideal, data_directory + 'Uquest_' + id + '.csv')
        save_signal(Uin_measured, data_directory + 'Uin_measured_' + id + '.csv')
        save_signal(Uout_measured, data_directory + 'Uout_measured_' + id + '.csv')
        save_signal(Uquest_adapted, data_directory + 'Uquest_adapted_' + id + '.csv')

        # plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured', 'Uout_measured')

        # taken out because of causing recursion error
        quality = signal_evaluate(data_directory + 'Uout_measured_' + id + '.csv',
                                  data_directory + 'quality_' + id + '.csv')
        # quality = 5
        quality_development.append(quality)
        Vpp_development.append(Uquest_adapted.Vpp)

    print(quality_development)
    save_2cols(data_directory + 'quality_vpp.csv', np.asarray(Vpp_development), np.asarray(quality_development))
    if not use_mock_system :
        save_text(data_directory)

    return Vpp_development, quality_development
evaluate_K()


